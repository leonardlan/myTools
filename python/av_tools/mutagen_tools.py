'''Read and write metadata of audio/video files using mutagen.'''


import mutagen


KEY_TRACK = 'TRCK'
KEY_TITLE = 'TIT2'
KEY_ARTIST = 'TPE1'
KEY_ALBUM = 'TALB'


def read_metadata(file_path):
    '''
    Read the track number, title, artist, and album from an audio or video file.

    Args:
    file_path (str): The path of the file to read the metadata from.

    Returns:
    tuple: A tuple of four values: the track number, title, artist, and album. Any of these values
    may be None if the metadata is not present in the file.
    '''
    audio = mutagen.File(file_path)
    track_num = audio.get(KEY_TRACK, [None])[0]
    title = audio.get(KEY_TITLE, [None])[0]
    artist = audio.get(KEY_ARTIST, [None])[0]
    album = audio.get(KEY_ALBUM, [None])[0]
    return track_num, title, artist, album


def write_metadata(file_path, track_num, title, artist, album):
    '''
    Write the track number, title, artist, and album to an audio or video file.

    Args:
    file_path (str): The path of the file to write the metadata to.
    track_num (int or str): The track number.
    title (str): The title.
    artist (str): The artist.
    album (str): The album.

    Returns:
    None
    '''
    audio = mutagen.File(file_path)
    audio[KEY_TRACK] = str(track_num)
    audio[KEY_TITLE] = title
    audio[KEY_ARTIST] = artist
    audio[KEY_ALBUM] = album
    audio.save()
