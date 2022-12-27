'''FFMPEG tools.'''


import os

FFMPEG_CMD = 'ffmpeg'


def trim(file_path, start_timestamp='', end_timestamp='', output_path=None):
    '''Trim audio/video to input start/end timestamps and as save as output_path.

    Example ffmpeg command:
    ffmpeg -ss 00:01:00 -to 00:02:00 -i input.mp4 -c copy output.mp4

    Args:
        file_path (str): Path to audio/video.

    Kwargs:
        start_timestamp (str): Start timestamp (ie. '00:01:12').
        end_timestamp (str): End timestamp (ie. '01:14:36').
        output_path (str): Output path. If None, adds '_trimmed' suffix.

    Returns:
        int: Result from os.system(command) call.
    '''
    commands = [FFMPEG_CMD]

    # Set start/end timestamps.
    if start_timestamp:
        commands.extend(['-ss', start_timestamp])
    if end_timestamp:
        commands.extend(['-to', end_timestamp])

    # Default output path.
    if not output_path:
        root, ext = os.path.splitext(file_path)
        output_path = root + '_trimmed' + ext

    commands.extend(['-i', '"{}"'.format(file_path), '-c', 'copy', '"{}"'.format(output_path)])

    cmd = ' '.join(commands)
    print('Running command: {}'.format(cmd))
    res = os.system(cmd)
    return res
