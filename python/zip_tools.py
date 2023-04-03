'''Functions for zipping and unzipping files using the zipfile module.'''


import os
import zipfile


def zip_files(source_dir, output_path):
    '''Compresses all files in a directory into a single ZIP archive.

    Args:
        source_dir (str): The directory to zip.
        output_path (str): The path to save the ZIP archive to.
    '''
    with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(source_dir):
            for file in files:
                zipf.write(os.path.join(root, file))


def extract_zip(zip_path, output_dir=None):
    '''Extracts all files from a ZIP archive to a directory. If the output directory already exists,
    files with the same name as those in the ZIP archive will be overwritten with the contents of
    the corresponding file in the ZIP archive.

    Args:
        zip_path (str): The path to the ZIP archive to extract.
        output_dir (str or None): The directory to extract the files to. If None, will use same name
        as zip file.
    '''
    output_dir = output_dir or os.path.splitext(zip_path)[0]
    with zipfile.ZipFile(zip_path, 'r') as zipf:
        zipf.extractall(output_dir)
    print('Extracted zip files to {output_dir}')
