from pathlib import Path
import re
import shutil
import sys
import argparse


concurrent_path = Path('.').cwd()

parser = argparse.ArgumentParser(prog='clean-folder', description='Cleaning folder')
parser.add_argument('--clean-folder', '-cfolder', default=concurrent_path)
parser.add_argument('--dest', '-d', default=concurrent_path, help='Destination folder')

args = vars(parser.parse_args())
clean_folder = args.get('clean-folder')
dest = args.get('dest')


CYRILLIC_SYMBOLS = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ'
TRANSLATION = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
               "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "u", "ja", "je", 'i', "ji", "g")

TRANS = {}

for c, l in zip(CYRILLIC_SYMBOLS,TRANSLATION):
    TRANS[ord(c)] = l
    TRANS[ord(c.upper())] = l.upper()


def normalize(name: str) -> str:

    t_name = name.translate(TRANS)
    t_name = re.sub(r'\W', '_', t_name)

    return t_name


JPEG_IMAGES = []
JPG_IMAGES = []
PNG_IMAGES = []
SVG_IMAGES = []

AVI_VIDEO = []
MP4_VIDEO = []
MOV_VIDEO = []
MKV_VIDEO = []

DOC_FILE = []
DOCX_FILE = []
TXT_FILE = []
PDF_FILE = []
XLSX_FILE = []
PPTX_FILE = []

MP3_AUDIO = []
OGG_AUDIO = []
WAV_AUDIO = []
AMR_AUDIO = []

ARCHIVES = []
MY_OTHER = []

REGISTER_EXTENSION = {
    'JPEG': JPEG_IMAGES,
    'JPG': JPG_IMAGES,
    'PNG': PNG_IMAGES,
    'SVG': SVG_IMAGES,
    'AVI': AVI_VIDEO,
    'MP4': MP4_VIDEO,
    'MOV': MOV_VIDEO,
    'MKV': MKV_VIDEO,
    'DOC': DOC_FILE,
    'DOCX': DOCX_FILE,
    'TXT': TXT_FILE,
    'PDF': PDF_FILE,
    'XLSX': XLSX_FILE,
    'PPTX': PPTX_FILE,
    'MP3': MP3_AUDIO,
    'OGG': OGG_AUDIO,
    'WAV': WAV_AUDIO,
    'AMR': AMR_AUDIO,
    'ZIP': ARCHIVES,
    'GZ': ARCHIVES,
    'TAR': ARCHIVES
}

FOLDERS = []
EXTENTIONS = set()
UNKNOWN = set()


def get_extention(filename: str) -> str:
    return Path(filename).suffix[1:].upper()


def scan(folder: Path):
    for item in folder.iterdir():

        # Робота з папкою
        if item.is_dir():

            # Перевіряємо, щоб папка не була тією в яку ми складаємо файли
            if item.name not in ('archives', 'video', 'audio', 'documents', 'other'):
                FOLDERS.append(item)
                scan(item)  # Скануємо цю вкладену папку

            continue  # Переходимо до наступного елементу в сканованій папці

        # ПРацюємо з файлом
        ext = get_extention(item.name)  # Беремо розширення файлу
        full_name = folder / item.name  # Берео повний шлях до файлу
        if not ext:
            MY_OTHER.append(full_name)
        else:
            try:
                container = REGISTER_EXTENSION[ext]
                EXTENTIONS.add(ext)
                container.append(full_name)
            except KeyError:
                UNKNOWN.add(ext)
                MY_OTHER.append(full_name)

#
# def handle_media(filename: Path, target_folder: Path) -> None:
#     target_folder.mkdir(exist_ok=True, parents=True)
#     filename.replace(target_folder / normalize(filename.name))
#
#
# def handle_other(filename: Path, target_folder: Path) -> None:
#     target_folder.mkdir(exist_ok=True, parents=True)
#     filename.replace(target_folder / normalize(filename.name))
#
#
# def handle_archive(filename: Path, target_folder: Path) -> None:
#     target_folder.mkdir(exist_ok=True, parents=True)
#     folder_for_file = target_folder / normalize(filename.name.replace(filename.suffix, ''))
#     folder_for_file.mkdir(exist_ok=True, parents=True)
#     try:
#         shutil.unpack_archive(str(filename.resolve()), str(folder_for_file.resolve()))
#     except shutil.ReadError:
#         folder_for_file.rmdir()
#         return None
#     filename.unlink()
#
#
# def handle_folder(folder: Path) -> None:
#     try:
#         folder.rmdir()
#     except OSError:
#         print(f'Sorry, we can not delate folder: {folder}')
#
#
# def main(folder: Path) -> None:
#     scan(folder)
#     for file in JPEG_IMAGES:
#         handle_media(file, folder / 'images' / 'JPEG')
#     for file in JPG_IMAGES:
#         handle_media(file, folder / 'images' / 'JPG')
#     for file in PNG_IMAGES:
#         handle_media(file, folder / 'images' / 'PNG')
#     for file in SVG_IMAGES:
#         handle_media(file, folder / 'images' / 'SVG')
#
#     for file in MP3_AUDIO:
#         handle_media(file, folder / 'audio' / 'MP3')
#     for file in OGG_AUDIO:
#         handle_media(file, folder / 'audio' / 'OGG')
#     for file in WAV_AUDIO:
#         handle_media(file, folder / 'audio' / 'WAV')
#     for file in AMR_AUDIO:
#         handle_media(file, folder / 'audio' / 'AMR')
#
#     for file in AVI_VIDEO:
#         handle_media(file, folder / 'video' / 'AVI')
#     for file in MP4_VIDEO:
#         handle_media(file, folder / 'video' / 'MP4')
#     for file in MOV_VIDEO:
#         handle_media(file, folder / 'video' / 'MOV')
#     for file in MKV_VIDEO:
#         handle_media(file, folder / 'video' / 'MKV')
#
#     for file in DOC_FILE:
#         handle_media(file, folder / 'documents' / 'DOC')
#     for file in DOCX_FILE:
#         handle_media(file, folder / 'documents' / 'DOCX')
#     for file in TXT_FILE:
#         handle_media(file, folder / 'documents' / 'TXT')
#     for file in PDF_FILE:
#         handle_media(file, folder / 'documents' / 'PDF')
#     for file in XLSX_FILE:
#         handle_media(file, folder / 'documents' / 'XLSX')
#     for file in PPTX_FILE:
#         handle_media(file, folder / 'documents' / 'PPTX')
#
#     for file in MY_OTHER:
#         handle_other(file, folder / 'MY_OTHERS')
#     for file in ARCHIVES:
#         handle_archive(file, folder / 'ARCHIVES')
#
#     for folder in FOLDERS[::-1]:
#         handle_folder(folder)


if __name__ == '__main__':

    folder_for_scan = dest #Path(sys.argv[1])

    #main(folder_for_scan.resolve())

    scan(Path(folder_for_scan))

    print(f"Images jpeg: {JPEG_IMAGES}")
    print(f"Images jpg: {JPG_IMAGES}")
    print(f"Images png: {PNG_IMAGES}")
    print(f"Images svg: {SVG_IMAGES}")

    print(f"Video avi: {AVI_VIDEO}")
    print(f"Video mp4: {MP4_VIDEO}")
    print(f"Video jmov: {MOV_VIDEO}")
    print(f"Video mkv: {MKV_VIDEO}")

    print(f"File doc: {DOC_FILE}")
    print(f"File docx: {DOCX_FILE}")
    print(f"File txt: {TXT_FILE}")
    print(f"File pdf: {PDF_FILE}")
    print(f"File xlsx: {XLSX_FILE}")
    print(f"File pptx: {PPTX_FILE}")

    print(f"Audio mp3: {MP3_AUDIO}")
    print(f"Audio ogg: {OGG_AUDIO}")
    print(f"Audio mwav: {WAV_AUDIO}")
    print(f"Audio amr: {AMR_AUDIO}")

    print(f"ARCHIVES: {ARCHIVES}")
    print('*' * 25)
    print(f'Types of file in folder: {EXTENTIONS}')
    print(f'UNKNOWN: {UNKNOWN}')