from ast import Try
from operator import contains
import sys
from pathlib import Path
from typing import Container

# перелік файлів
JPEG_IMAGES, PNG_IMAGES, JPG_IMAGES, SVG_IMAGES = [], [], [], []
AVI_VIDEO, MP4_VIDEO, MOV_VIDEO, MKV_VIDEO = [], [], [], []
DOC_DOCUMENTS, DOCX_DOCUMENTS, TXT_DOCUMENTS, PDF_DOCUMENTS, XLSX_DOCUMENTS, PPTX_DOCUMENTS = [], [], [], [], [], []
MP3_AUDIO, OGG_AUDIO, WAV_AUDIO, AMR_AUDIO = [], [], [], []
ZIP_ARCHIVES, GZ_ARCHIVES, TAR_ARCHIVES = [], [], []
OTHER = []

# перелік папок
FOLDERS = []

REGISTER_EXTENTIONS = {
    'JPEG': JPEG_IMAGES, 'PNG': PNG_IMAGES, 'JPG': JPG_IMAGES, 'SVG': SVG_IMAGES,
    'AVI': AVI_VIDEO, 'MP4': MP4_VIDEO, 'MOV': MOV_VIDEO, 'MKV': MKV_VIDEO,
    'DOC': DOC_DOCUMENTS, 'DOCX': DOCX_DOCUMENTS, 'TXT': TXT_DOCUMENTS, 'PDF': PDF_DOCUMENTS, 'XLSX': XLSX_DOCUMENTS, 'PPTX': PPTX_DOCUMENTS,
    'MP3': MP3_AUDIO, 'OGG': OGG_AUDIO, 'WAV': WAV_AUDIO, 'AMR': AMR_AUDIO,
    'ZIP': ZIP_ARCHIVES, 'GZ': GZ_ARCHIVES, 'TAR': TAR_ARCHIVES
}

EXTENTIONS = set()
UNKNOWN = set()


def get_extention(filename: str) -> str:
    # перетворюю розширення файлу в назву папки (.mp3 -> MP3)
    return Path(filename).suffix[1:].upper()
    pass


def scan(folder: Path) -> None:
    # обробка папки
    for item in folder.iterdir():
        # якщо елемент - папка, то додаю його до списку FOLDER
        if item.is_dir():
            # перевіряю чи це не папка з результатами
            if item.name not in ('archives', 'video', 'audio', 'documents', 'images', 'OTHER'):
                FOLDERS.append(item)
                # сканую вкладену папку
                scan(item)
            # переходжу до наступного елементу в папці, що сканується
            continue

    # обробка файлу
        ext = get_extention(item.name)  # отримую розширення
        fullname = folder / item.name  # отримую повний шлях до файлу
        if not ext:  # якщо файл не має розширення, то додаю до невідомих
            OTHER.append(fullname)
        else:
            try:
                # беру список для додавання шляху до файлу
                container = REGISTER_EXTENTIONS[ext]
                EXTENTIONS.add(ext)
                container.append(fullname)
            except KeyError:
                # якщо не реєстрував розширення в REGISTER_EXTENTIONS, то додаю в OTHER
                UNKNOWN.add(ext)
                OTHER.append(fullname)


if __name__ == '__main__':
    folder_for_scan = sys.argv[1]
    print(f"Start in folder {folder_for_scan}")

    scan(Path(folder_for_scan))
    print(f"Images jpeg {JPEG_IMAGES}")
    print(f"Images jpg {JPG_IMAGES}")
    print(f"Images svg {SVG_IMAGES}")
    print(f"Audio mp3 {MP3_AUDIO}")
    print(f"Archives zip {ZIP_ARCHIVES}")

    print(f"File types {EXTENTIONS}")
    print(f"Unknown fule types {UNKNOWN}")

    print(f"Folders list: {FOLDERS[::-1]}")
