import os, shutil, time
import locale, platform
import subprocess
from subprocess import Popen

print ("AudioArchiver V0.2.0");
sys = platform.system()

if sys  == 'Windows':
  print("  running on windows system")
  
  locale.setlocale(locale.LC_TIME, 'deu_deu')

  basePath ="../../BeispielAufnahme/"
  ffmpegPath = "../ffmpeg/bin/ffmpeg.exe"
  
if sys == 'Linux':
  print("  running on Linux system")
  
  locale.setlocale(locale.LC_TIME, 'de_DE')

  basePath ="/media/pi/GODIARCHIV/"
  ffmpegPath = " "

print ("prepairing vars")

srcFile = basePath + "AHQU/USBREC/QU-ST001.WAV"
srcFileRename =  basePath + "AHQU/USBREC/" +  time.strftime("%d.%m.%Y") + ".WAV"
destPath = basePath +  "Gottesdienst_Archiv/" + time.strftime("%Y/%B/%d.%m.%Y/")
destFile = destPath + time.strftime("%d.%m.%Y") + ".mp3"


if not os.path.isdir(destPath):
  print ("creating directories")
  os.makedirs(destPath)


print ("normalize and convert to mp3")
print ("please wait")

cmd = ffmpegPath + " -i " + srcFile + " -vn -ar 44100 -ac 2 -filter:a loudnorm -ab 192k -f mp3 " + destFile
 
proc = Popen(cmd, shell=False)
proc.wait()

print ("done")



if os.path.isfile(destFile):
  print ("result will be found here: " + destFile)
  print ("rename src file to backup original")

  os.rename(srcFile, srcFileRename)
  print ("done")
else:
  print ("error output file was not found")     
