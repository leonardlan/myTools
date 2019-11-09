#!/usr/bin/env bash

# Set MY_WS variable
MY_WSS=$MY_WSS:~/dev/workspace:~/dev
for path in ${MY_WSS//:/ }; do
    if [ -d "$path" ]; then
        MY_WS=$path
        break
    fi
done

if [ -d ~/dev/sandbox ]; then
    MY_SB=~/dev/sandbox
elif [ -d ~/sandbox ]; then
    MY_SB=~/sandbox
fi

echo_and_run () { echo "\$ $*" ; "$@" ; }

alias ls='ls --color=auto'
alias l='ls -lh'
alias h='history'
alias py='python'
alias p='python' # Everyday, I get a little bit lazier
alias fp='readlink -f'

# How lazy am I?
alias u='cd ..'
alias uu='cd ../..'
alias uuu='cd ../../..'
alias uuuu='cd ../../../..'
alias uuuuu='cd ../../../../..'

alias a='alias'  # Aliasception
complete -a a

alias less='less -R'    # Color me less

# Prints pwd relative to home dir in bold blue
alias _pwd_nice='printf "\033[1;34m`dirs +0`\n\033[0m"'

runmeindirs () { for d in ./*/ ; do (cd "$d" && echo && _pwd_nice && $@); done }

# Case-insensitive file/folder search
f () { find . -iname "*$@*" | grep -i --color=auto $@; }
g () {
    grep -nr --exclude=\*.{jpg,png} "$@" 2>/dev/null
}

alias find-executables-recursively='find . -type f -perm /u=x,g=x,o=x -exec ls -l {} \;'
alias find-images-recursively='find ./ -type f \( -iname \*.jpg -o -iname \*.jpeg -o -iname \*.png -o -iname \*.exr -o -iname \*.tiff -o -iname \*.gif -o -iname \*.bmp \)'

hs () { h | grep "$@"; }

# Command search
cs () { compgen -c | sort | grep "$@"; }

es () { env | grep "$@"; }
complete -v es

psa () { ps aux | grep "$@"; }

complete -a alias
complete -a unalias

numfiles () {
    N="$(ls $1 | wc -l)";
    echo "$N files in $1";
}

# Change to workspace
ws () { cd $MY_WS/$1; }
_ls_ws_dirs () {
    local cur="${COMP_WORDS[COMP_CWORD]}"
    COMPREPLY=( $(compgen -W "`ls -F $MY_WS | grep /`" -- ${cur}) )
}
complete -F _ls_ws_dirs ws

# Change to sandbox
sb () {
    # Ask to create directory if not exist
    if [ ! -d $MY_SB/$1 ]
    then
        read -p "Directory $1 does not exist. Create one? (y/n) " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]
        then
            mkdir $MY_SB/$1
        else
            return
        fi
    fi
    cd $MY_SB/$1;
}
_ls_sb_dirs () {
    local cur="${COMP_WORDS[COMP_CWORD]}"
    COMPREPLY=( $(compgen -W "`ls -F $MY_SB | grep /`" -- ${cur}) )
}
complete -F _ls_sb_dirs sb

# Backup file or dir using cp
function backup() {
    for var in "$@"
    do
        cmd="cp -r $var $var.backup_$(date +%F_%T)"
        echo $cmd
        $cmd
    done
}

alias myTools='cd ${MYTOOLS}'

# Git
alias gg='git gui &'
alias gs='git st'
alias gsa='for d in $MY_WS/*/ ; do (cd "$d" && _pwd_nice && git st); done'
alias gd='git diff'
alias gb='git branch'
alias gac="git add . && git commit -m" # + commit message
alias gp="git push"
alias gl="git pull"
alias gpom="git push origin master"
alias glom="git pull origin master"
alias gmom="git merge origin/master"
alias git-show-devs='git shortlog -sn'
alias git-show-origin='git remote show origin'
alias git-show-top-level='realpath --relative-to=`pwd` "$(git rev-parse --show-toplevel)"'
alias git-current-branch="git branch | grep \* | cut -d ' ' -f2"
alias git-stash-show='git stash show -p'

alias c='xclip -sel clip'
alias ea='vim ~/.bash_aliases'
alias sa='for f in ~/.bash_aliases*; do source $f; done'
alias tree='tree -C'

alias s='~/sublime_text_3/sublime_text'

# Debugging
alias tf='tail -f'

# View env var split by semicolon
listenv () {
    var_name=$1
    sed "s/:/\n/g" <<< "${!var_name}"
}
complete -v listenv

# Kill process
alias ks='kill -9'
alias pk='killall -9'
alias pkp='pk python'
alias pkt='pk tail'

# Django
alias migrate='python manage.py migrate'
alias makemigrations='python manage.py makemigrations'
alias rs='python manage.py runserver &'
alias createsuperuser='python manage.py createsuperuser'
alias collectstatic='python manage.py collectstatic'
alias djshell='python manage.py shell'

# Testing
alias nt='nosetests $@; ns'

# Python
which_python () {
python - <<EOF
import $@
for attribute in ["__file__", "__path__", "__version__"]:
    try:
        print attribute, "=", getattr($@, attribute)
    except AttributeError, e:
        print e
EOF
}
alias start_python_service='python -m SimpleHTTPServer & google-chrome 0.0.0.0:8000'

alias clean='find . -name "*.pyc" -delete'

# Prints path to file color-indicating up to where it exists
lssmart () {
    for file in "$@"
    do
        exists=$file
        while [[ $exists && ! -d $exists ]] ; do
            exists=$(dirname "${exists}")
        done
        if [[ -d $exists ]] ; then
            echo -e "\e[1m\e[34m$exists\e[31m${file/$exists/}\e[39m\e[0m"
        fi
    done
}

# Virtualenv
alias srcvirtualenv='
if [ -f /usr/bin/virtualenvwrapper.sh ]; then
    echo_and_run source /usr/bin/virtualenvwrapper.sh
fi

if [ -f ~/.local/bin/virtualenvwrapper.sh ]; then
    echo_and_run source ~/.local/bin/virtualenvwrapper.sh
fi'


####################
# Mock render jobs #
####################
# Randomly succeed or fail
alias true-or-false='if ((RANDOM % 2)); then echo_and_run true; else echo_and_run false; fi;'

# Never ends
alias infinite-loop='while true; do date; sleep 1; done'

# Sleeps for 1-60 seconds
sleeper () {
    SECONDS_TO_SLEEP=$(((RANDOM % 60) + 1))
    date
    echo Sleeping for $SECONDS_TO_SLEEP seconds zzz...
    sleep $SECONDS_TO_SLEEP
    echo "Yawn! I'm done now!"
}


###########
# My docs #
###########
alias useful-commands='vim ${MYTOOLS}/docs/useful_commands.md'


######################
# 3rd party software #
######################
alias ho='houdini &'
alias k='katana &'
alias m='maya &'
alias n='nuke &'
