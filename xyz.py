import os
from datetime import datetime
from zipfile import ZipFile

zipped_parent = input("Zipped Downloaded Assignments Directory Path:\n")
cohort_name = input("Enter Desired Destination Cohort Directory Name:\n")
assignment_name = input("Assignment Name (Anything You Want... Not A Path):")
cohort_path = f'C:/Users/theau/Dojo/cohorts/{cohort_name}/'

def ifCohort(dir_path):
  if not os.path.exists(dir_path):
    os.mkdir(dir_path)
    print("Created Cohort Directory " , dir_path)
  else:    
    print("Cohort Directory " , dir_path ,  " already exists. Skipping task...")

def scan_incoming(incoming, cohort):
  for file in os.listdir(incoming):
    student_name = os.fsdecode(file)
    download_dir = os.fsdecode(incoming)+'\\'+student_name
    student_dir = cohort+student_name
    if student_name.replace(' ', '').endswith(".html"):
      print(f"{student_name} is not a directory or zipped file...")
      print(f"Copying File At:\n {download_dir}\nTo: {cohort}\n")
      os.system(f"cp -rf '{download_dir}' '{cohort}{assignment_name} gitLinks {datetime.now().strftime('%d-%m-%Y %I:%M')}.html'")
      continue
    if not os.path.exists(student_dir):
      os.mkdir(student_dir)
      print(f"{student_name} Assignemnt Directory CREATED")
    for file in os.listdir(download_dir):
      print(f"UnZipping contents at: \n {download_dir+file}\nTo: {student_dir}\n")
      with ZipFile(download_dir+"\\"+file, 'r') as zObject:
        zObject.extractall(path=student_dir)

def open_parent(incoming):
  print("Extracting Parent Directory")
  trimmed_incoming = None
  if incoming[0] == '"' and incoming[len(incoming)-1] == '"':
    trimmed_incoming = incoming[1:len(incoming)-1]
  else:
    trimmed_incoming = incoming
  destination_path = trimmed_incoming.replace('.zip', '').replace('&', '')
  with ZipFile(trimmed_incoming, 'r') as zObject:
    zObject.extractall(path= destination_path)
  return destination_path

def trim_filepath(input):
  if input != None:
    return input.strip(' "')
  else:
    return input

ifCohort(cohort_path)
scan_incoming(open_parent(zipped_parent), cohort_path)




