'''FFMPEG tools.'''


import datetime
import os
import subprocess

FFMPEG_CMD = 'ffmpeg'
FFPROBE_CMD = 'ffprobe'


def trim(media_path, start='', end='', output_path=None, suffix='_trimmed', dry_run=False):
    '''Trim audio/video to input start/end timestamps and as save as output_path.

    Example ffmpeg command:
    ffmpeg -ss 00:01:00 -to 00:02:00 -i input.mp4 -c copy output.mp4

    Args:
        media_path (str): Path to audio/video.

    Kwargs:
        start (str, int, or float): Start timestamp as string ('HH:MM:SS'; ie. '00:01:12') or
            seconds as int or float.
        end (str): End timestamp as string or seconds from end of file, as positive int or float.
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
                raise ValueError('End timestamp cannot be negative: {}'.format(end))

            end = _as_timestamp(end)
        commands.extend(['-to', end])

    # Default output path.
    if not output_path:
        root, ext = os.path.splitext(media_path)
        output_path = root + suffix + ext

    commands.extend(['-i', '"{}"'.format(media_path), '-c', 'copy', '"{}"'.format(output_path)])

    cmd = ' '.join(commands)
    print('Running command: {}'.format(cmd))
    if dry_run:
        print('Not running in dry run')
        return None

    res = os.system(cmd)
    return res


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
    '''Get string of timestamp (100 -> '0:01:40').'''
    if isinstance(seconds, (int, float)):
        return str(datetime.timedelta(seconds=seconds))
    return seconds
