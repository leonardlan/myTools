'''FFMPEG tools.'''


import datetime
import os
import re
import subprocess
import time

from lancore import human_time
from python_compatibility import is_string


FFMPEG_CMD = 'ffmpeg'
FFPROBE_CMD = 'ffprobe'
MP3_EXT = '.mp3'


def trim(
        media_path, start='', end='', track_num=None, output_path=None, suffix='_trimmed',
        dry_run=False):
    '''Trim audio/video to input start/end timestamps and as save as output_path.

    Example ffmpeg command:
    ffmpeg -ss 00:01:00 -to 00:02:00 -i input.mp4 -c copy output.mp4

    Args:
        media_path (str): Path to audio/video.

    Kwargs:
        start (str, int, or float): Start timestamp as string ('HH:MM:SS'; ie. '00:01:12', 'MM:SS';
            ie. '2:25') or seconds as int or float.
        end (str): End timestamp as string or seconds from end of file, as positive int or float.
        track_num (int, str, or None): Metadata track number to add to trimmed file.
        output_path (str): Output path. If None, adds suffix to filename.
        suffix (str): If output_path is None, adds default suffix.
        dry_run (bool): Doesn't run ffmpeg command if True.

    Returns:
        int: Result from os.system(command) call.
    '''
    commands = [FFMPEG_CMD]

    # Add start/end timestamps.
    if start:
        start = _as_timestamp(start)
        commands.extend(['-ss', start])
    if end:
        if isinstance(end, (int, float)):
            length = get_length(media_path)
            end = length - end

            if end < 0:
                raise ValueError(
                    'End timestamp cannot be negative: {}. Should be positive number of seconds ' \
                    'from end of file'.format(end))

            end = _as_timestamp(end)
        commands.extend(['-to', end])

    # Default output path.
    if not output_path:
        root, ext = os.path.splitext(media_path)
        output_path = root + suffix + ext

    commands.extend(['-i', '"{}"'.format(media_path)])

    # Add track number.
    if track_num:
        commands.extend([f'-metadata track={track_num}'])

    commands.extend(['-c', 'copy', '"{}"'.format(output_path)])

    cmd = ' '.join(commands)
    print('Running command: {}'.format(cmd))
    if dry_run:
        print('Not running in dry run')
        return None

    return os.system(cmd)


def get_length(media_path):
    '''Returns length of video/audio as float.'''
    result = subprocess.run(
        [
            FFPROBE_CMD, '-v', 'error', '-show_entries', 'format=duration', '-of',
            'default=noprint_wrappers=1:nokey=1', media_path],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT)
    return float(result.stdout)


def _as_timestamp(seconds):
    '''Convert int/float into timestamp string of 'HH:MM:SS'. Return input if already string.

    Args:
        seconds (str, int, or float): Seconds as:
            - string: acceptable by ffmpeg (ie. 'MM:SS', 'HH:MM:SS' or 'HH:MM:SS.SSS')
            - int: 100 -> '0:01:40'
            - float: 55.123 -> '0:00:55.123000'

    Returns:
        str: Timestamp as HH:MM:SS.

    Raises:
       TypeError: If seconds is invalid type.
    '''
    if isinstance(seconds, (int, float)):
        return str(datetime.timedelta(seconds=seconds))
    elif is_string(seconds):
        return seconds
    raise TypeError(
        'Invalid seconds type: {}. Should be int, float, or string'.format(type(seconds)))


def convert_to_mp3(media_path, remove_original=False):
    '''Convert file to mp3.'''
    file_name, _ = os.path.splitext(media_path)
    root = os.path.dirname(media_path)
    media_path = os.path.join(root, media_path)
    dest_file = os.path.join(root, '{}{}'.format(file_name, MP3_EXT))
    if not os.path.exists(dest_file):
        res = os.system('{} -i "{}" "{}"'.format(FFMPEG_CMD, media_path, dest_file))

        if res == 0 and remove_original:
            print('Removing original {}'.format(media_path))
            os.remove(media_path)
        return dest_file
    else:
        print('File already exists: {}'.format(dest_file))


def convert_to_mp3_in_dir(root, remove_original=False):
    '''Convert audio/video files to mp3 in DIR using ffmpeg.'''
    if not os.path.exists(root):
        print('Path does not exist: {}'.format(root))
        return

    files = os.listdir(root)
    start = time.time()
    count = len(files)
    already_converted = []
    failed_to_convert = []
    converted = []
    for ind, fil in enumerate(files):
        fil = os.path.join(root, fil)
        if fil.endswith(MP3_EXT):
            continue

        print('Converting {} ({}/{})...'.format(fil, ind + 1, count))
        res = convert_to_mp3(fil, remove_original=remove_original)

        if res == 0:
            converted.append(fil)
        elif res is None:
            already_converted.append(fil)
        else:
            failed_to_convert.append(fil)

    # Print report.
    if converted:
        print('Converted {} in {}'.format(
            converted[0] if len(converted) == 1 else '{} files'.format(len(converted)),
            human_time(time.time() - start)))
    else:
        print('Did not convert any files')

    # Print already converted.
    if already_converted:
        print('Already converted {} file(s):\n{}'.format(
            len(already_converted), '\n'.join(already_converted)))

    # Print failed to convert.
    if failed_to_convert:
        print('Failed to convert {} file(s):\n{}'.format(
            len(failed_to_convert), '\n'.join(failed_to_convert)))


def split_audio_file(
        audio_file_path, timestamps_file_path, overwrite=False, directory='.', add_track_num=True,
        dry_run=True):
    '''Split an audio file into smaller files based on timestamps defined in a text file.

    Written with the help of ChatGPT.

    Args:
        audio_file_path (str): The path to the input audio file.
        timestamps_file_path (str): The path to the text file containing the timestamps for
            splitting the audio file. Example line: "0:00 3:45 Song Title"
        overwrite (bool): If True, overwrite existing output files with the same name. Defaults to
            False.
        directory (str): The directory where the output files will be saved. Defaults to the current
            directory.
        add_track_num (bool): If True, adds track number according to order in timestamp file,
            starting with 1.
        dry_run (bool): Doesn't run ffmpeg command if True.

    Returns:
        None

    Raises:
        None

    Example Usage:
    >>> split_audio_file(
            'input_file.mp3',
            'timestamps.txt',
            overwrite=True,
            directory='/path/to/output/directory')
    '''
    # Open the timestamps file and read in each line.
    with open(timestamps_file_path, 'r') as f:
        lines = f.readlines()

    # Iterate through each line, split it into its components, and split the audio file.
    failed_files = []
    for index, line in enumerate(lines):
        components = line.strip().split(' ')
        start = components[0]
        end = components[1]
        text = ' '.join(components[2:])
        track_num = index + 1

        # Generate a new file name based on the text
        new_file_name = f'{text}.mp3'

        # Check if the file already exists and whether we should overwrite it
        file_path = os.path.join(directory, new_file_name)
        if os.path.exists(file_path) and not overwrite:
            print(f'Skipping file {file_path} since it already exists and overwrite=False')
            continue

        # Use FFmpeg to split the audio file
        result = trim(
            audio_file_path,
            start=start,
            end=end,
            track_num=track_num if add_track_num else None,
            output_path=file_path,
            dry_run=dry_run)

        # Check if the split was successful and print a message
        if result == 0:
            print(f'Split audio file from {start} to {end} and saved to {file_path}')
        elif not dry_run:
            print(f'Failed to split audio file from {start} to {end} and save to {file_path}')
            failed_files.append(file_path)

    # Print out a list of files that failed to save
    if not dry_run and failed_files:
        print('The following files failed to save:')
        for file_name in failed_files:
            print(file_name)
