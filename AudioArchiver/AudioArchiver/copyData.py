import psutil, os, shutil, threading, queue

import sys


class FileCopy(threading.Thread):
    def __init__(self, queue, files, dirs):
        threading.Thread.__init__(self)
        self.queue = queue
        self.files = list(files)  # copy list
        self.dirs = list(dirs)    # copy list
        for f in files:
            if not os.path.exists(f):
                raise ValueError('%s does not exist' % f)
        for d in dirs:
            if not os.path.isdir(d):
                raise ValueError('%s is not a directory' % d)

    def run(self):
        # This puts one object into the queue for each file,
        # plus a None to indicate completion
        try:
            for f in self.files:
                try:
                    for d in self.dirs:
                        shutil.copy(f, d)
                except IOError as e:
                    self.queue.put(e)
                else:
                    self.queue.put(f)
        finally:
            self.queue.put(None)  # signal completion


class FileDelete(threading.Thread):
    def __init__(self, queue, files, dirs):
        threading.Thread.__init__(self)
        self.queue = queue
        self.files = list(files)  # copy list
        self.dirs = list(dirs)    # copy list

        for d in dirs:
            if not os.path.isdir(d):
                raise ValueError('%s is not a directory' % d)

    def run(self):
        # This puts one object into the queue for each file,
        # plus a None to indicate completion
        try:
            for f in self.files:
                try:
                    for d in self.dirs:
                        
                        flist = os.listdir(d)
                        delfiles = [i for i in flist if i.endswith(f)]
                        for df in delfiles:
                            print(d + df)
                            os.remove(d + df )
                except IOError as e:
                    self.queue.put(e)
                else:
                    self.queue.put(f)
        finally:
            self.queue.put(None)  # signal completion


def do(arg1):
    # do whatever the script does

    #print ('Argument :' + arg1)
	
	
    if not os.path.exists(arg1):
        raise ValueError('Datei %s wurde nicht gefunden' % arg1)

    partList = psutil.disk_partitions()

    mountList = [];
     
    for partition in partList:
        #print(partition)
        if partition.opts=='rw,removable':
            mountList.append(partition.mountpoint)

    print( str(len(mountList)) + ' USB sticks gefunden:')
    
    if len(mountList) == 0:      
      raise NameError("keine USB-Sticks gefunden")     

    #for usbDevice in mountList:
    #    print('   ' + str(usbDevice))


    q = queue.Queue()
    files = []
    files.append(arg1)
    delFiles = ['.mp3']
    
    delthread = FileDelete(q, delFiles, mountList)
    print('Lösche alte mp3 Dateien auf den USB-Sticks')
    print('Das kann etwas dauern! Bitte warten')
    delthread.start()
    while True:
        x = q.get()
        if x is None:
            break
        print(x)
    delthread.join()


    q = queue.Queue()
    copythread = FileCopy(q, files, mountList)
    print('Beginne mit den kopieren der mp3-Datei aud USB-Sticks')
    print('Das kann etwas dauern! Bitte warten')
    copythread.start()
    while True:
        x = q.get()
        if x is None:
            break
        print(x)
    copythread.join()


if __name__ == "__main__":
    do("M:/Gottesdienst_Archiv/2018/Januar/Gottesdienst_03_01_2018.mp3")
