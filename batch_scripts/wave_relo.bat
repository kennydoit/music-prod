@echo off
:: This script moves all .wav files from a source directory to a destination directory

echo Starting file transfer...
echo From: C:\Users\Kenrm\Documents\Splice
echo To: G:\02_FL Data\Patches\Packs\Vocals
echo.


:: Move all .wav files, including those in subfolders
for /r "C:\Users\Kenrm\Documents\Splice" %%f in (*.wav) do (
    echo Moving: "%%f"
    move "%%f" "G:\02_FL Data\Patches\Packs\Vocals"
)

echo.
echo File transfer complete
pause