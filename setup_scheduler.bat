@echo off
echo ============================================
echo    Setting up Auto-Commit Task Scheduler
echo ============================================
echo.

REM Get the script directory
set SCRIPT_DIR=%~dp0

REM Create the scheduled task that runs daily at 9:30 PM
REM The Python script itself adds random delay (0-120 min)
schtasks /create /tn "AutoGitHubDrip" /tr "\"%SCRIPT_DIR%run_auto_commit.bat\" --drip" /sc daily /st 21:30 /f /rl HIGHEST

echo.
echo ============================================
echo    Task Scheduler setup complete!
echo    Task: AutoGitHubCommit
echo    Schedule: Daily at 9:30 PM
echo    Action: Runs auto_commit.py --drip
echo ============================================
echo.

REM Also create a task for normal auto-commit (for non-drip projects)
schtasks /create /tn "AutoGitHubCommitNormal" /tr "\"%SCRIPT_DIR%run_auto_commit.bat\"" /sc daily /st 22:00 /f /rl HIGHEST

echo.
echo    Additional task: AutoGitHubCommitNormal
echo    Schedule: Daily at 10:00 PM
echo    Action: Runs auto_commit.py (normal mode)
echo.
pause
