import os
import traceback
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
    file_name = os.fsdecode(file)
    download_dir = incoming+'\\'+file_name
    student_dir = destination_path+'\\'+file_name
    if file_name.replace(' ', '').endswith(".html"):
      new_name = f'{destination_path}\\{assignment_name}_gitLinks.html'
      print(f"\nCopying File: \n {file_name}\nTo: {new_name}")
      os.system(f"cp -rf '{download_dir}' '{new_name}'")
      open_links(new_name)
      continue
    if not os.path.exists(student_dir):
      os.mkdir(student_dir)
      print(f"\n{file_name} Directory CREATED")
    else:
      print(f"\n{file_name} Directory FOUND")
    for file in os.listdir(download_dir):
      with ZipFile(download_dir+"\\"+file, 'r') as zObject:
        assignment_dir = zObject.namelist()[0].split('.')[0]
        if os.path.exists(student_dir+"\\"+assignment_dir):
          print(f"Assignment {assignment_dir} alrady exists for {file_name}\n  Skipping this .zip file...\n")
          continue
        else:
          print(f"Extracting contents of: \n {file}\nTo: {student_dir}\n")
          zObject.extractall(path=student_dir)
  destroy_temp(incoming)

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

def open_links(filepath):
  import webbrowser
  try:
    from bs4 import BeautifulSoup
  except:
    import subprocess
    import sys
    subprocess.check_call([sys.executable, "-m", "pip", "install", 'beautifulsoup4'])
  from bs4 import BeautifulSoup
  with open(filepath) as fp:
    soup = BeautifulSoup(fp, features="html.parser")
  for link in soup.find_all('a'):
    link = link.get('href')
    print(f"Opening {link}...")
    webbrowser.open_new(link)

try:
  scan_assignments(open_parent(zipped_parent), trim_filepath(destination_path))
  destroy_temp(zipped_parent)
except Exception as e:
  destroy_temp(zipped_parent)
  print(f"<<**ERROR**>>\n{e}")
  print("--------------------------------------------------")
  traceback.print_exc()