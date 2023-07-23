import os, sys, subprocess, traceback, webbrowser, shutil
from zipfile import ZipFile
from typing import Optional

def set_decision(user_input: str) -> bool:
    return True if user_input.lower() == 'y' else False

def if_group(dir_path: str) -> None:
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
        print(f"{dir_path} CREATED")
    else:
        print(f"{dir_path} FOUND")

def scan_assignments(incoming: str, destination_path: Optional[str]) -> None:
    global need_links
    if destination_path is None:
        destination_path = incoming.replace('(temp)', '')
    if_group(destination_path)
    for file in os.listdir(incoming):
        file_name = os.fsdecode(file)
        download_dir = os.path.join(incoming, file_name)
        student_dir = os.path.join(destination_path, file_name)
        if file_name.replace(' ', '').endswith(".html") and need_links:
            new_name = copy_links(download_dir, file_name, destination_path)
            if open_links:
                webbrowser.open_new(new_name) # Opens _gitLinks.html
                continue
        if is_filtered_file(file_name):
            print(f"Skipping File:\n{file_name}\n")
            continue
        if_group(student_dir)
        open_child(download_dir, student_dir, file_name)
    destroy_temp(incoming)

def copy_links(download_dir: str, file_name: str, destination_path: str) -> str:
    new_name = os.path.join(destination_path, f"{assignment_name}_gitLinks.html")
    print(f"\nCopying File:\n{file_name}\nTo: {new_name}")
    shutil.copy(download_dir, new_name)
    return new_name

def is_filtered_file(file_name: str) -> bool:
    filtered_extensions = ['.metadata', '_MACOSX', '.git', 'node_modules', '.DS_Store']
    for extension in filtered_extensions:
        if extension in file_name:
            return True
    return False

def open_child(input_location: str, student: str, file_name: str) -> None:
    for file in os.listdir(input_location):
        with ZipFile(os.path.join(input_location, file), 'r') as zObject:
            assignment_dir = zObject.namelist()[0].split('.')[0]
            if os.path.exists(os.path.join(student, assignment_dir)):
                print(f"Assignment {assignment_dir} already exists for {file_name}\n  Skipping file...\n")
                continue
            else:
                print(f"Extracting contents of:\n{file}\nTo: {student}\n")
                zObject.extractall(path=student)

def open_parent(input: str) -> str:
    trimmed_incoming = trim_filepath(input)
    destination_path = trimmed_incoming.replace('.zip', '(temp)').replace('&', '')
    if_group(destination_path)
    print()
    with ZipFile(trimmed_incoming, 'r') as zObject:
        zObject.extractall(path=destination_path)
    return destination_path

def destroy_temp(input: str) -> None:
    temp_parent = trim_filepath(input).replace('.zip', '(temp)').replace('&', '')
    if os.path.exists(temp_parent):
        shutil.rmtree(temp_parent)

def trim_filepath(input: Optional[str]) -> Optional[str]:
    if input is not None:
        return input.strip(' "')
    else:
        return input

def open_links(filepath: str) -> None:
    try:
        from bs4 import BeautifulSoup
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", 'beautifulsoup4'])
        from bs4 import BeautifulSoup
    with open(filepath) as fp:
        soup = BeautifulSoup(fp, features="html.parser")
    for link in soup.find_all('a'):
        link = link.get('href')
        print(f"...Opening {link}")
        webbrowser.open_new(link)
    print()

if __name__ == "__main__":
    need_links = set_decision(input("Include Git Repo Links File? (Y/yes, Any Key/no): "))
    open_links = set_decision(input("Open Git Repo Links? (Y/yes, Any Key/no): "))
    if need_links:
        assignment_name = input("Assignment Name or Alias: ")
    zipped_parent = input("FILE PATH to ZIPPED DOWNLOADED assignment directory (where is it?): \n")
    unzip_here = set_decision(input("Unzip Files in Current Directory? (Y/yes, Any Key/no): "))
    location_option = None if unzip_here else input("Please provide FILE PATH to destination directory (where is it going?): ")

    try:
        need_links = False
        scan_assignments(open_parent(zipped_parent), trim_filepath(location_option))
        destroy_temp(zipped_parent)
    except Exception as e:
        destroy_temp(zipped_parent)
        print(f"<<**ERROR**>>\n{e}")
        print("--------------------------------------------------")
        traceback.print_exc()
