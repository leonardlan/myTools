<title>Useful Commands</title>

# Useful Commands

My useful commands that I can't seem to remeber. :thinking_face:

## Git
```bash
# Run git status in all directories in ~/dev/
for dir in ~/dev/*/ ; do (cd "$dir" && pwd && git st); done

# View origin
git remote show origin

# To delete a local branch
git branch -d the_local_branch

# Remove remote branch
git push origin --delete the_remote_branch

# Show which files have changed betwen two revisions
git diff --name-status master..branchName

# Amend last commit without changing message
git add <files>
git commit --amend --no-edit

# Amend last commit message
git commit --amend

# View the content of the most recent stash
git stash show -p

# View the content of an arbitrary stash
git stash show -p stash@{1}

# Show all users and the number of commits
git shortlog -sn

# Show top-level directory
git rev-parse --show-toplevel

# Squash last 2 commits into one
git rebase -i HEAD~2

# Go back 1 commit (Warning: cannot undo)
git reset --hard HEAD~1

# Revert to previous commit (that was already pushed) in a new commit
git revert COMMIT_HASH

# Fetch/merge
git fetch
git merge origin/master

# Cherry-pick commit
git cherry-pick <commit>
# Cherry-pick but don't commit
git cherry-pick -n <commit>
```


## Shell
```bash
# Copy command output to clipboard with pipe
xclip -sel clip

# Get last system reboot
uptime -s

# Get reboot history
last reboot | head -10
```

### Compgen: List All Available Commands
```bash
# List all commands
compgen -c

# List all aliases
compgen -a

# List all built-ins
compgen -b

# List all keywords
compgen -k

# List all functions
compgen -A functio
```

### Pipes (Redirecting Output)
```bash
# Redirect error message to NUL
command args 2> nul

# Redirect output to one place and errors to another
command args > output.log 2> error.log
```

### Miscellaneous
```bash
# cd into all directories and run a command
for d in ./*/ ; do (echo $d && cd "$d" && somecommand); done
```


## Files And Directories
```bash
# Make multiple directories in one go
mkdir ~/projects/{bin,pkg,src}

# Find number of files in current folder
find . -type f | wc -l

# View long list for a single directory
l -d dir

# List by last modified
l -tr

# Query number of files open limited by OS
ulimit -n

# Set number of files limited by OS
ulimit -n 2048

# Query number of files limit by process
prlimit -n -p PID

# Set number of files limit by process
prlimit --nofile=4096 -p PID

# Rename multiple files (Red Hat; CentOS)
# Fix the extension of HTML files so that all .htm files have a four-letter .html suffix
rename .htm .html *.htm

# Remove string (remove_me) in file names
rename remove_me '' *

# List files recursively modified in last 24 hours
find . -mtime -1 -print

# Keep last 1,000 lines of file (will overwrite existing)
echo "$(tail -1000 my_super_huge.log)" > my_super_huge.log
```

## Syncing files and folders
```bash
# Copy directory across hosts
scp -r . USER@HOST:/PATH/TO/DESTINATION_FOLDER

# Copy one single local file to a remote destination
scp /PATH/TO/SOURCE_FILE USER@HOST:/PATH/TO/DESTINATION_FOLDER/

# Copy one single file from a remote server to your current local server
scp USER@HOST:/PATH/TO/SOURCE_FILE /PATH/TO/DESTINATION_FOLDER

# Copy one single file from a remote server to another remote server
scp USER1@SERVER1:/PATH/TO/SOURCE USER2@server2:/PATH/TO/DESTINATION/

# Copy multiple files with one command
scp file1.txt file2.txt file3.txt USER@HOST:/PATH/TO/DESTINATION/
```

### Rsync
```bash
# Copy a Directory from Local Server to a Remote Server
rsync -avz source_dir/ USER@IP_ADDRESS:/dest/dir/
```

## Installing packages
### yum
```bash
yum install PACKAGE
yum update PACKAGE
yum info PACKAGE
yum list available

# Install from file
sudo yum -y install $(install_my_stuff.txt)
```

### pip
```bash
# Install package for specific user **in home directory** (without sudo)
pip install --user PACKAGE

# Show info about package
pip show PACKAGE_NAME

# Show all package versions
pip freeze

# Upgrade pip
pip install --upgrade pip

# Uninstall package
pip uninstall PACKAGE_NAME

```

## Backing up files
```bash
# Backup file with date and time in filename (file.txt.backup_2018-08-03_12:51:34)
mv file.txt file.txt.backup_$(date +%F_%T)
```

## Permissions
```bash
# View mask
umask
umask -S

# Give permission recursively
sudo chmod -Rvf 755

# Check if user is sudo
sudo -l -U USER

# Add user to sudoers
sudo usermod -aG wheel USER

# Log in as root
sudo su -

# Change file owner
chown USER:GROUP FILE
```

## Symbolic link
```bash
    ln -s link_from link_to
    unlink LINK_NAME
    rm LINK_NAME
```

## Ports and processes
```bash
# Check listening ports and applications
sudo netstat -tulpn | grep LISTEN
```

## Cron jobs
```bash
crontab -e  # Edit crontab file, or create one if it doesn’t already exist.
crontab -l  # crontab list of cronjobs, display crontab file contents.
crontab -r  # Remove your crontab file.
```

See [crontab.guru](https://crontab.guru) for crontab notation.


## Images
```bash
# Get info about image
identify

# List all images recursively
find . -name '*' -exec file {} \; | grep -o -P '^.+: \w+ image'

# Converting
# Convert jpg to pn
convert img.jpg img.png

# Convert multiple jpg to png
mogrify -formt png *.jpg

# Convert exr to png while maintaining format
convert input.exr -colorspace RGB -colorspace sRGB output.png

# Resize image
convert img.png -resize 16x16 img.png
```

## Regex
```regex
(?# Line without word)
^((?!word).)*$

(?# Matching square brackets! Ha! Genius!)
\[([^]]+)\]

(?# Positive lookbehind and lookahead)
(?:^|(?<= ))(words|I|want|to|find)(?:(?= )|$)

(?# Negative lookbehind)
(?<= )

(?# Positive lookahead)
(?=\t)

(?# Remove unnecessary whitespace)
[\t ]+$

(?# Remove trailing)
[\t\n ]{2,}\Z => \n
```

## Users And Groups
```bash
# See which user/process is using a file
fuser -u FILE

# List all local users
cat /etc/passwd

# Add user
adduser username

# Remove user
userdel USER

# Remove user and user directory
userdel -r USER

# Sign in as another user
su - USER

# Add account for user
sudo chsh -s /bin/bash USER

# Change user home directory
usermod -d /new/home user

# List all groups
cat /etc/group

# Change group
chgrp GROUP FILENAME

# Add existing user to existing group
sudo usermod -aG GROUP USER

# print real and effective user and group IDs
id USER
```

## Web dev
### Django
```bash
# Create app
python manage.py startapp polls

# Takes migration names and returns their SQL
python manage.py sqlmigrate APP VERSION

# Makemigrations
python manage.py makemigrations

# Migrate
python manage.py migrate
python manage.py migrate --run-syncdb

# Runserver
python manage.py runserver &
python manage.py runserver 0.0.0.0:8080 &

# Shell
python manage.py shell

# Run a script
python manage.py shell < myscript.py

# Create super user
python manage.py createsuperuser
python manage.py createsuperuser --email=admin@gmail.com

# Run test
python manage.py test APP

# Delete all migration files
find . -iname '*migrations' | xargs rm -rf

# Generate requirements.txt
pipreqs /path/to/project

# Install requirements in file
pip install -r requirements.txt
```

> **_NOTE:_**  If server code is not updating with apache when you edit .py files, try `touch wsgi.py`, which will tell it to recompile .py files

### Python
```bash
# Start service
python -m SimpleHTTPServer
```

## Servers
### Apache
```bash
apachectl status
apachectl restart
apachectl stop
apachectl start

# check version
httpd -v

# Enable the Apache service so that it starts automatically at boot
sudo systemctl enable httpd
```

### Systemctl
```bash
sudo systemctl start httpd
sudo systemctl restart httpd
sudo systemctl stop httpd

# Check status
systemctl status httpd

# View today's logs
journalctl -u service_name.service --since today

# Remove service
systemctl stop SERVICENAME
systemctl disable SERVICENAME
rm /etc/systemd/system/SERVICENAME
systemctl daemon-reload
systemctl reset-failed
```

### Nginx
Access and error logs: `/var/log/nginx/`

## Virtual environment
```bash
# Create a Python virtual environment
virtualenv VIR_ENV_NAME

# Activate
source /path/to/env/bin/activate

deactivate
```

### [virtualenvwrapper](https://python-guide-cn.readthedocs.io/en/latest/dev/virtualenvs.html#virtualenvwrapper)
```bash
lsvirtualenv -b
mkvirtualenv VIR_ENV_NAME
workon VIR_ENV_NAME
lssitepackages
deactivate
rmvirtualenv VIR_ENV_NAME
```

## Password
```bash
# Change password for user
sudo passwd USER

# No password
sudo passwd -d USER
```

## Mounting and unmounting
```bash
# View fstab file
cat /etc/fstab

# Refresh /etc/fstab file
sudo mount -a

# Unmount
umount PATH_TO_DIR

# View mount info
nfsstat -m
```

## Databases
### MySQL server
```bash
# Start server
sudo /etc/init.d/mysql start

# Connect to server from shell
mysql -u USER -p DATABASE_NAME
mysql -u root -p ftta_application

# Source sql file from mysql shell
source FILE_NAME;

# Configuration file
/etc/mysql/my.cnf
```

### Postgres
```bash
# Open db in command line
sudo -u postgres psql -U postgres -d DATABASE_NAME

# Dump out your file
sudo -u postgres psql DATABASE_NAME > file.backup

# Repopulate empty db with export file
sudo -u postgres psql DATABASE_NAME < file.backup

# Alternative way to pg_dump/restore
pg_dump DATABASE_NAME > db.sql
pg_restore -d newdb db.sql

# Restart server
sudo /etc/init.d/postgresql restart

# Drop database
sudo -u postgres psql postgres -c "DROP DATABASE DATABASE_NAME"

# Create database
sudo -u postgres psql postgres -c "CREATE DATABASE DATABASE_NAME"

# Add hstore extension
sudo -u postgres psql postgres -d DATABASE_NAME -c "CREATE EXTENSION IF NOT EXISTS hstore;"
```

### sqlite
```bash
# Backup
sqlite3 my_database.sq3 ".backup 'backup_file.sq3'"

# Print the database structure
.schema

# Print database structure and data
.dump
```

## SSH
```bash
# Known hosts file
~/.ssh/known_hosts

# Launch gui from remote (Enables X11 forwarding)
ssh -X MACHINE_NAME

# ssh into machine and cd to directory
ssh -t MACHINE_NAME "cd /var/log ; bash"
```

## SELinux
```bash
# Check status
sestatus

# Disable SE Linux
setenforce 0 
```


## Find out where a command is
```bash
which
whereis
```

## Memory
```bash
# View machine RAM
free -mh

# View size of directories
du -shc *

# View `du -h` sorted by size
du -hs * | sort -h

# `du` on steroids
ncdu
```

## Nosetests
```bash
# Show print messages
nosetests --nocapture

# Test specific function
nosetests tests/test_backrefs.py:TestBackrefs.test_backref

# Test with execution time per test
nosetests --with-timer
```

## Processes
```bash
# List open files
lsof -p PROCESS_ID

# View environment variables of a running process
cat /proc/PID/environ
```

## htop shortcuts
| Shortcut Key | Function Key |       Description        |
|--------------|--------------|--------------------------|
| h            | F1           | Invoke htop Help         |
| S            | F2           | Htop Setup Menu          |
| /            | F3           | Search for a Process     |
| I            | F4           | Invert Sort Order        |
| t            | F5           | Tree View                |
| >            | F6           | Sort by a column         |
| [            | F7           | Nice – (change priority) |
| ]            | F8           | Nice + (change priority) |
| k            | F9           | Kill a Process           |
| q            | F10          | Quit htop                |


## Setuptools
```bash
# Install
python setup.py install

# Record a list of installed files
python setup.py install --record files.txt

# Remove installed files
cat files.txt | xargs rm -rf
```

## gdb
`gdb -p PID`

| Command    |                       Description                                |
|------------|------------------------------------------------------------------|
| b main     | Puts a breakpoint at the beginning of the program                |
| b          | Puts a breakpoint at the current line                            |
| b N        | Puts a breakpoint at line N                                      |
| b +N       | Puts a breakpoint N lines down from the current line             |
| b fn       | Puts a breakpoint at the beginning of function "fn"              |
| d N        | Deletes breakpoint number N                                      |
| info break | list breakpoints                                                 |
| r          | Runs the program until a breakpoint or error                     |
| c          | Continues running the program until the next breakpoint or error |
| f          | Runs until the current function is finished                      |
| s          | Runs the next line of the program                                |
| s N        | Runs the next N lines of the program                             |
| n          | Like s, but it does not step into functions                      |
| u N        | Runs until you get N lines in front of the current line          |
| p var      | Prints the current value of the variable "var"                   |
| bt         | Prints a stack trace                                             |
| u          | Goes up a level in the stack                                     |
| d          | Goes down a level in the stack                                   |
| q          | Quits gdb                                                        |
| attach ID  | Attaches to process with process ID                              |
| detach     | Detaches from current attached process                           |


## OpenEXR
```bash
# A utility for modifying OpenEXR standard attributes
exrstdattr

# Show file format version, channels contained, compression type, data window, display window, line, pixel aspect ratio, and the center and width of the screen window for a given OpenEXR file(s).
exrinfoorder

# Takes a collection of EXR images and outputs them as a single EXR with all channels combined, for use with denoise.
exrmergesuitable

# View headers
exrheader
```

## Terminal Mail
```bash
# Launch Terminal app
mail

# Commands
? delete *
? q
```

## NVidia
```bash
# View memory usage, GPU utilization, and temperature of GPU
nvidia-smi
```

## Misc
```bash
# Unzip tar.gz
tar -zxvf
```
