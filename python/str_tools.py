# -*- coding: utf-8 -*-

'''Useful string-related functions.'''


import os
import re
import unidecode

from python_compatibility import is_string


def string_match(
        string_to_match, string_list, ignore_case=False, ignore_accents=False, remove_chars=None,
        split_ext=False):
    '''Check if a string or list of strings matches any of the strings in a list of strings, with
    options for ignoring case, ignoring Unicode, removing certain characters, and splitting strings
    into name and extension.

    Written with the help of ChatGPT.

    Args:
        string_to_match (str or [str]): The string(s) to match.
        string_list (list): A list of strings to search for a match.
        ignore_case (bool): Ignore the case of the strings. Defaults to False.
        ignore_accents (bool, optional): Ignore accents in the strings. Defaults to False.
        remove_chars (str, None): A string containing all characters to remove from the strings.
            Defaults to None.
        split_ext (bool): Split the strings in `string_list` into name and extension, and
            match by name. Defaults to False.

    Returns:
        str or None: The first string in the list that matches the input string, or None if no match
            is found.
    '''
    # Use list of strings to match.
    strings_to_match = string_to_match if isinstance(string_to_match, list) else [string_to_match]

    # Use private, modified variable _string_list with same length and order as string_list.
    _string_list = string_list

    # Ignore case.
    if ignore_case:
        strings_to_match = [str_.lower() for str_ in strings_to_match]
        _string_list = [str_.lower() for str_ in _string_list]

    # Ignore accent (ie. "e" and "é".)
    if ignore_accents:
        strings_to_match = [unidecode.unidecode(str_) for str_ in strings_to_match]
        _string_list = [unidecode.unidecode(str_) for str_ in _string_list]

    # Remove specified characters.
    if remove_chars:
        regex = '[' + re.escape(remove_chars) + ']'
        strings_to_match = [re.sub(regex, '', str_) for str_ in strings_to_match]
        _string_list = [re.sub(regex, '', str_) for str_ in _string_list]

    # Split extension in string_list.
    if split_ext:
        _string_list = [os.path.splitext(str_)[0] for str_ in _string_list]

    results = []
    for string_to_match in strings_to_match:
        for i, string in enumerate(_string_list):
            if string_to_match == string:
                # It's a match! :D
                if len(strings_to_match) == 1:
                    return string_list[i]
                results.append(string_list[i])
        else:
            # Not found, so add None.
            if len(strings_to_match) == 1:
                return None
            results.append(None)

    return results
