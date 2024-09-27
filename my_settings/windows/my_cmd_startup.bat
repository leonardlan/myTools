@echo off

echo Running my_cmd_startup.bat...

:: My windows cmd settings. Set path as AutoRun of "Command Processor" key using regedit.
:: Query current AutoRun value:
:: REG QUERY "HKEY_LOCAL_MACHINE\Software\Microsoft\Command Processor" /v AutoRun

:: Make prompt nice
:: Example:
:: [10:05:29 Leonard@MY-PC]
:: C:\Users\Leonard
:: > 
:: First line is blue (except username and computername is cyan), second line is green, third line
:: with the ">" is white.
set prompt=$E[1;34m[$t$h$h$h $E[1;36m%username%@%computername%$E[1;34m]$_$E[1;32m$p$_$E[1;0m$g$s$E[1;0m

set DEV=%USERPROFILE%\dev
set MYTOOLS_PATH=%DEV%\myTools
set MYTOOLS_PYTHONPATH=%MYTOOLS_PATH%\python
set MYTOOLS_MY_SETTINGS=%MYTOOLS_PATH%\my_settings

:: Python env vars
set PYTHONPATH=%PYTHONPATH%;%MYTOOLS_PYTHONPATH%
set PYTHONSTARTUP=%MYTOOLS_MY_SETTINGS%\pythonrc

:: Env vars
set SANDBOX_PATH=%DEV%\sandbox
set SANDBOX_SCRIPTS=%SANDBOX_PATH%\scripts
set WORKSPACE_PATH=%DEV%\workspace
set SUBLIME_PATH="C:\Program Files\Sublime Text 3\sublime_text.exe"

:: My aliases/doskeys
doskey ls=dir $*
doskey h=doskey /history
doskey py=python $*
doskey p=python $*
doskey pi=python -i $*
doskey python-vanilla="set \"PYTHONPATH=\" & set \"PYTHONSTARTUP=\" & python"
doskey nt=nosetests $*
doskey tree=tree /f $*

:: Make directory and cd into it
doskey mkcd=md $1 ^& cd $1

doskey u=cd ..
doskey uu=cd ..\..
doskey uuu=cd ..\..\..
doskey uuuu=cd ..\..\..\..
doskey uuuuu=cd ..\..\..\..\..

:: Change directory to popular folders
doskey Documents=cd %USERPROFILE%\Documents
doskey Downloads=cd %USERPROFILE%\Downloads
doskey Pictures=cd %USERPROFILE%\Pictures

doskey dev=cd %DEV%
doskey myTools=cd %MYTOOLS_PATH%
doskey sandbox=cd %SANDBOX_PATH%
doskey sandbox_scripts=cd %SANDBOX_SCRIPTS%
doskey workspace=cd %WORKSPACE_PATH%
doskey ws=cd %WORKSPACE_PATH%

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
doskey git-show-top-level=git rev-parse --show-toplevel


SETLOCAL

:: Add 's' Sublime doskey
IF EXIST %SUBLIME_PATH% (
    doskey s=%SUBLIME_PATH% $*
) ELSE (
    @echo on
    echo Sublime Text not installed at %SUBLIME_PATH%
    @echo off
)

:: Add sm doskey
set sublime_merge_path="C:\Program Files\Sublime Merge\sublime_merge.exe"
IF EXIST %sublime_merge_path% (
    doskey sm=%sublime_merge_path% $*
) ELSE (
    @echo on
    echo Sublime Merge not installed at %sublime_merge_path%
    @echo off
)

ENDLOCAL


:: Add executables and batch scripts to PATH.
set PATH=%PATH%;%MYTOOLS_PATH%\bin\windows


:: Shortcuts for editing and re-running this current file (my_cmd_startup.bat)
set MY_CMD_STARTUP_PATH=%MYTOOLS_MY_SETTINGS%\windows\my_cmd_startup.bat
doskey my_cmd_startup=%MY_CMD_STARTUP_PATH%
doskey open_my_cmd_startup=%SUBLIME_PATH% %MY_CMD_STARTUP_PATH%
