import os
from shutil import move, unpack_archive
from pathlib import Path
from time import time, sleep
import concurrent.futures


        
def find_files(path): 

    files_path = []
    for root, dirs, files in os.walk(path):
        for f in files:
            
            if not root.endswith('archives'):
                path_to_file = Path(root) / f
                files_path.append(path_to_file)
    
    files_path = normalize(files_path)
    return files_path

def sort_files(file, path):

    if file.suffix in FILES_EXTENSION['images']:  
        move_file(file, folder= 'images', path=path)

    elif file.suffix in FILES_EXTENSION['documents']:
        move_file(file, folder= 'documents', path=path)
    
    elif file.suffix in FILES_EXTENSION['audio']:
        move_file(file, folder= 'audio', path=path)

    elif file.suffix in FILES_EXTENSION['video']:
        move_file(file, folder= 'video', path=path)
    
    elif file.suffix in FILES_EXTENSION['archives']:
        path_to_archives = Path(path) / 'archives'
        unpack_archive(file, path_to_archives)
        os.remove(file)
    
    else:
        move_file(file, folder= 'others', path=path)


def create_folder(path):
    
    if not os.path.exists(path):
        os.mkdir(path)

def delete_empty_folders(root):
   for dirpath, dirnames, filenames in os.walk(root, topdown=False):
      for dirname in dirnames:
         full_path = os.path.join(dirpath, dirname)
         if not os.listdir(full_path): 
            os.rmdir(full_path)

def move_file(file, folder, path):
    new_folder = Path(path) / folder
    new_path_to_file = Path(new_folder) / file.name
    create_folder(new_folder)
    move(file, new_path_to_file)

def normalize(files_path):
    CYRILLIC_SYMBOLS = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ"
    TRANSLATION = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
               "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "ya", "je", "i", "ji", "g")
    TRANS = {}
    normalize_files = []
    for c, l in zip(CYRILLIC_SYMBOLS, TRANSLATION):
        TRANS[ord(c)] = l
        TRANS[ord(c.upper())] = l.upper()
    
    def inner(file):
        
        file_name = file.name
        new_name = file_name.translate(TRANS)
        path_to_file = os.path.dirname(file)
        
        for char in new_name:
            if char not in '1234567890qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM.':
                new_name = new_name.replace(char, '_')
            
        new_name_path = Path(path_to_file) / new_name
        os.rename(file, new_name_path)
        
        new_file = Path(f'{path_to_file}\{new_name}')
        return new_file

    with concurrent.futures.ThreadPoolExecutor() as executor:
        normalize_files.extend(list(executor.map(inner, files_path)))
    
    return normalize_files
    

def woker(path):
    start = time()
    find_time = time()
    files_path = find_files(path)
    print('find_files =', time() - find_time)
    sort_files_time = time()
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(lambda f: sort_files(f, path), files_path)
    print( 'sort_files_time =', time() - sort_files_time)
    delete_time = time()
    delete_empty_folders(path)
    print('delete_time =', time()- delete_time)
    print('main_time =', time() - start)

def main():

    while True:
        input_ = input('(close, exit)\nEnter path: ')
        input_ = input_.strip().casefold()
        
        if input_ in ['exit', 'close']:
            print('bye')
            break

        woker(input_)
    
    

FILES_EXTENSION = {
    'images' : ['.png', '.png', '.png', '.jpeg', '.jpg', '.svg'],
    'documents' : [".doc", ".docx", ".txt", ".pdf", ".xlsx", ".xls", ".pptx", ".cad", ".dwg", ".odg", ".odt", ".html", ".url"],
    'audio' : [".mp3", ".ogg", ".wav", ".amr"],
    'archives': [".zip", ".gz", ".tar", '.rar', '.7z', '.tgz', '.iso', '.jar', '.bz2'],
    'video': [".avi", ".mp4", ".mov", ".mkv", '.flv', '.mpeg', '.3gp', '.webm', '.vob', '.bivx']
}


if __name__ == '__main__':
    main()