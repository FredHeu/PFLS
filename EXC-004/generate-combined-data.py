# setup
import os, shutil, re

path = os.path.join('RAW-DATA')
destination = os.path.join('COMBINED-DATA')
# create directory or remove contents
try:
   os.mkdir(destination)
except FileExistsError:
   filelist = [f for f in os.listdir(destination)]
   for f in filelist:
      os.remove(os.path.join(destination, f))

# creates list with names of Directorys: [DNA57, DNA64, ...] 
dir_list = []
with os.scandir(path) as it:
    for entry in it:
        if not entry.name.startswith('.') and entry.is_dir():
            dir_list.append(entry.name)

# extracts ID from sample-translation -> stored in xxx
for directory in dir_list:
   DNA_path = os.path.join(path, directory, 'bins')
   zMAG = 1
   zBIN = 1   
   with open(os.path.join(path,'sample-translation.txt'), 'r') as f:
      for line in f.readlines():
         if directory in line:
            sample_translation = line.split()
            xxx = sample_translation[1]

# copy unbinned/checkm/gtdb files to combined dir:
   shutil.copy(os.path.join(DNA_path, 'bin-unbinned.fasta'), os.path.join(destination, str(xxx + '_UNBINNED.fa')))
   sup_file_path = os.path.join(path, directory)
   shutil.copy(os.path.join(sup_file_path, 'checkm.txt'), os.path.join(destination, str(xxx + '-CHECKM.txt')))
   shutil.copy(os.path.join(sup_file_path, 'gtdb.gtdbtk.tax'), os.path.join(destination, str(xxx + '-GTDB-TAX.txt')))

# assess yyy - therefore: extract bin# from file name -> search from checkm.txt
# while at it, iterate seperatly for zzz, copy and rename files into output folder

   filelist = [f for f in os.listdir(os.path.join(path, directory, 'bins'))]
   for file in filelist:
      if not file.startswith('.') and not file == "bin-unbinned.fasta":
         yyybin = file.rstrip('.fasta')
         with open(os.path.join(path, directory, 'checkm.txt'), 'r') as f:
            for line in f.readlines():
               if yyybin in line:
                  checkm = line.split()
                  compl = float(checkm[12])
                  conta = float(checkm[13])
                  if compl > 50 and conta < 5:
                     yyy = "MAG"
                     zzzMAG = str(zMAG).zfill(3)
                     zMAG += 1
                     shutil.copy(os.path.join(DNA_path, file), os.path.join(destination, str(xxx + '_' + yyy + '_' + zzzMAG + '.fa')))
                  else:
                     yyy = "BIN"
                     zzzBIN = str(zBIN).zfill(3)
                     zBIN += 1
                     shutil.copy(os.path.join(DNA_path, file), os.path.join(destination, str(xxx + '_' + yyy + '_' + zzzBIN + '.fa')))

# add ID to defline in copied fasta
filelist = [f for f in os.listdir(destination)]
for file in filelist:
   if file.endswith('.fa'):
      xxx = file.split('_')
      xxx = xxx[0]
      with open(os.path.join(destination, file)) as input_file:
         with open(os.path.join(destination, str(file + '.new')), 'w') as output_file:
            for line in input_file:
               if '>' in line:
                  new_line = line.lstrip('>')
                  new_line = ">" + xxx + ";" + new_line
                  output_file.write(new_line)
               else:
                  output_file.write(line)
      os.rename(os.path.join(destination, str(file + '.new')), os.path.join(destination, file))
