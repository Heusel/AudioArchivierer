import os, shutil, time
import locale, platform
import subprocess
from subprocess import Popen
import sys

print ("AudioArchiver V0.2.0");
sys = platform.system()

if sys  == 'Windows':
  print("  running on windows system")
  
  locale.setlocale(locale.LC_TIME, 'deu_deu')
  
  # basePath = "../../BeispielAufnahme/"
  basePath = "f:\\"
  ffmpegPath = "../ffmpeg/bin/ffmpeg.exe"
  
if sys == 'Linux':
  print("  running on Linux system")
  
  locale.setlocale(locale.LC_TIME, 'de_DE')

  basePath ="/media/pi/GODIARCHIV/"
  ffmpegPath = "ffmpeg"


print ("prepairing vars")

srcFile = basePath + "AHQU/USBREC/QU-ST001.WAV"
srcFileRename =  basePath + "AHQU/USBREC/" +  time.strftime("%d_%m_%Y") + ".WAV"
destPath = basePath +  "Gottesdienst_Archiv/" + time.strftime("%Y/%B/")
destFile = destPath + time.strftime("Gottesdienst_%d_%m_%Y") + ".mp3"


if not os.path.isdir(destPath):
  print ("creating directories")
  os.makedirs(destPath)

  
if not os.path.isfile(srcFile):
    print("error input file was not found")
    exit(1)

print ("normalize and convert to mp3")
print ("please wait")
meta =  '-metadata title="' + time.strftime("Gottesdienst vom %d.%m.%Y") + '" -metadata album="Martinskirche Oeschingen" -metadata copyright="Evangelische Kirchengemeinde Oeschingen"'
cmd = ffmpegPath + " -i " + srcFile + " -vn -ar 44100 -ac 2 " + meta + " -filter:a loudnorm -ab 160k -f mp3 " + destFile
 
proc = Popen(cmd, shell=False)
proc.wait()

print ("done")



if os.path.isfile(destFile):
  print ("result will be found here: " + destFile)
  print ("rename src file to backup original")

  os.rename(srcFile, srcFileRename)
  print ("done")
  exit(0)
else:
  print ("error output file was not found")     
  exit(2)
