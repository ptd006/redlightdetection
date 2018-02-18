# redlightdetection
A fun learning project to catch red light jumpers automatically.


Preprocessing with ffmpeg (cropping done manually for now):

```
ffmpeg -i 20180218_142849.mp4 -vf "transpose=2,crop=600:600:270:500,transpose=1" -an -r 20 -b:v 100K PreprocessedLights.mpg
ffmpeg -i PreprocessedLights.mpg -vf fps=10 snapshots/out%d.png

[... processing with Python and OpenCV creates output images ...]

ffmpeg -r 2 -f image2 -i snapshots/test/out%d.png -vcodec libx264 -crf 40 -pix_fmt yuv420p -vf "crop=150:150:250:0" test.mp4
```


