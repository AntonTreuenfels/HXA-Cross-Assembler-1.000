@echo off
cls
echo I am in charge here (call me Al)

rem - run flag tests
rem   python hxa.py %tdir%test000.a [-q] [-h]

set tdir=test\

rem recognized flags (fail - no filename)

rem flag '-q'

echo. & echo Testing -q only & python hxa.py -q
if %errorlevel% NEQ 0 echo test FAILED! Errorlevel =%errorlevel%
echo.

rem flag '--quiet'

echo. & echo Testing --quiet only & python hxa.py --quiet
if %errorlevel% NEQ 0 echo test FAILED! Errorlevel =%errorlevel%
echo.

set tdir=