'''Read and write metadata of audio/video files using mutagen.'''


import mutagen

from mutagen.easyid3 import EasyID3


KEY_TRACKNUMBER = 'tracknumber'
KEY_TITLE = 'title'
KEY_ARTIST = 'artist'
KEY_ALBUM = 'album'
KEY_ALBUMARTIST = 'albumartist'
KEY_DATE = 'date'
KEY_GENRE = 'genre'
KEY_YEAR = 'year'

FRAME_ID_YEAR = 'TDRC'

DEFAULT_READ_METADATA_KEYS = [KEY_ARTIST, KEY_ALBUM, KEY_TITLE, KEY_TRACKNUMBER]
KNOWN_KEYS = [
    KEY_TRACKNUMBER,
    KEY_TITLE,
    KEY_ARTIST,
    KEY_ALBUM,
    KEY_ALBUMARTIST,
    KEY_DATE,
    KEY_GENRE,
    KEY_YEAR,
]


def read_metadata(file_path, keys=None):
    '''Get metadata values from an audio or video file, given list of keys to query.

    Args:
        file_path (str): The path of the file to read the metadata from.
        keys ([str]): List of keys to query. Will return values in same order. Defaults to
            DEFAULT_READ_METADATA_KEYS.

    Returns:
        list: A list of values in same order as given list.
    '''
    keys = keys or DEFAULT_READ_METADATA_KEYS
    audio = mutagen.File(file_path, easy=True)

    # Register year if requested, otherwise it won't work.
    if KEY_YEAR in keys:
        _register_year()

    return [audio.get(key, [None])[0] for key in keys]


def write_metadata(file_path, **kwargs):
    '''Write metadata of an audio or video file.

    Args:
        file_path (str): The path of the file to write the metadata to.
    Kwargs:
        Key to value of metadata to write. For example: {'artist': 'John', 'album': 'The Album'}.
        See KNOWN_KEYS for keys.

    Returns:
        None
    '''
    audio = mutagen.File(file_path, easy=True)
    for key, val in kwargs.items():
        if key == KEY_YEAR:
            _register_year()
        audio[key] = val
    audio.save()


def _register_year():
    EasyID3.RegisterTextKey(KEY_YEAR, FRAME_ID_YEAR)
