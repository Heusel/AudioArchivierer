import os, shutil, time
import locale, platform
from subprocess import Popen
import sys
import copyData
import argparse
import glob 


class AudioArchiver():
  def __init__(self, check=False):
    
    self.version = "V0.5.2"
    
    print("AudioArchiver: " + self.version)
    print("Suche Dateien")
    time.sleep(5)
    sys = platform.system()

    if sys  == 'Windows':
      print("  SW läuft auf einem  Windows Rechner")
      
      locale.setlocale(locale.LC_TIME, 'deu_deu')
      
      # basePath = "../../BeispielAufnahme/"
      basePath = "m:/"
      self.searchPath = basePath + "AHQU/USBREC//QU-ST*.WAV"
      self.ffmpegPath = "C:/ffmpeg-20171218-74f408c-win64-static/bin/ffmpeg.exe"
      
    if sys == 'Linux':
      print("  SW läuft auf einem Linux Rechner ")
      
      locale.setlocale(locale.LC_TIME, 'de_DE')

      basePath ="/media/pi/GODIARCHIV/"
      self.ffmpegPath = "ffmpeg"


    self.srcFile = self.searchForInputFile () #basePath + "AHQU/USBREC/QU-ST001.WAV"
    #self.srcFileRename =  basePath + "AHQU/USBREC/" +  time.strftime("%Y_%m_%d") + ".WAV"    
    self.srcFileRename =  basePath + "backup_Aufnahmen/" +  time.strftime("%Y_%m_%d") + ".WAV"



    self.destPath = basePath +  "Gottesdienst_Archiv/" + time.strftime("%Y/%B/")
    self.destFile = self.destPath + time.strftime("Gottesdienst_%d_%m_%Y") + ".mp3"
    self.dateStr = time.strftime("%d.%m.%Y")

	
    if not os.path.isdir(self.destPath):
      print ("Anlegen des Ablageverzeichnis")
      os.makedirs(self.destPath)


    if check == True:
      if not os.path.isfile(self.srcFile):
        raise NameError("Aufnahme Datei "+ self.srcFile + " wurde nicht gefunden")    

  def searchForInputFile(self):
    print("  suche nach Aufnahmedateien")
    files = glob.glob(self.searchPath)
    #print (files)
    NumFiles = len(files)

    n = ""

    print ("  " + str(NumFiles) + " Dateien gefunden")
  
    if NumFiles != 0:
      n = files[0]
      for f in files:
        print (f)
        if f > n:
          n=f

      print ("  " + n + " ausgewählt")

    return  (n)

  def checkOutputFile(self):  
    print("  Überprüfe Ablagedatei um ein überschreiben der Aufnahmen zu verhindern")
    checkFilename =  self.basePath + "AHQU/USBREC/" +  self.myTime.strftime("%d_%m_%Y") + ".WAV"
    
    fCnt = 0

    while (os.path.isfile(checkFilename)):
        fCnt = fCnt + 1
        checkFilename =  self.basePath + "AHQU/USBREC/" +  self.myTime.strftime("%d_%m_%Y") +"_"+ str(fCnt) + ".WAV"

    print ("  " + checkFilename )

    return fCnt

  def normalize(self):

    if not os.path.isfile(self.srcFile):
      raise NameError("Aunfnahmedatei "+ self.srcFile + " nicht gefunden")

    meta =  '-metadata title="Gottesdienst vom ' + self.dateStr + '" -metadata album="Martinskirche Oeschingen" -metadata copyright="Evangelische Kirchengemeinde Oeschingen"'
    cmd = self.ffmpegPath + " -i " + self.srcFile + " -vn -ar 44100 -ac 2 " + meta + " -filter:a loudnorm=I=-23:LRA=1 -ab 160k -f mp3 " + self.destFile
     
    proc = Popen(cmd, shell=False)
    proc.wait()
    
    if not os.path.isfile(self.destFile):
      raise NameError("Ablagedatei  " + self.destFile +" nicht gefunden") 

  def archiveSrc(self):
   os.rename(self.srcFile, self.srcFileRename)
   

  def copyToSticks(self):
    copyData.do(self.destFile)  

def main():
  try:
  
    parser = argparse.ArgumentParser()
    parser.add_argument("--NoCreation", help="no mp3 creation. only copying files to sticks", action="store_true")
    parser.add_argument("--NotCopy", help="not copy the converted mp3 file to sticks", action="store_true") 
    args = parser.parse_args()
    
    #print ("Anlegen der Variablen")

    audioArchiver = AudioArchiver()

    
    if not args.NoCreation:
        print ("Normalisien und nach mp3 konvertieren")
        print ("Bitte warten")
        audioArchiver.normalize()
        print ("erledigt")

        print ("Ergebnis liegt unter: " + audioArchiver.destFile)
        print ("umbennen der Quell-Datei (Backup original)")
        audioArchiver.archiveSrc()
        print ("erledigt")
    
    if not args.NotCopy:
        print (audioArchiver.destFile + " auf alle gefunden USB-Stickes kopieren")
        audioArchiver.copyToSticks()
        print ("erledigt")
        #print("Bitte irgendeine Taste drücken")
        os.system("pause")
	
  except Exception as e:
    print("Hoppla!  ", e)
    #print("Bitte irgendeine Taste drücken")
    os.system("pause")
    exit(1)


if __name__ == "__main__":
    main()
