import os, sys, subprocess, traceback, webbrowser
from zipfile import ZipFile

assignment_name = input("Assignment Name or Alias: ")
zipped_parent = input("Zipped Download-File Path: \n")
#done todo change cohort name input to a filepath 
#done give option to unzip to default location(containing folder)
#done Rename git links.html file to be assignment specific
# # ? are incoming filepath structured differently per os?
# # ? utilize try catch for bad file path errors
location_option = input("To unzip files into containing directory enter Y\n   *OR*\nPlease provide path to destination directory: ")
possible_input = ['nothing', 'none','y', '']
if location_option.lower() in possible_input:
  destination_path = None
else:
  destination_path = location_option

def if_group(dir_path):
  if not os.path.exists(dir_path):
    os.mkdir(dir_path)
    print(f"{dir_path} CREATED")
  else:
    print(f"{dir_path} FOUND")

def scan_assignments(incoming, destination_path):
  #A If destination_path == None unzip into current dir else extract to destination_path path
  if destination_path == None:
    destination_path = incoming.replace('(temp)', '')
  if_group(destination_path)
  for file in os.listdir(incoming):
    file_name = os.fsdecode(file)
    download_dir = incoming+'\\'+file_name
    student_dir = destination_path+'\\'+file_name
    # # todo Check for .metadata, _MACOSX, .git, node_modules
    # # ? what other files for other stacks can be filtered out
    if file_name.replace(' ', '').endswith(".html"):
      new_name = f'{destination_path}\\{assignment_name}_gitLinks.html'
      print(f"\nCopying File: \n {file_name}\nTo: {new_name}")
      # done timestamp can be simplified... or create some simpler identifier
      # ? Posssible system dependent command
      os.system(f"cp -rf '{download_dir}' '{new_name}'")
      open_links(new_name)
      continue
    if_group(student_dir)
    print()
    open_child(download_dir, student_dir, file_name)
  destroy_temp(incoming)


def open_child(input_location, student, file_name):
  # todo try catch for ZipFile errors
  # ? file presence, position, duplicate file names etc
  for file in os.listdir(input_location):
    with ZipFile(input_location+"\\"+file, 'r') as zObject:
      assignment_dir = zObject.namelist()[0].split('.')[0]
      # print(assignment_dir)
      # done IF assignment already exists, skip it
      if os.path.exists(student+"\\"+assignment_dir):
        print(f"Assignment {assignment_dir} alrady exists for {file_name}\n  Skipping file...\n")
        continue
      else:
        print(f"Extracting contents of: \n {file}\nTo: {student}\n")
        zObject.extractall(path=student)

def open_parent(input):
  # print("Extracting Parent Directory")
  trimmed_incoming = trim_filepath(input)
  destination_path = trimmed_incoming.replace('.zip', '(temp)').replace('&', '')
  # ? are there any other assignemnt names with problematic characters
  if_group(destination_path)
  print()
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
  
# # done Open git links directly into the browser
# #A webbrowser.open_new() could work if the links can be accessesed as strings
# # ? if so could they still be packaged up with the downloaded zip in a student named file?
def open_links(filepath):
  try:
    from bs4 import BeautifulSoup
  except:
    #? Possible system dependent command
    subprocess.check_call([sys.executable, "-m", "pip", "install", 'beautifulsoup4'])
    from bs4 import BeautifulSoup
  with open(filepath) as fp:
    soup = BeautifulSoup(fp, features="html.parser")
  for link in soup.find_all('a'):
    link = link.get('href')
    print(f"...Opening {link}")
    webbrowser.open_new(link)
  print()

# todo Check for projects *not in a parent directory *in nested parent directory
#!? Does os.system() bash commands require git bash be installed for windows systems?

# <Identifying terminal type to use custom commands
  # print(os.ctermid()) #didnt work
  # print(os.uname()) #didnt work
  #> Below prints the system identifier windows:'win32', macos:'darwin', linux:'linux'
  # import sys
  # print(sys.platform)
# > Below to use as condition
  # if sys.platform.startswith('linux'):

try:
  scan_assignments(open_parent(zipped_parent), trim_filepath(destination_path))
  destroy_temp(zipped_parent)
except Exception as e:
  destroy_temp(zipped_parent)
  print(f"<<**ERROR**>>\n{e}")
  print("--------------------------------------------------")
  traceback.print_exc()