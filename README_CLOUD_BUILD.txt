BUILD THE WINDOWS EXE WITHOUT INSTALLING PYTHON ON YOUR PC

This project includes a GitHub Actions workflow that builds the EXE on a hosted Windows runner.
You need a GitHub account and internet access, but do not need Python installed on your computer.

1. Sign in to GitHub and create a NEW repository. A private repository is fine.
2. Upload the contents of this ZIP to the repository's main branch. Make sure the .github/workflows/build-windows.yml file is included.
   If uploading through the website, you may need to use Add file > Upload files and preserve the .github/workflows folders.
3. Open the repository's Actions tab and select "Build Windows EXE" if prompted.
4. Open the latest successful workflow run.
5. At the bottom of the run page, find Artifacts and download "JoystickAutoClicker-Windows-EXE".
6. Extract the downloaded artifact ZIP. It contains JoystickAutoClicker.exe.

IMPORTANT
- This cloud workflow has not been run or verified in this chat.
- Windows may show a SmartScreen warning for an unsigned EXE. Only run it if you trust the source and have reviewed the code.
- The app sends inputs through a virtual Xbox controller, not by physically pressing your controller buttons. The game must accept virtual Xbox/XInput input.
- vgamepad may require a compatible ViGEmBus driver installed on the Windows PC. Driver compatibility and game/anti-cheat restrictions vary.
