@echo off
cls
echo I am in charge here (call me Al)

rem - run one specific test

set tdir=test68\

echo. & echo Testing %1 & python hxa.py %tdir%test%1.a -hxa68
echo.
echo The exit code is %errorlevel%

set tdir=