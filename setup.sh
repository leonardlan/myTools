# Creates symlinks. Be careful, this will delete existing.

ln -sfn `realpath useful_commands.txt` ~/useful_commands.txt
ln -sfn `realpath install_my_stuff.txt` ~/install_my_stuff.txt
ln -sfn `realpath bash_aliases` ~/.bash_aliases
ln -sfn `realpath Preferences.sublime-settings` ~/.config/sublime-text-3/Packages/User/Preferences.sublime-settings
ln -sfn `realpath pythonrc` ~/.pythonrc
