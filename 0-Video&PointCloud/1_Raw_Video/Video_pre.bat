@echo off
REM * Written by Iris Guo, Rutgers Civil RISE Group 9/5/2017
title Intro
color 0f
::##################################################################################


:Page One
cls 

::################# set vidoe name ###################################################
rem set "str1=1"    
rem   set "str2=.mp4"
del ../2_Clip_Video/*.mkv



set "str1=20170801_103007_20170801_103815"    
  set "str2=.mkv"
  set str3 =.mkv


  set "video_name_in=%str1%%str2%"
  rem set "str4=%str1% %str2%"
  rem set "str1=%str1% DOS %str2%"
  rem echo.%str3%
  rem echo.%str4%
  echo.Video Name:   %video_name_in%
  set "video_name=output.mp4"

.\ffmpeg -i %video_name_in% -codec copy %video_name%
:: ################### output video properties #######################################

set cmd=".\ffprobe.exe -v error -select_streams v:0 -show_entries stream=duration -of default=noprint_wrappers=1:nokey=1 %video_name%"
FOR /F "tokens=*" %%i IN (' %cmd% ') DO SET Video_Dur=%%i
echo.Video Duration: %Video_Dur%

set /a Clip_Min=%Video_Dur / 60
set /a Clip_Min = %Clip_Min + 1

echo.Video Minute Number: %Clip_Min%


set cmd=".\ffprobe.exe -v error -select_streams v:0 -show_entries stream=avg_frame_rate -of default=noprint_wrappers=1:nokey=1  %video_name%"
FOR /F "tokens=*" %%i IN (' %cmd% ') DO SET Video_FPS=%%i
echo.Video FPS: %Video_FPS%


set cmd=".\ffprobe.exe -v error -of flat=s=_ -select_streams v:0 -show_entries   stream=height -of default=noprint_wrappers=1:nokey=1 %video_name%"
FOR /F "tokens=*" %%i IN (' %cmd% ') DO SET Video_H=%%i
echo.Video Height: %Video_H%


set cmd=".\ffprobe.exe -v error -of flat=s=_ -select_streams v:0 -show_entries stream=width -of default=noprint_wrappers=1:nokey=1 %video_name%"
FOR /F "tokens=*" %%i IN (' %cmd% ') DO SET Video_W=%%i
echo.Video Width: %Video_W%


rem .\ffprobe.exe -v error -select_streams v:0 -show_entries stream=duration -of default=noprint_wrappers=1:nokey=1 %video_name%
rem .\ffprobe.exe -v error -select_streams v:0 -show_entries stream=avg_frame_rate -of default=noprint_wrappers=1:nokey=1 %video_name%
rem .\ffprobe.exe -v error -of flat=s=_ -select_streams v:0 -show_entries stream=height %video_name%
rem .\ffprobe.exe -v error -of flat=s=_ -select_streams v:0 -show_entries stream=width %video_name%


::################### clip video ####################################################
:: cut the entire video into pieces
    echo ############################################################################
	echo Total Time Duration for the current video is %Clip_Min%
	set "Time_start =0"
	set /a Time_start = %Time_start
	::######################### change Time_dur ######################################
	set /a Time_dur =  180 
	echo Set Clip Video Duration to %Time_dur% seconds
	::######################### change Time_dur ######################################
	set /a Clip_Num= %Video_Dur / 180 + 1
	echo.Clip Number: %Clip_Num%
	echo.Start Time: %Time_start%  


setlocal enabledelayedexpansion
set Time_start = 0
echo !Time_start!
set str3 =".mkv"

FOR /L %%G IN (1,1,%Clip_Num%) DO (
	echo Loop: %%G
	.\ffmpeg.exe -ss !Time_start! -i %video_name% -c copy -t %Time_dur% output_clip%%~nG.mkv
	set /a Time_start = %Time_dur% + !Time_start!
	echo !Time_start!

	)

::#################### Video un-distoration ################################

move output_clip*.mkv ../2_Clip_Video
del output.mp4

echo done
pause>nul