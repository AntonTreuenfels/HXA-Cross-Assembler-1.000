@echo off
cls
echo I am in charge here (call me Al)

set tdir=test\

rem REGRESS limita [limitb]
rem - run regressions tests between limita and limitb

rem did we get only one number ?
if [%2] == [] goto onlyend

rem - make sure we have decimal number; watch out for octal !
set /a index = 1%1 - 1000
set /a end = 1%2 - 1000
goto begin

:onlyend
set /a index = 1
set /a end = 1%1 - 1000

:begin
echo running regressions from %index% to %end%
:While
if %index% gtr %end% goto EndWhile
   if %index% lss 1000 set num=%index%
   if %index% lss 100 set num=0%index%
   if %index% lss 10 set num=00%index%
   if not exist %tdir%test%num%.a if not exist %tdir%test%num%e.a goto nexttest
   echo. & echo Testing set test%num%*.a & python regress1.py %num%

:nexttest
   set /A index+=1
   goto While
:EndWhile
   set num=
   set index=
   set end=
   set tdir=
   echo Done!
