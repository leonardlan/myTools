# Creates symlinks. Be careful, this will delete existing.

ln -sfn `readlink -f my_bashrc` ~/.my_bashrc
ln -sfn `readlink -f useful_commands.txt` ~/useful_commands.txt
ln -sfn `readlink -f bash_aliases` ~/.bash_aliases
ln -sfn `readlink -f Preferences.sublime-settings` ~/.config/sublime-text-3/Packages/User/Preferences.sublime-settings
ln -sfn `readlink -f pythonrc` ~/.pythonrc

add_line_to_file() {
    grep -qF -- "$1" "$2" || echo "$1" >> "$2"
}

# Add source line to .bashrc file if not existing
add_line_to_file 'source ~/.my_bashrc' ~/.bashrc

# Add cron job
crontab -l > /tmp/mycron
add_line_to_file "0 9-18 * * 1-5 /home/llan/myTools/notify-time.sh > /dev/null 2>&1 # Notify me every so often" /tmp/mycron
crontab /tmp/mycron
rm /tmp/mycron
