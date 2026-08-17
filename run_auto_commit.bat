@echo off
REM Helper script to run auto-commit safely from Windows Task Scheduler
set PYTHONIOENCODING=utf8
cd /d "%~dp0"

for /f "tokens=2 delims==" %%I in ('wmic os get localdatetime /value') do set datetime=%%I
set current_date=%datetime:~0,8%


python auto_commit.py %*
