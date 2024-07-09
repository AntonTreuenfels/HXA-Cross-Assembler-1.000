@echo off
cls
echo I am in charge here (call me Al)

rem - run flag tests
rem   python hxa.py %tdir%test000.a [-q] [-h]

set tdir=test\

rem recognized flags (ok)

rem flag '-q'

echo. & echo Testing source file and -q & python hxa.py %tdir%test000.a -q
if %errorlevel% NEQ 0 echo test FAILED! Errorlevel =%errorlevel%
echo.

echo. & echo Testing -q and sourcefile & python hxa.py -q %tdir%test000.a
if %errorlevel% NEQ 0 echo test FAILED! Errorlevel =%errorlevel%
echo.

rem flag '--quiet'

echo. & echo Testing sourcefile and --quiet & python hxa.py %tdir%test000.a --quiet
if %errorlevel% NEQ 0 echo test FAILED! Errorlevel =%errorlevel%
echo.

echo. & echo Testing --quiet and sourcefile & python hxa.py %tdir%test000.a --quiet
if %errorlevel% NEQ 0 echo test FAILED! Errorlevel =%errorlevel%
echo.

set tdir=