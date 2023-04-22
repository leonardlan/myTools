'''Read and write metadata of audio/video files using mutagen.'''


import os

import mutagen

from mutagen.easyid3 import EasyID3


KEY_ALBUM = 'album'
KEY_ALBUMARTIST = 'albumartist'
KEY_ARTIST = 'artist'
KEY_COMPOSER = 'composer'
KEY_DATE = 'date'
KEY_GENRE = 'genre'
KEY_MEDIA = 'media'
KEY_TITLE = 'title'
KEY_TRACKNUMBER = 'tracknumber'
KEY_YEAR = 'year'

DEFAULT_READ_METADATA_KEYS = [KEY_ARTIST, KEY_ALBUM, KEY_TITLE, KEY_TRACKNUMBER]
KNOWN_KEYS = [
    KEY_ALBUM,
    KEY_ALBUMARTIST,
    KEY_ARTIST,
    KEY_COMPOSER,
    KEY_DATE,
    KEY_GENRE,
    KEY_TITLE,
    KEY_TRACKNUMBER,
    KEY_YEAR,
]

FRAME_ID_YEAR = 'TDRC'

# WMA file keys. They're different for some reason.
EXTENSION_WMA = 'wma'
EXTENSION_M4A = 'm4a'
_KEY_TO_WMA_KEY = {
    KEY_ALBUM: 'WM/AlbumTitle',
    KEY_ALBUMARTIST: 'WM/AlbumArtist',
    KEY_ARTIST: 'Author',
    KEY_COMPOSER: 'WM/Composer',
    KEY_GENRE: 'WM/Genre',
    KEY_TITLE: 'Title',
    KEY_TRACKNUMBER: 'WM/TrackNumber',
    KEY_YEAR: 'WM/Year',
}
# M4A file keys. "Year" is "date" for some reason.
_KEY_TO_M4A_KEY = {
    KEY_YEAR: 'date',
}
_EXTENSION_TO_KEY_DICT = {
    EXTENSION_M4A: _KEY_TO_M4A_KEY,
    EXTENSION_WMA: _KEY_TO_WMA_KEY,
}


_REGISTERED_YEAR = False


class BaseFile:

    '''Wrapper around class returned from mutagen.File() function call. Somehow it has different
    keys for .wma and .m4a files for some reason. Using this class to support the file types with
    same keys. See _KEY_TO_WMA_KEY and _KEY_TO_M4A_KEY for mapped keys.
    '''

    def __init__(self, file_path, **kwargs):
        self.file_path = file_path
        self.mutagen_file = mutagen.File(file_path, **kwargs)

    def __repr__(self):
        return 'BaseFile({})'.format(os.path.basename(self.file_path))

    @property
    def ext(self):
        '''File extension without the period.'''
        return os.path.splitext(self.mutagen_file.filename)[1].replace('.', '').lower()

    def _is_wma(self):
        '''True if file is .wma file.'''
        return self.ext == EXTENSION_WMA

    def _is_m4a(self):
        '''True if file is .m4a file.'''
        return self.ext == EXTENSION_M4A

    def _get_key(self, key):
        '''Keys vary depending on file type.'''
        key_map = _EXTENSION_TO_KEY_DICT.get(self.ext, {})
        return key_map.get(key, key) if key_map else key

    def __getitem__(self, key):
        '''Get key value.'''
        key = self._get_key(key)
        return self.mutagen_file.get(key)

    def get(self, key, default=None):
        '''Get key value, defaulting to specified value.'''
        key = self._get_key(key)
        return self.mutagen_file.get(key, default)

    def __contains__(self, key):
        '''Check if key in mutagen file keys.'''
        return key in self.mutagen_file

    def __setitem__(self, key, val):
        '''Change key value.'''
        key = self._get_key(key)
        self.mutagen_file[key] = val

    def __delitem__(self, key):
        '''Delete key.'''
        key = self._get_key(key)
        del self.mutagen_file[key]

    def keys(self):
        '''Return all keys.'''
        return self.mutagen_file.keys()

    def save(self, *args, **kwargs):
        '''Save file.'''
        return self.mutagen_file.save(*args, **kwargs)


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
    audio = BaseFile(file_path, easy=True)

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
    audio = BaseFile(file_path, easy=True)
    for key, val in kwargs.items():
        if key == KEY_YEAR:
            _register_year()
        audio[key] = val
    audio.save()


def delete_metadata(file_path, keys):
    '''Delete metadata keys in an audio or video file, if available.

    Args:
        file_path (str): The path of the file to delete the metadata in.
        keys (str or [str]): Key or list of keys to delete.

    Returns:
        None
    '''
    keys = [keys] if not isinstance(keys, list) else keys

    audio = BaseFile(file_path, easy=True)

    # Register year if requested, otherwise it won't work.
    if KEY_YEAR in keys:
        _register_year()

    for key in keys:
        if key in audio:
            del audio[key]
    audio.save()


def _register_year():
    global _REGISTERED_YEAR
    if not _REGISTERED_YEAR:
        print('Registering year...')
        EasyID3.RegisterTextKey(KEY_YEAR, FRAME_ID_YEAR)
        _REGISTERED_YEAR = True
