@echo off
cls
echo I am in charge here (call me Al)

rem - run flag tests
rem   python hxa.py %tdir%test000.a [-q] [-h]

set tdir=test\

rem no source file

echo. & echo Testing source file only & python hxa.py
if %errorlevel% NEQ 4 echo test FAILED! Errorlevel =%errorlevel%
echo.

rem  multiple source files (more than one)

echo. & echo Testing two source files & python hxa.py %tdir%test000.a %tdir%test001.a
if %errorlevel% NEQ 4 echo test FAILED! Errorlevel =%errorlevel%
echo.

echo. & echo Testing three source files & python hxa.py %tdir%test000.a %tdir%test001.a %tdir% test002.a
if %errorlevel% NEQ 4 echo test FAILED! Errorlevel =%errorlevel%
echo.

echo. & echo Testing four source files & python hxa.py %tdir%test000.a %tdir%test001.a %tdir% test002.a %tdir% test003.a
if %errorlevel% NEQ 4 echo test FAILED! Errorlevel =%errorlevel%
echo.

rem '-' only

echo. & echo Testing - only & python hxa.py -
if %errorlevel% NEQ 4 echo test FAILED! Errorlevel =%errorlevel%
echo.

echo. & echo Testing sourcefile and - & python hxa.py %tdir%test000.a -
if %errorlevel% NEQ 4 echo test FAILED! Errorlevel =%errorlevel%
echo.

echo. & echo Testing - and sourcefile & python hxa.py - %tdir%test000.a
if %errorlevel% NEQ 4 echo test FAILED! Errorlevel =%errorlevel%
echo.

rem bad flag, '-h' prefix

echo. & echo Testing -unrecognized only & python hxa.py -unrecognized
if %errorlevel% NEQ 4 echo test FAILED! Errorlevel =%errorlevel%
echo.

echo. & echo Testing sourcefile and -unrecognized & python hxa.py %tdir%test000.a -unrecognized
if %errorlevel% NEQ 4 echo test FAILED! Errorlevel =%errorlevel%
echo.

echo. & echo Testing -unrecognized and sourcefile & python hxa.py -unrecognized %tdir%test000.a
if %errorlevel% NEQ 4 echo test FAILED! Errorlevel =%errorlevel%
echo.

rem bad flag, partial overlap with real flag

echo. & echo Testing -hunrecognized only & python hxa.py -hunrecognized
if %errorlevel% NEQ 4 echo test FAILED! Errorlevel =%errorlevel%
echo.

echo. & echo Testing sourcefile and -hunrecognized & python hxa.py %tdir%test000.a -hunrecognized
if %errorlevel% NEQ 4 echo test FAILED! Errorlevel =%errorlevel%
echo.

echo. & echo Testing -hunrecognized and sourcefile & python hxa.py -hunrecognized %tdir%test000.a
if %errorlevel% NEQ 4 echo test FAILED! Errorlevel =%errorlevel%
echo.

rem '/' only

echo. & echo Testing / only & python hxa.py /
if %errorlevel% NEQ 4 echo test FAILED! Errorlevel =%errorlevel%
echo.

echo. & echo Testing sourcefile and / & python hxa.py %tdir%test000.a /
if %errorlevel% NEQ 4 echo test FAILED! Errorlevel =%errorlevel%
echo.

echo. & echo Testing / and sourcefile & python hxa.py / %tdir%test000.a
if %errorlevel% NEQ 4 echo test FAILED! Errorlevel =%errorlevel%
echo.

rem bad flag, '/' prefix

echo. & echo Testing /unrecognized only & python hxa.py /unrecognized
if %errorlevel% NEQ 4 echo test FAILED! Errorlevel =%errorlevel%
echo.

echo. & echo Testing sourcefile and /unrecognized & python hxa.py %tdir%test000.a /unrecognized
if %errorlevel% NEQ 4 echo test FAILED! Errorlevel =%errorlevel%
echo.

echo. & echo Testing /unrecognized and sourcefile & python hxa.py /unrecognized %tdir%test000.a
if %errorlevel% NEQ 4 echo test FAILED! Errorlevel =%errorlevel%
echo.

rem bad flag, partial overlap with real flag

echo. & echo Testing /?unrecognized only & python hxa.py /?unrecognized
if %errorlevel% NEQ 4 echo test FAILED! Errorlevel =%errorlevel%
echo.

echo. & echo Testing sourcefile and /?unrecognized & python hxa.py %tdir%test000.a /?unrecognized
if %errorlevel% NEQ 4 echo test FAILED! Errorlevel =%errorlevel%
echo.

echo. & echo Testing /?unrecognized and sourcefile & python hxa.py /?unrecognized %tdir%test000.a
if %errorlevel% NEQ 4 echo test FAILED! Errorlevel =%errorlevel%
echo.

rem '--' only

echo. & echo Testing -- only & python hxa.py --
if %errorlevel% NEQ 4 echo test FAILED! Errorlevel =%errorlevel%
echo.

echo. & echo Testing sourcefile and -- & python hxa.py %tdir%test000.a --
if %errorlevel% NEQ 4 echo test FAILED! Errorlevel =%errorlevel%
echo.

echo. & echo Testing -- and sourcefile & python hxa.py -- %tdir%test000.a
if %errorlevel% NEQ 4 echo test FAILED! Errorlevel =%errorlevel%
echo.

rem bad flag, '--' prefix

echo. & echo Testing --unrecognized only & python hxa.py --unrecognized
if %errorlevel% NEQ 4 echo test FAILED! Errorlevel =%errorlevel%
echo.

echo. & echo Testing sourcefile and --unrecognized & python hxa.py %tdir%test000.a --unrecognized
if %errorlevel% NEQ 4 echo test FAILED! Errorlevel =%errorlevel%
echo.

echo. & echo Testing --unrecognized and sourcefile & python hxa.py --unrecognized %tdir%test000.a
if %errorlevel% NEQ 4 echo test FAILED! Errorlevel =%errorlevel%
echo.

rem bad flag, partial overlap with real flag

echo. & echo Testing --helpunrecognized only & python hxa.py --helpunrecognized
if %errorlevel% NEQ 4 echo test FAILED! Errorlevel =%errorlevel%
echo.

echo. & echo Testing sourcefile and --helpunrecognized & python hxa.py %tdir%test000.a --helpunrecognized
if %errorlevel% NEQ 4 echo test FAILED! Errorlevel =%errorlevel%
echo.

echo. & echo Testing --helpunrecognized and sourcefile & python hxa.py --helpunrecognized %tdir%test000.a
if %errorlevel% NEQ 4 echo test FAILED! Errorlevel =%errorlevel%
echo.

set tdir=