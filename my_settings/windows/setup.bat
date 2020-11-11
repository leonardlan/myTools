:: Setup my general symlinks
echo Setting up symlinks...
mklink "%USERPROFILE%\.gitconfig" "%USERPROFILE%\myTools\my_settings\gitconfig"
mklink "%USERPROFILE%\.gitignore_global" "%USERPROFILE%\myTools\my_settings\gitignore_global"
mklink "%USERPROFILE%\.pythonrc" "%USERPROFILE%\myTools\my_settings\pythonrc"
echo Symlinks all set up

echo Setting up Sublime symlink...
mklink "%USERPROFILE%\AppData\Roaming\Sublime Text 3\Packages\User\Preferences.sublime-settings" "%USERPROFILE%\myTools\sublime\Preferences.sublime-settings"
echo Sublime symlinks all set up
