@echo off
cls
echo I am in charge here (call me Al)

rem - run all tests in one set

set tdir=demo\

rem - delete list and error files
for %%t in (%tdir%*.lst %tdir%*.err) do if exist %%t del %%t > nul
rem - delete binary and hex object files
for %%t in (%tdir%*.obj %tdir%*.raw %tdir%*.hex %tdir%*.s* %tdir%*.t* %tdir%*.u*) do if exist %%t del %%t > nul
rem - delete non-default filenames files
for %%t in (%tdir%my*.* %tdir%*.0*) do if exist %%t del %%t > nul
rem - run actual test set
for %%t in (%tdir%demo_%1*.a) do echo. & echo Testing %%t & python hxa.py -hxa_t %%t

set tdir=
