import os, shutil, time
import locale, platform
from subprocess import Popen
import sys
import copyData
import argparse

class AudioArchiver():
  def __init__(self, check=False):
    sys = platform.system()

    if sys  == 'Windows':
      print("  running on windows system")
      
      locale.setlocale(locale.LC_TIME, 'deu_deu')
      
      # basePath = "../../BeispielAufnahme/"
      basePath = "f:/"
      self.ffmpegPath = "../ffmpeg/bin/ffmpeg.exe"
      
    if sys == 'Linux':
      print("  running on Linux system")
      
      locale.setlocale(locale.LC_TIME, 'de_DE')

      basePath ="/media/pi/GODIARCHIV/"
      self.ffmpegPath = "ffmpeg"

    self.srcFile = basePath + "AHQU/USBREC/QU-ST001.WAV"
    self.srcFileRename =  basePath + "AHQU/USBREC/" +  time.strftime("%d_%m_%Y") + ".WAV"
    self.destPath = basePath +  "Gottesdienst_Archiv/" + time.strftime("%Y/%B/")
    self.destFile = self.destPath + time.strftime("Gottesdienst_%d_%m_%Y") + ".mp3"
    self.dateStr = time.strftime("%d.%m.%Y")

    if not os.path.isdir(self.destPath):
      print ("creating directories")
      os.makedirs(self.destPath)


    if check == True:
      if not os.path.isfile(self.srcFile):
        raise NameError("Input file "+ self.srcFile + " was not found")    

  def normalize(self):

    if not os.path.isfile(self.srcFile):
      raise NameError("Input file "+ self.srcFile + " was not found")

    meta =  '-metadata title="Gottesdienst vom ' + self.dateStr + '" -metadata album="Martinskirche Oeschingen" -metadata copyright="Evangelische Kirchengemeinde Oeschingen"'
    cmd = self.ffmpegPath + " -i " + self.srcFile + " -vn -ar 44100 -ac 2 " + meta + " -filter:a loudnorm=I=-23:LRA=1 -ab 160k -f mp3 " + self.destFile
     
    proc = Popen(cmd, shell=False)
    proc.wait()
    
    if not os.path.isfile(self.destFile):
      raise NameError("Output file " + self.destFile +" was not found") 

  def archiveSrc(self):
   os.rename(self.srcFile, self.srcFileRename)

  def copyToSticks(self):
    copyData.do(self.destFile)  

def main():
  try:
    print ("AudioArchiver V0.3.0");

    parser = argparse.ArgumentParser()
    parser.add_argument("--NoCreation", help="no mp3 creation. only copying files to sticks", action="store_true")
    parser.add_argument("--NotCopy", help="not copy the converted mp3 file to sticks", action="store_true") 
    args = parser.parse_args()
    
    print ("prepairing vars")
    audioArchiver = AudioArchiver()

    if not args.NoCreation:
        print ("normalize and convert to mp3")
        print ("please wait")
        audioArchiver.normalize()
        print ("done")

        print ("result will be found here: " + audioArchiver.destFile)
        print ("rename src file to backup original")
        audioArchiver.archiveSrc()
        print ("done")
    
    if not args.NotCopy:
        print ("copy result to all found memory sticks")
        audioArchiver.copyToSticks()
        print ("done")
   
  except Exception as e:
    print("Oops!  ", e)
    exit(1)


if __name__ == "__main__":
    main()