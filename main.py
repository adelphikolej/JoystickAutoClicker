import threading
import time
import tkinter as tk
from tkinter import ttk, messagebox

try:
    import vgamepad as vg
except ImportError:
    vg = None


BUTTONS = {
    "A": vg.XUSB_BUTTON.XUSB_GAMEPAD_A if vg else None,
    "B": vg.XUSB_BUTTON.XUSB_GAMEPAD_B if vg else None,
    "X": vg.XUSB_BUTTON.XUSB_GAMEPAD_X if vg else None,
    "Y": vg.XUSB_BUTTON.XUSB_GAMEPAD_Y if vg else None,
    "START": vg.XUSB_BUTTON.XUSB_GAMEPAD_START if vg else None,
    "SELECT / BACK": vg.XUSB_BUTTON.XUSB_GAMEPAD_BACK if vg else None,
    "LB": vg.XUSB_BUTTON.XUSB_GAMEPAD_LEFT_SHOULDER if vg else None,
    "RB": vg.XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_SHOULDER if vg else None,
    "UP": vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_UP if vg else None,
    "DOWN": vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_DOWN if vg else None,
    "LEFT": vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_LEFT if vg else None,
    "RIGHT": vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_RIGHT if vg else None,
}


class JoystickAutoClicker:
    def __init__(self, root):
        self.root = root
        self.root.title("Joystick AutoClicker")
        self.root.geometry("480x560")
        self.root.minsize(440, 520)
        self.root.configure(bg="#f3f6fb")

        self.gamepad = None
        self.worker = None
        self.stop_event = threading.Event()
        self.running = False

        style = ttk.Style()
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass
        style.configure("TFrame", background="#f3f6fb")
        style.configure("TLabel", background="#f3f6fb", font=("Segoe UI", 10))
        style.configure("Header.TLabel", font=("Segoe UI", 19, "bold"), foreground="#15345b")
        style.configure("Sub.TLabel", foreground="#5d6b7c")
        style.configure("TButton", font=("Segoe UI", 10, "bold"), padding=8)

        outer = ttk.Frame(root, padding=22)
        outer.pack(fill="both", expand=True)

        ttk.Label(outer, text="🎮 Joystick AutoClicker", style="Header.TLabel").pack(anchor="w")
        ttk.Label(outer, text="Automatically press a virtual Xbox controller button", style="Sub.TLabel").pack(anchor="w", pady=(4, 18))

        card = ttk.Frame(outer, padding=16)
        card.pack(fill="x")
        ttk.Label(card, text="Controller button").pack(anchor="w")
        self.button_var = tk.StringVar(value="A")
        self.button_combo = ttk.Combobox(
            card, textvariable=self.button_var, values=list(BUTTONS.keys()),
            state="readonly", font=("Segoe UI", 11)
        )
        self.button_combo.pack(fill="x", pady=(6, 14))

        ttk.Label(card, text="Press interval").pack(anchor="w")
        self.interval_var = tk.StringVar(value="1 second")
        self.interval_combo = ttk.Combobox(
            card, textvariable=self.interval_var,
            values=["100 ms", "250 ms", "500 ms", "1 second", "2 seconds", "5 seconds"],
            state="readonly", font=("Segoe UI", 11)
        )
        self.interval_combo.pack(fill="x", pady=(6, 14))

        ttk.Label(card, text="Repeat mode").pack(anchor="w")
        self.repeat_var = tk.StringVar(value="Continuous until STOP")
        self.repeat_combo = ttk.Combobox(
            card, textvariable=self.repeat_var,
            values=["Continuous until STOP", "10 presses", "100 presses"],
            state="readonly", font=("Segoe UI", 11)
        )
        self.repeat_combo.pack(fill="x", pady=(6, 4))

        self.status_var = tk.StringVar(value="Status: Stopped")
        ttk.Label(outer, textvariable=self.status_var, font=("Segoe UI", 11, "bold")).pack(anchor="w", pady=(18, 10))

        buttons = ttk.Frame(outer)
        buttons.pack(fill="x")
        self.start_button = tk.Button(
            buttons, text="▶  START", command=self.start,
            bg="#16803c", fg="white", activebackground="#11632e",
            activeforeground="white", relief="flat", font=("Segoe UI", 11, "bold"),
            padx=14, pady=12, cursor="hand2"
        )
        self.start_button.pack(side="left", fill="x", expand=True, padx=(0, 6))
        self.stop_button = tk.Button(
            buttons, text="■  STOP", command=self.stop,
            bg="#b4232f", fg="white", activebackground="#8e1c25",
            activeforeground="white", relief="flat", font=("Segoe UI", 11, "bold"),
            padx=14, pady=12, cursor="hand2", state="disabled"
        )
        self.stop_button.pack(side="left", fill="x", expand=True, padx=(6, 0))

        note = (
            "Important: this sends inputs through a virtual Xbox 360 controller. "
            "It does not directly press buttons on your physical controller. "
            "Some games may block virtual inputs or require controller setup."
        )
        ttk.Label(outer, text=note, wraplength=420, justify="left", style="Sub.TLabel").pack(anchor="w", pady=(18, 0))

        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def interval_seconds(self):
        value = self.interval_var.get()
        return {
            "100 ms": 0.1, "250 ms": 0.25, "500 ms": 0.5,
            "1 second": 1.0, "2 seconds": 2.0, "5 seconds": 5.0
        }[value]

    def start(self):
        if self.running:
            return
        if vg is None:
            messagebox.showerror(
                "Missing dependency",
                "Install the required package first:\n\npython -m pip install -r requirements.txt"
            )
            return
        try:
            self.gamepad = vg.VX360Gamepad()
        except Exception as exc:
            messagebox.showerror(
                "Virtual controller unavailable",
                "Could not create a virtual Xbox controller.\n\n"
                "Install the ViGEmBus driver (see README.txt), restart Windows if requested, "
                "then try again.\n\nDetails: " + str(exc)
            )
            return

        self.stop_event.clear()
        self.running = True
        self.start_button.configure(state="disabled")
        self.stop_button.configure(state="normal")
        self.button_combo.configure(state="disabled")
        self.interval_combo.configure(state="disabled")
        self.repeat_combo.configure(state="disabled")
        self.status_var.set("Status: Running — sending " + self.button_var.get())
        self.worker = threading.Thread(target=self.run_loop, daemon=True)
        self.worker.start()

    def run_loop(self):
        name = self.button_var.get()
        button = BUTTONS[name]
        mode = self.repeat_var.get()
        count_limit = 10 if mode == "10 presses" else 100 if mode == "100 presses" else None
        count = 0
        try:
            while not self.stop_event.is_set():
                # Send a short press and release so games register separate presses.
                self.gamepad.press_button(button=button)
                self.gamepad.update()
                if self.stop_event.wait(0.08):
                    break
                self.gamepad.release_button(button=button)
                self.gamepad.update()
                count += 1
                if count_limit is not None and count >= count_limit:
                    break
                if self.stop_event.wait(max(0, self.interval_seconds() - 0.08)):
                    break
        except Exception as exc:
            self.root.after(0, lambda: messagebox.showerror("Controller error", str(exc)))
        finally:
            try:
                if self.gamepad is not None:
                    self.gamepad.release_button(button=button)
                    self.gamepad.update()
            except Exception:
                pass
            self.root.after(0, self.finish_run)

    def finish_run(self):
        self.running = False
        self.start_button.configure(state="normal")
        self.stop_button.configure(state="disabled")
        self.button_combo.configure(state="readonly")
        self.interval_combo.configure(state="readonly")
        self.repeat_combo.configure(state="readonly")
        self.status_var.set("Status: Stopped")

    def stop(self):
        if self.running:
            self.status_var.set("Status: Stopping…")
            self.stop_event.set()

    def on_close(self):
        self.stop_event.set()
        self.root.after(100, self.root.destroy)


if __name__ == "__main__":
    root = tk.Tk()
    app = JoystickAutoClicker(root)
    root.mainloop()
