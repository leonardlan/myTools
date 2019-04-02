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

alias ls='ls --color=auto'
alias l='ls -lh'
alias h='history'
alias py='python'
alias fp='readlink -f'
alias u='cd ..'
alias uu='cd ../..'
alias uuu='cd ../../..'
alias uuuu='cd ../../../..'
alias uuuuu='cd ../../../../..'

runmeindirs () { for d in ./*/ ; do (cd "$d" && echo && pwd && $@); done }

f () { find . -name "*$@*" | grep $@; }
g () { grep -nr --exclude=\*.{jpg,png} "$@"; }
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

function backup() {
    for var in "$@"
    do
        cmd="cp -r $var $var.backup_$(date +%F_%T)"
        echo $cmd
        $cmd
    done
}

alias myTools='cd ~/myTools'

# Git
alias gg='git gui &'
alias gs='git st'
alias gsa='for d in $MY_WS/*/ ; do (cd "$d" && pwd && git st); done'
alias gd='git diff'
alias gb='git branch'
alias showtoplevel='realpath --relative-to=`pwd` "$(git rev-parse --show-toplevel)"'
alias showorigin='git remote show origin'
alias gac="git add . && git commit -m" # + commit message
alias gp="git push"
alias gl="git pull"
alias gpom="git push origin master"
alias glom="git pull origin master"
alias gitshowdevelopers='git shortlog -sn'

alias c='xclip -sel clip'
alias ea='vim ~/.bash_aliases'
alias sa='for f in ~/.bash_aliases*; do source $f; done'
alias tree='tree -C'
ns () {
    notify-send -i face-smile-big "Done!" "$@";
    play -q ~/myTools/sounds/quite-impressed.ogg &
}

alias subl='~/sublime_text_3/sublime_text'

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

# Django
alias migrate='python manage.py migrate'
alias makemigrations='python manage.py makemigrations'
alias rs='python manage.py runserver &'
alias createsuperuser='python manage.py createsuperuser'
alias collectstatic='python manage.py collectstatic'
alias djshell='python manage.py shell'

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
alias start_python_service='python -m SimpleHTTPServer &'

alias clean_pyc_files='find . -name "*.pyc" -delete'

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
