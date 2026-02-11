# setup
import os, shutil, re

path = "./EXC-004/RAW-DATA"
destination = "./EXC-004/COMBINED-DATA"
# create directory or remove contents
try:
   os.mkdir('./EXC-004/COMBINED-DATA')
except FileExistsError:
   filelist = [f for f in os.listdir('./EXC-004/COMBINED-DATA')]
   for f in filelist:
      os.remove(os.path.join('./EXC-004/COMBINED-DATA', f))

# creates list with names of Directorys: [DNA57, DNA64, ...] 
dir_list = []
with os.scandir(path) as it:
    for entry in it:
        if not entry.name.startswith('.') and entry.is_dir():
            dir_list.append(entry.name)

# extracts ID from sample-translation -> stored in xxx
for directory in dir_list:
   DNA_path = path + "/" + directory + "/bins"
   zMAG = 1
   zBIN = 1   
   with open('./EXC-004/RAW-DATA/sample-translation.txt', 'r') as f:
      for line in f.readlines():
         if directory in line:
            sample_translation = line.split()
            xxx = sample_translation[1]

# copy unbinned to combined dir:
   shutil.copy(DNA_path + '/bin-unbinned.fasta', destination + '/' + xxx + '_UNBINNED.fa')


# assess yyy - therefore: extract bin# from file name -> search from checkm.txt
# while at it, iterate seperatly for zzz, copy and rename files into output folder

   filelist = [f for f in os.listdir('./EXC-004/RAW-DATA/' + directory + '/bins')]
   for file in filelist:
      if not file.startswith('.') and not file == "bin-unbinned.fasta":
         yyybin = file.rstrip('.fasta')
         with open('./EXC-004/RAW-DATA/' + directory + '/checkm.txt', 'r') as f:
            for line in f.readlines():
               if yyybin in line:
                  checkm = line.split()
                  compl = float(checkm[12])
                  conta = float(checkm[13])
                  if compl > 50 and conta < 5:
                     yyy = "MAG"
                     zzzMAG = str(zMAG).zfill(3)
                     zMAG += 1
                     shutil.copy(DNA_path + '/' + file, destination + '/' + xxx + '_' + yyy + '_' + zzzMAG + '.fa')
                  else:
                     yyy = "BIN"
                     zzzBIN = str(zBIN).zfill(3)
                     zBIN += 1
                     shutil.copy(DNA_path + '/' + file, destination + '/' + xxx + '_' + yyy + '_' + zzzBIN + '.fa')


# Tasks remaining:
#  Manipulate Defline with xxx
#  copy and rename checkm.txt and gtdb file