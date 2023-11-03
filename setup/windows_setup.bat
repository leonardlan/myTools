@echo off
REM Make sandbox dir.
set SANDBOX_PATH=%USERPROFILE%\dev\sandbox
if not exist "%SANDBOX_PATH%" (
    mkdir "%SANDBOX_PATH%"
    echo Created sandbox folder: %SANDBOX_PATH%
) else (
    echo Sandbox folder already exists: %SANDBOX_PATH%
)

REM Setup general symlinks.
echo Setting up git symlinks...
mklink /H "%USERPROFILE%\.gitconfig" "%~dp0\..\my_settings\gitconfig"
mklink /H "%USERPROFILE%\.gitignore_global" "%~dp0\..\my_settings\gitignore_global"
echo Git symlinks all set up

rem echo Setting up Sublime symlink...
rem mklink /H "%USERPROFILE%\AppData\Roaming\Sublime Text 3\Packages\User\Preferences.sublime-settings" "%~dp0\..\sublime\Preferences.sublime-settings"
rem mklink /H "%USERPROFILE%\AppData\Roaming\Sublime Text 3\Packages\User\Default (Windows).sublime-keymap" "%~dp0\..\sublime\Default (Windows).sublime-keymap"
rem mklink /H "%USERPROFILE%\AppData\Roaming\Sublime Text 3\Packages\User\python_class.sublime-snippet" "%~dp0\..\sublime\snippets\python_class.sublime-snippet"
rem mklink /H "%USERPROFILE%\AppData\Roaming\Sublime Text 3\Packages\User\python_function.sublime-snippet" "%~dp0\..\sublime\snippets\python_function.sublime-snippet"
rem mklink /H "%USERPROFILE%\AppData\Roaming\Sublime Text 3\Packages\User\python_function_simple.sublime-snippet" "%~dp0\..\sublime\snippets\python_function_simple.sublime-snippet"
rem mklink /H "%USERPROFILE%\AppData\Roaming\Sublime Text 3\Packages\User\python_docstring.sublime-snippet" "%~dp0\..\sublime\snippets\python_docstring.sublime-snippet"
rem mklink /H "%USERPROFILE%\AppData\Roaming\Sublime Text 3\Packages\User\python_unittest.sublime-snippet" "%~dp0\..\sublime\snippets\python_unittest.sublime-snippet"
rem echo Sublime symlinks all set up

rem Install Python packages.
@echo off
setlocal
set /p userConfirmation=Do you want to pip install requirements (y/n)? 
if /i "%userConfirmation%"=="y" (
    echo Installing python packages...
    pip install -r requirements.txt
    echo Python packages installed
) else (
    echo Not installing python packages
)
endlocal
