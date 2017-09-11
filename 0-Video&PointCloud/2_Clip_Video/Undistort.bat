
@echo off
REM * Written by Iris Guo, Rutgers Civil RISE Group 9/5/2017
title Intro
color 0f
::##################################################################################

:Page One
cls 

echo -----This program will loop all the mkv video files in the same folder----
echo -----Process Start Now----------------------------------------
echo.
for  %%A in (output*.mkv) Do (echo Path Name: %%~nA   & undistort_mjpeg_arg.py -i %%~nA.mkv )



echo done
pause >nul
