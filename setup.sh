# Make sandbox dir
mkdir -p ~/dev/sandbox

# Setup my general symlinks
echo Setting up symlinks...
ln -sfnv `readlink -f my_settings/bash_aliases` ~/.bash_aliases
ln -sfnv `readlink -f my_settings/gitconfig` ~/.gitconfig
ln -sfnv `readlink -f my_settings/gitignore_global` ~/.gitignore_global
ln -sfnv `readlink -f my_settings/my_bashrc` ~/.my_bashrc
ln -sfnv `readlink -f my_settings/pythonrc` ~/.pythonrc
ln -sfnv `readlink -f docs/useful_commands.md` ~/useful_commands.md
ln -sfnv `readlink -f myTools.desktop` ~/.local/share/applications/myTools.desktop
echo Symlinks all set up

echo Setting up Sublime symlink...
ln -sfn `readlink -f sublime/Preferences.sublime-settings` ~/.config/sublime-text-3/Packages/User/Preferences.sublime-settings
ln -sfn "`readlink -f sublime/'Default (Linux).sublime-keymap'`" ~/.config/sublime-text-3/Packages/User/'Default (Linux).sublime-keymap'
ln -sfn `readlink -f sublime/snippets/python_class.sublime-snippet` ~/.config/sublime-text-3/Packages/User/python_class.sublime-snippet
ln -sfn `readlink -f sublime/snippets/python_function.sublime-snippet` ~/.config/sublime-text-3/Packages/User/python_function.sublime-snippet
ln -sfn `readlink -f sublime/snippets/python_function_simple.sublime-snippet` ~/.config/sublime-text-3/Packages/User/python_function_simple.sublime-snippet
ln -sfn `readlink -f sublime/snippets/python_docstring.sublime-snippet` ~/.config/sublime-text-3/Packages/User/python_docstring.sublime-snippet
ln -sfn `readlink -f sublime/snippets/python_unittest.sublime-snippet` ~/.config/sublime-text-3/Packages/User/python_unittest.sublime-snippet
echo Sublime symlinks all set up

add_line_to_file() {
    # If line already exists, don't add it again
    grep -qF -- "$1" "$2" || echo "$1" >> "$2"
}

echo Adding source ~/.my_bashrc line to .bashrc file...
add_line_to_file 'source ~/.my_bashrc' ~/.bashrc

echo Adding cron job...
crontab -l > /tmp/mycron
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
add_line_to_file "0 9-18 * * 1-5 ${DIR}/bin/notify-time > /dev/null 2>&1 # Notify me every so often" /tmp/mycron
add_line_to_file "*/5 9-18 * * 1-5 ${DIR}/bin/change-desktop-wallpaper > /dev/null 2>&1 # Change desktop background" /tmp/mycron
crontab /tmp/mycron
rm /tmp/mycron
echo "New crontab:"
crontab -l
echo Cron job added

echo Installing python packages...
pip install -r requirements.txt
echo Python packages installed
