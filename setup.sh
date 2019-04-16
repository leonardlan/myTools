# Creates symlinks. Be careful, this will delete existing.

# Make sandbox dir
mkdir -p ~/dev/sandbox

ln -sfn `readlink -f bash_aliases` ~/.bash_aliases
ln -sfn `readlink -f gitconfig` ~/.gitconfig
ln -sfn `readlink -f gitignore_global` ~/.gitignore_global
ln -sfn `readlink -f my_bashrc` ~/.my_bashrc
ln -sfn `readlink -f pythonrc` ~/.pythonrc
ln -sfn `readlink -f useful_commands.txt` ~/useful_commands.txt

# Setup my sublime prefs
ln -sfn `readlink -f Preferences.sublime-settings` ~/.config/sublime-text-3/Packages/User/Preferences.sublime-settings
ln -sfn "`readlink -f 'Default (Linux).sublime-keymap'`" ~/.config/sublime-text-3/Packages/User/'Default (Linux).sublime-keymap'
ln -sfn `readlink -f sublime/snippets/python_class.sublime-snippet` ~/.config/sublime-text-3/Packages/User/python_class.sublime-snippet
ln -sfn `readlink -f sublime/snippets/python_function.sublime-snippet` ~/.config/sublime-text-3/Packages/User/python_function.sublime-snippet
ln -sfn `readlink -f sublime/snippets/python_function_simple.sublime-snippet` ~/.config/sublime-text-3/Packages/User/python_function_simple.sublime-snippet
ln -sfn `readlink -f sublime/snippets/python_docstring.sublime-snippet` ~/.config/sublime-text-3/Packages/User/python_docstring.sublime-snippet

add_line_to_file() {
    grep -qF -- "$1" "$2" || echo "$1" >> "$2"
}

# Add source line to .bashrc file if not existing
add_line_to_file 'source ~/.my_bashrc' ~/.bashrc

# Add cron job
crontab -l > /tmp/mycron
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
add_line_to_file "0 9-18 * * 1-5 ${DIR}/notify-time.sh > /dev/null 2>&1 # Notify me every so often" /tmp/mycron
crontab /tmp/mycron
rm /tmp/mycron
echo "New crontab:"
crontab -l

# Install python packages
pip install -r requirements.txt
