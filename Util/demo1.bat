@echo off
cls
echo I am in charge here (call me Al)

rem - run one specific test

set ddir=demo\

echo. & echo Testing %1 & python hxa.py %ddir%demo%1.a
echo.
echo The exit code is %errorlevel%

set ddir=