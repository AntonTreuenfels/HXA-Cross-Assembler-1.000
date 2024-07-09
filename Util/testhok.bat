@echo off
cls
echo I am in charge here (call me Al)

rem - run flag tests
rem   python hxa.py %tdir%test000.a [-q] [-h]

set tdir=test\

rem single source file

echo. & echo Testing source file only & python hxa.py %tdir%test000.a
if %errorlevel% NEQ 0 echo test FAILED! Errorlevel =%errorlevel%
echo.

rem recognized flags (ok)

rem flag '-h'

echo. & echo Testing -h only & python hxa.py -h
if %errorlevel% NEQ 0 echo test FAILED! Errorlevel =%errorlevel%
echo.

echo. & echo Testing source file and -h & python hxa.py %tdir%test000.a -h
if %errorlevel% NEQ 0 echo test FAILED! Errorlevel =%errorlevel%
echo.

echo. & echo Testing -h and sourcefile & python hxa.py -h %tdir%test000.a
if %errorlevel% NEQ 0 echo test FAILED! Errorlevel =%errorlevel%
echo.

rem flag '--help'

echo. & echo Testing --help only & python hxa.py --help
if %errorlevel% NEQ 0 echo test FAILED! Errorlevel =%errorlevel%
echo.

echo. & echo Testing sourcefile and --help & python hxa.py %tdir%test000.a --help
if %errorlevel% NEQ 0 echo test FAILED! Errorlevel =%errorlevel%
echo.

echo. & echo Testing --help and sourcefile & python hxa.py %tdir%test000.a --help
if %errorlevel% NEQ 0 echo test FAILED! Errorlevel =%errorlevel%
echo.

rem flag '/?'

echo. & echo Testing /? only & python hxa.py /?
if %errorlevel% NEQ 0 echo test FAILED! Errorlevel =%errorlevel%
echo.

echo. & echo Testing sourcefile and /? & python hxa.py %tdir%test000.a /?
if %errorlevel% NEQ 0 echo test FAILED! Errorlevel =%errorlevel%
echo.

echo. & echo Testing /? and sourcefile & python hxa.py %tdir%test000.a /?
if %errorlevel% NEQ 0 echo test FAILED! Errorlevel =%errorlevel%
echo.

set tdir=