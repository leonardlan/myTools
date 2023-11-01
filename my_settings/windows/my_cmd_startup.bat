@echo off

:: My windows cmd settings. Set path as AutoRun of "Command Processor" key using regedit.
:: Query current AutoRun value:
:: REG QUERY "HKEY_LOCAL_MACHINE\Software\Microsoft\Command Processor" /v AutoRun

:: Make prompt nice
:: Example:
:: [10:05:29 Leonard@MY-PC]
:: C:\Users\Leonard
:: >
set prompt=[$t$h$h$h %username%@%computername%]$_$p$_$g$s

set MYTOOLS_PYTHONPATH=%USERPROFILE%\myTools\python

:: Python env vars
set PYTHONPATH=%PYTHONPATH%;%MYTOOLS_PYTHONPATH%
set PYTHONSTARTUP=%USERPROFILE%\myTools\my_settings\pythonrc

:: Set git ignore global on windows
git config --global core.excludesfile "%USERPROFILE%\.gitignore_global"

:: Env vars
set MYTOOLS=%USERPROFILE%\myTools
set SANDBOX_SCRIPTS=%USERPROFILE%\sandbox\scripts

:: My aliases/doskeys
doskey h=doskey /history
doskey py=python $*
doskey p=python $*
doskey pi=python -i $*
doskey python-vanilla="set \"PYTHONPATH=\" & set \"PYTHONSTARTUP=\" & python"

doskey u=cd ..
doskey uu=cd ..\..
doskey uuu=cd ..\..\..
doskey uuuu=cd ..\..\..\..
doskey uuuuu=cd ..\..\..\..\..

:: Popular folders
doskey Documents=cd %USERPROFILE%\Documents
doskey Downloads=cd %USERPROFILE%\Downloads
doskey Pictures=cd %USERPROFILE%\Pictures

doskey myTools=cd %MYTOOLS%
doskey sandbox=cd %USERPROFILE%\sandbox
doskey sandbox_scripts=cd %SANDBOX_SCRIPTS%

:: Git
doskey gg=git gui
doskey gs=git st
doskey gd=git diff
doskey gb=git branch
doskey gac="git add . & git commit -m"
doskey gp=git push
doskey gl=git pull
doskey gpom=git push origin master
doskey glom=git pull origin master
doskey gmom=git merge origin/master
doskey git-show-devs=git shortlog -sn
doskey git-show-origin=git remote show origin
doskey git-stash-show=git stash show -p

SETLOCAL

:: Add s doskey.
set sublime_path="C:\Program Files\Sublime Text 3\sublime_text.exe"
IF EXIST %sublime_path% (
    doskey s=%sublime_path% $*
) ELSE (
    @echo on
    echo Sublime Text not installed at %sublime_path%
    @echo off
)

:: Add sm doskey.
set sublime_merge_path="C:\Program Files\Sublime Merge\sublime_merge.exe"
IF EXIST %sublime_merge_path% (
    doskey sm=%sublime_merge_path% $*
) ELSE (
    @echo on
    echo Sublime Merge not installed at %sublime_merge_path%
    @echo off
)

ENDLOCAL

doskey useful-commands=s %MYTOOLS%\docs\useful_commands.md

:: Python
doskey nt=nosetests $*
