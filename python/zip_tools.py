'''Functions for zipping and unzipping files using the zipfile module.'''


import os
import shutil
import zipfile


def zip_files(source_dir, output_path):
    '''Compresses all files in a directory into a single ZIP archive.

    Args:
        source_dir (str): The directory to zip.
        output_path (str): The path to save the ZIP archive to.
    '''
    with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(source_dir):
            for file_ in files:
                zipf.write(os.path.join(root, file_))


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


def zip_subfolders(source_dir, output_dir):
    '''Create a ZIP archive for each top-level directory in source_dir, saving each archive to
    output_dir with the same name. Uses shutil.make_archive().

    Args:
        source_dir (str): Source directory containing folders to zip.
        output_dir (str): Output directory to export zipped folders to.

    Returns:
        None
    '''
    # Create output_dir if not exist.
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Get list of directories in source_dir.
    dirs = [entry.name for entry in os.scandir(source_dir) if entry.is_dir()]

    # Zip every directory.
    total = len(dirs)
    for ind, item in enumerate(dirs, start=1):
        print('[{}/{}] Zipping {}'.format(ind, total, item))
        output_zip_path = os.path.join(output_dir, item)
        source_item = os.path.join(source_dir, item)
        shutil.make_archive(base_name=output_zip_path, format='zip', root_dir=source_item)
