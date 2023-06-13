import os
import traceback
from datetime import datetime
from zipfile import ZipFile

zipped_parent = input("Please provide zipped assignments directory path: \n")
location_option = input("To unzip files into containing directory enter Y\n   *OR*\nPlease provide path to destination directory: ")
possible_input = ['y', '']
if location_option.lower() in possible_input:
  destination_path = None
else:
  destination_path = location_option
assignment_name = input("Rename git links.html file to be assignment specific(Anything You Want... Not A Path): ")

def if_group(dir_path):
  if not os.path.exists(dir_path):
    os.mkdir(dir_path)

def scan_assignments(incoming, destination_path):
  if destination_path == None:
    destination_path = incoming.replace('(temp)', '')
  if_group(destination_path)
  for file in os.listdir(incoming):
    student_name = os.fsdecode(file)
    download_dir = os.fsdecode(incoming)+'\\'+student_name
    student_dir = destination_path+student_name
    if student_name.replace(' ', '').endswith(".html"):
      print(f"{student_name} is not a directory or zipped file...")
      print(f"Copying File At:\n {download_dir}\nTo: {destination_path}\n")
      os.system(f"cp -rf '{download_dir}' '{destination_path}{assignment_name} gitLinks {datetime.now().strftime('%d-%m-%Y %I:%M')}.html'")
      continue
    if not os.path.exists(student_dir):
      os.mkdir(student_dir)
      print(f"{student_name} Assignemnt Directory CREATED")
    for file in os.listdir(download_dir):
      print(f"UnZipping contents at: \n {download_dir+file}\nTo: {student_dir}\n")
      with ZipFile(download_dir+"\\"+file, 'r') as zObject:
        zObject.extractall(path=student_dir)

def open_parent(input):
  print("Extracting Parent Directory...")
  trimmed_incoming = trim_filepath(input)
  destination_path = trimmed_incoming.replace('.zip', '(temp)').replace('&', '')
  if_group(destination_path)
  with ZipFile(trimmed_incoming, 'r') as zObject:
    zObject.extractall(path= destination_path)
  return destination_path

def destroy_temp(input):
  temp_parent = trim_filepath(input).replace('.zip', '(temp)').replace('&', '')
  if os.path.exists(temp_parent):
    os.system(f"rm -rf '{temp_parent}'")

def trim_filepath(input):
  if input != None:
    return input.strip(' "')
  else:
    return input

try:
  scan_assignments(open_parent(zipped_parent), trim_filepath(destination_path))
  destroy_temp(zipped_parent)
except Exception as e:
  destroy_temp(zipped_parent)
  print(f"<<**ERROR**>>\n{e}")
  print("--------------------------------------------------")
  traceback.print_exc()




