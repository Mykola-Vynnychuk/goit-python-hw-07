import sys
from pathlib import Path
import uuid
import shutil


CATEGORIES = {"Archives": [".zip", ".gz", ".tar", ".rar"],
              "Audio": [".mp3", ".ogg", ".wav", ".amr"],
              "Documents": [".doc", ".docx", ".txt", ".pdf", ".xlsx", ".pptx"],
              "Images": [".jpeg", ".png", ".jpg", ".svg"],
              "Video": [".avi", ".mp4", ".mov", ".mkv"]}


CYRILLIC_SYMBOLS = "абвгґдеёєжзиіїйклмнопрстуфхцчшщъыьэюя"

TRANSLATION = ("a", "b", "v", "h", "g", "d", "e", "e", "ie", "zh", 
               "z", "y", "i", "i", "i", "k", "l", "m", "n", "o", "p", 
               "r", "s", "t", "u", "f", "kh", "ts", "ch", "sh", "shch", 
               "", "y", "", "e", "iu", "ia")

BAD_SYMBOLS = ("%", "*", " ", "-")

TRANS = {}

for c, t in zip(list(CYRILLIC_SYMBOLS), TRANSLATION):
    TRANS[ord(c)] = t
    TRANS[ord(c.upper())] = t.upper()

for i in BAD_SYMBOLS:
    TRANS[ord(i)] = "_"

known_extensions = []

unknown_extensions = []

def normalize(name: str) -> str:
    return name.translate(TRANS)
    
def move_file(file: Path, root_dir: Path, categorie: str) -> None:
    target_dir = root_dir.joinpath(categorie)
    if not target_dir.exists():
        target_dir.mkdir()
        print(f"Make {target_dir}")

    new_name = target_dir.joinpath(f"{normalize(file.stem)}{file.suffix}")
    
    if new_name.exists():
        new_name = new_name.with_name(f"{new_name.stem}-{uuid.uuid4()}{file.suffix}")
        print(f"File {file} has been renamed to {new_name.name}")
    file.rename(new_name)
    print(f"File {new_name.name} has been moved to the directory \"{categorie}\"")

def get_categories(file: Path) -> str:
    ext = file.suffix
    for cat, exts in CATEGORIES.items():
        if ext in exts:
            known_extensions.append(file.suffix)
            return cat
    unknown_extensions.append(file.suffix)
    return "Other"

def delete_empty_folder(path: Path) -> None:
    for item in path.iterdir():
        if item.is_dir():
            delete_empty_folder(item)
            if not any(item.iterdir()):
                item.rmdir()
                print(f"Empty directory {str(item)} has been deleted")

def unpack_archive(path: Path) -> None:
    archives_folder = path / "Archives"
    if archives_folder.is_dir():
        for file_path in archives_folder.iterdir():
            if file_path.is_file():
                try:
                    shutil.unpack_archive(str(file_path), str(archives_folder / file_path.stem))
                    print(f"Archive {str(file_path)} unpack successful")
                    file_path.unlink()
                except PermissionError:
                    print(f"Archive {str(file_path)} was not unpacked")
                    continue
    else:
        print("Directoria 'Archives' does not exist")
    

def sort_folder(path: Path) -> None:
    path_list = list(path.glob("**/*"))[::-1]
    for i in path_list:
        if i.is_file():
            move_file(i, path, get_categories(i))
        else: 
            delete_empty_folder(path)

def get_category_files_log(path: Path) -> None:
    for category in CATEGORIES:
        category_dir = path / category
        files = list(category_dir.glob("*"))
        if files:
            print(f"\nFiles in category '{category}':")
            for file in files:
                print(file.name)

def main():
    try:
        path = Path(sys.argv[1])
    except IndexError:
        return "No path to folder"
    
    if not path.exists():
        return f"Folder with path {path} dos not exists."
    
    sort_folder(path)
    unpack_archive(path)
    get_category_files_log(path)
    print(f'\nSorted files with the following known extensions:\n{set(known_extensions)}\n')
    print(f'\nFiles with the following unknown extensions have been moved to the "Other" directory:\n{set(unknown_extensions)}\n')
    return "Congratulations! The files have been successfully sorted\n"

if __name__ == "__main__":
    print(main())
