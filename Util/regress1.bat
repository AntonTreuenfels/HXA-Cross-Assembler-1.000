@echo off
cls
echo I am in charge here (call me Al)

rem - run all tests in one set

set tdir=test\

rem - delete list and error files
for %%t in (%tdir%*.lst %tdir%*.err) do if exist %%t del %%t > nul
rem - delete binary and hex object files
for %%t in (%tdir%*.obj %tdir%*.raw %tdir%*.hex %tdir%*.s* %tdir%*.t* %tdir%*.u*) do if exist %%t del %%t > nul
rem - delete non-default filenames files
for %%t in (%tdir%my*.* %tdir%*.0*) do if exist %%t del %%t > nul
rem - run actual test set
echo. & echo Testing set test%1*.a & python regress1.py %1

set tdir=
