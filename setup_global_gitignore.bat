@echo off
echo ============================================
echo    Setting up Global .gitignore
echo ============================================
echo.

set GITIGNORE_PATH=%~dp0.gitignore_global

echo Setting global gitignore to: %GITIGNORE_PATH%
git config --global core.excludesfile "%GITIGNORE_PATH%"

echo.
echo Verifying...
git config --global core.excludesfile

echo.
echo ============================================
echo    Global .gitignore is now active!
echo    All repos on this machine will use it.
echo ============================================
echo.
pause
