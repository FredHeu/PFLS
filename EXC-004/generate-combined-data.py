# setup
import os, shutil
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
   with open('./EXC-004/RAW-DATA/sample-translation.txt', 'r') as f:
      for line in f.readlines():
         if directory in line:
            sample_translation = line.split()
            xxx = sample_translation[1]

# copy unbined to combined dir:
   shutil.copy(DNA_path + '/bin-unbinned.fasta', destination + '/' + xxx + '_UNBINNED.fa')


# assess yyy - therefore: extract bin# from file name -> search from checkm.txt

   # returns xxx_and_name for each FASTA
#   with os.scandir(DNA_path) as it:
#      for entry in it:
#         if not entry.name.startswith('.') and entry.is_file():
#            print(xxx + '_' + entry.name)