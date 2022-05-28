from enum import Enum


class MultiValueEnum(Enum):
    '''Enum with support for tuple values.'''

    def __new__(cls, *values):
        obj = object.__new__(cls)
        # First value is canonical value.
        obj._value_ = values[0]
        for other_value in values[1:]:
            cls._value2member_map_[other_value] = obj
        obj._all_values = values
        return obj

    def __repr__(self):
        return '<%s.%s: %s>' % (
                self.__class__.__name__,
                self._name_,
                ', '.join([repr(v) for v in self._all_values]),
                )


class FileExtensions(MultiValueEnum):
    '''Match file type to file extensions.

    Example:
    >>> file_extensions.FileExtensions('wma')
    <FileExtensions.AUDIO: 'aif', 'mp3', 'wav', 'wma'>
    >>> file_extensions.FileExtensions('txt')
    <FileExtensions.TEXT: 'txt'>
    >>> file_extensions.FileExtensions('mp4')
    <FileExtensions.VIDEO: 'avi', 'mov', 'mp4', 'mpeg', 'mpg'>
    '''

    # A/V.
    AUDIO = 'aif', 'mp3', 'wav', 'wma'
    IMAGE = 'exr', 'gif', 'jpeg', 'jpg', 'png', 'ppm', 'svg', 'tif', 'tiff', 'ttf'
    VIDEO = 'avi', 'mov', 'mp4', 'mpeg', 'mpg'

    # Documents.
    EXCEL = 'xls', 'xlsb', 'xlsm', 'xlsx'
    PDF = 'pdf'
    POWERPOINT = 'ppt', 'pptm', 'pptx'
    WORD = 'doc', 'docx'

    # DCC Software.
    BLENDER = 'blend', 'blend1'
    MAYA = 'ma', 'mb', 'mel'
    NUKE = 'nk'
    ALEMBIC = 'abc'
    FBX = 'fbx'
    OBJ = 'obj'
    PHOTOSHOP = 'psd'

    # Software development.
    BASH = 'bash', 'bashrc', 'bash_profile'
    C_PLUS_PLUS = 'c', 'cpp', 'c++', 'h'
    C_SHARP = 'c#'
    CMD = 'bat'
    CSS = 'css'
    DATABSE = 'db'
    GIT = 'git', 'gitignore'
    HTML = 'htm', 'html'
    JAVA = 'java', 'class'
    JAVASCRIPT = 'js'
    LOG = 'log'
    MAKEFILE = 'makefile'
    PERL = 'perl'
    PHP = 'php'
    PYTHON = 'py', 'pyc'
    SQL = 'sql', 'sqlite3'

    # Miscellaneous.
    DATA = 'csv', 'json', 'xml', 'yml'
    EXECUTABLE = 'exe'
    MARKDOWN = 'markdown', 'md'
    RESTRUCTURED = 'rst'
    TEXT = 'txt'
    ZIP = 'zip'
