@echo off
REM ============================================
REM   Auto GitHub Drip-Feed — Scheduled Task
REM   Runs daily to commit the next batch of files
REM ============================================

cd /d "c:\Users\ganti\chart\AI automation"

REM Set encoding for emoji support
set PYTHONIOENCODING=utf-8

REM Date check
for /f "tokens=2 delims==" %%I in ('wmic os get localdatetime /value') do set datetime=%%I
set current_date=%datetime:~0,8%
if "%current_date%"=="20260625" (
    echo Skipping execution today (June 25) because manual commits were already pushed.
    exit /b 0
)

REM Load GitHub PAT from user environment
for /f "tokens=2*" %%a in ('reg query "HKCU\Environment" /v GITHUB_PAT 2^>nul') do set GITHUB_PAT=%%b

REM Run the drip-feed
python auto_commit.py --drip

REM Log completion
echo [%date% %time%] Drip-feed task completed >> "c:\Users\ganti\chart\AI automation\logs\scheduler.log"
