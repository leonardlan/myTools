'''Tools extending subprocess module.'''


import subprocess


MELD_EXE = r'C:\Program Files (x86)\Meld\Meld.exe'
SUBLIME_TEXT_EXE = r'C:\Program Files\Sublime Text 3\sublime_text.exe'


def run_command(command, *args):
    '''Run command with args using subprocess.Popen().'''
    contents = [command] + list(args)
    command = ['"{}"'.format(c) if ' ' in c else c for c in contents]
    command = ' '.join(command)
    print('Running command: {}'.format(command))
    return subprocess.Popen(contents)


def meld(*args):
    run_command(MELD_EXE, *args)


def subl(*args):
    '''Open Sublime Text on files/folders.'''
    run_command(SUBLIME_TEXT_EXE, *args)
