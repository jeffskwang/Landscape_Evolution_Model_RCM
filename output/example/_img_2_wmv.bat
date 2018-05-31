C:\ffmpeg\bin\ffmpeg.exe -r 10 -f image2 -i "discharge_%%06d.png" -crf 1 -q:v 1 -s 960x720 -vcodec wmv2 _discharge.wmv
C:\ffmpeg\bin\ffmpeg.exe -r 10 -f image2 -i "elevation_%%06d.png" -crf 1 -q:v 1 -s 960x720 -vcodec wmv2 _elevation.wmv
PAUSE