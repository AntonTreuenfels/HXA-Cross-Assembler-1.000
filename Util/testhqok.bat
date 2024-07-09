@echo off
cls
echo I am in charge here (call me Al)

rem - run flag tests
rem   python hxa.py %tdir%test000.a [-q] [-h]

set tdir=test\

rem single file, '-h' flag ( which takes precedence )

rem single source file

echo. & echo Testing source file and -h & python hxa.py %tdir%test000.a -h
if %errorlevel% NEQ 0 echo test FAILED! Errorlevel =%errorlevel%
echo.

echo. & echo Testing -h and source file & python hxa.py -h %tdir%test000.a
if %errorlevel% NEQ 0 echo test FAILED! Errorlevel =%errorlevel%
echo.

echo. & echo Testing source file and /? & python hxa.py %tdir%test000.a /?
if %errorlevel% NEQ 0 echo test FAILED! Errorlevel =%errorlevel%
echo.

echo. & echo Testing /? and source file & python hxa.py /? %tdir%test000.a
if %errorlevel% NEQ 0 echo test FAILED! Errorlevel =%errorlevel%
echo.

echo. & echo Testing source file and --help & python hxa.py %tdir%test000.a --help
if %errorlevel% NEQ 0 echo test FAILED! Errorlevel =%errorlevel%
echo.

echo. & echo Testing --help and source file & python hxa.py --help %tdir%test000.a
if %errorlevel% NEQ 0 echo test FAILED! Errorlevel =%errorlevel%
echo.

rem - double flags ( -h always takes precedence )

rem testing '-h' flag

echo. & echo Testing -h and -q & python hxa.py -h -q
if %errorlevel% NEQ 0 echo test FAILED! Errorlevel =%errorlevel%
echo.

echo. & echo Testing -q and -h & python hxa.py -q -h
if %errorlevel% NEQ 0 echo test FAILED! Errorlevel =%errorlevel%
echo.

echo. & echo Testing -h and --quiet & python hxa.py -h --quiet
if %errorlevel% NEQ 0 echo test FAILED! Errorlevel =%errorlevel%
echo.

echo. & echo Testing --quiet and -h & python hxa.py --quiet -h
if %errorlevel% NEQ 0 echo test FAILED! Errorlevel =%errorlevel%
echo.

rem - testing '/?' flag

echo. & echo Testing -/? and -q & python hxa.py /? -q
if %errorlevel% NEQ 0 echo test FAILED! Errorlevel =%errorlevel%
echo.

echo. & echo Testing -q and /? & python hxa.py -q /?
if %errorlevel% NEQ 0 echo test FAILED! Errorlevel =%errorlevel%
echo.

echo. & echo Testing /? and --quiet & python hxa.py /? --quiet
if %errorlevel% NEQ 0 echo test FAILED! Errorlevel =%errorlevel%
echo.

echo. & echo Testing --quiet and /? & python hxa.py --quiet /?
if %errorlevel% NEQ 0 echo test FAILED! Errorlevel =%errorlevel%
echo.

rem testing '--help' flag

echo. & echo Testing --help and -q & python hxa.py --help -q
if %errorlevel% NEQ 0 echo test FAILED! Errorlevel =%errorlevel%
echo.

echo. & echo Testing -q and --help & python hxa.py -q --help
if %errorlevel% NEQ 0 echo test FAILED! Errorlevel =%errorlevel%
echo.

echo. & echo Testing --help and --quiet & python hxa.py --help --quiet
if %errorlevel% NEQ 0 echo test FAILED! Errorlevel =%errorlevel%
echo.

echo. & echo Testing --quiet and --help & python hxa.py --quiet --help
if %errorlevel% NEQ 0 echo test FAILED! Errorlevel =%errorlevel%
echo.

rem Testing duplicate help flags

echo. & echo Testing -h and -h & python hxa.py -h -h
if %errorlevel% NEQ 0 echo test FAILED! Errorlevel =%errorlevel%
echo.

echo. & echo Testing -h and /? & python hxa.py -h /?
if %errorlevel% NEQ 0 echo test FAILED! Errorlevel =%errorlevel%
echo.

echo. & echo Testing /? and -h & python hxa.py /? -h
if %errorlevel% NEQ 0 echo test FAILED! Errorlevel =%errorlevel%
echo.

echo. & echo Testing -h and --help & python hxa.py -h --help
if %errorlevel% NEQ 0 echo test FAILED! Errorlevel =%errorlevel%
echo.

echo. & echo Testing --help and -h & python hxa.py --help -h
if %errorlevel% NEQ 0 echo test FAILED! Errorlevel =%errorlevel%
echo.

echo. & echo Testing /? and /? & python hxa.py /? /?
if %errorlevel% NEQ 0 echo test FAILED! Errorlevel =%errorlevel%
echo.

echo. & echo Testing /? and --help & python hxa.py /? --help
if %errorlevel% NEQ 0 echo test FAILED! Errorlevel =%errorlevel%
echo.

echo. & echo Testing --help and /? & python hxa.py --help /?
if %errorlevel% NEQ 0 echo test FAILED! Errorlevel =%errorlevel%
echo.

echo. & echo Testing --help and --help & python hxa.py --help --help
if %errorlevel% NEQ 0 echo test FAILED! Errorlevel =%errorlevel%
echo.


set tdir=


