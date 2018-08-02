# Creates symlinks. Be careful, this will delete existing.

ln -sfn `readlink -f useful_commands.txt` ~/useful_commands.txt
ln -sfn `readlink -f bash_aliases` ~/.bash_aliases
ln -sfn `readlink -f Preferences.sublime-settings` ~/.config/sublime-text-3/Packages/User/Preferences.sublime-settings
ln -sfn `readlink -f pythonrc` ~/.pythonrc
