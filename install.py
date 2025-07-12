import os
import urllib.request
import zipfile
import shutil
import appex
import console

# Constants
GITHUB_ZIP_URL = 'https://github.com/TheMrNaab/BroadcastifyShortcutsPY/archive/refs/heads/main.zip'
ZIP_FILENAME = 'BroadcastifyShortcutsPY.zip'
EXTRACT_DIR = 'BroadcastifyShortcutsPY-main'
DEST_DIR = 'BroadcastifyShortcutsPY'

def download_zip():
    console.show_activity()
    print('Downloading ZIP from GitHub...')
    urllib.request.urlretrieve(GITHUB_ZIP_URL, ZIP_FILENAME)
    print('Download complete.')

def extract_zip():
    print('Extracting ZIP...')
    with zipfile.ZipFile(ZIP_FILENAME, 'r') as zip_ref:
        zip_ref.extractall()
    print('Extraction complete.')

def move_files():
    if os.path.exists(DEST_DIR):
        print(f'Removing old "{DEST_DIR}" directory...')
        shutil.rmtree(DEST_DIR)

    print(f'Moving "{EXTRACT_DIR}" to "{DEST_DIR}"...')
    shutil.move(EXTRACT_DIR, DEST_DIR)
    print('Move complete.')

def cleanup():
    print('Cleaning up...')
    if os.path.exists(ZIP_FILENAME):
        os.remove(ZIP_FILENAME)
    print('Cleanup done.')

def main():
    download_zip()
    extract_zip()
    move_files()
    cleanup()
    print('\n✅ Installed to folder: BroadcastifyShortcutsPY')
    print('📂 You can now open it in Pythonista and run script.py')

if __name__ == '__main__':
    main()
