import os, shutil, time
import locale, platform

print ("AudioArchiver V0.0.1");

sys = platform.system()

if sys  == 'Windows':
  locale.setlocale(locale.LC_TIME, 'deu_deu')
  basePath ="C:/Users/Johannes/Documents/GitHub/AudioArchivierer/BeispielAufnahme/"
  print("  running on windows system")  

srcPath  = basePath + "AHQU/USBREC/"
destPath = basePath +  "Gottesdienst_Archiv/" + time.strftime("%Y/%B/%d.%m.%Y/")

if not os.path.isdir(destPath):
  os.makedirs(destPath)

 

files = os.listdir(srcPath)
files.sort()

for f in files:
    src = srcPath+f
    dst = destPath+f
    shutil.move(src,dst)
    print ("Kopiere " + f + " nach " + destPath)




