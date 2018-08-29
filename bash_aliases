export MY_DEV=~/dev

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
f () { find . -name "*$@*" | grep --color $@; }
g () { grep -nr --color "$@"; }

complete -a alias

# Change to workspace
ws() { cd $MY_DEV/$1; }
_ls_dev_dirs () {
    local cur="${COMP_WORDS[COMP_CWORD]}"
    COMPREPLY=( $(compgen -W "`ls -D $MY_DEV`" -- ${cur}) )
}
complete -F _ls_dev_dirs ws

function backup() {
    for var in "$@"
    do
        cmd="mv $var $var.backup_$(date +%F_%T)"
        echo $cmd
        $cmd
    done
}

# Git
alias gg='git gui &'
alias gsa='for d in $MY_DEV/*/ ; do (cd "$d" && pwd && git st); done'

alias c='xclip -sel clip'
alias ea='vim ~/.bash_aliases'
alias sa='source ~/.bash_aliases; source ~/.bash_aliases_airbud'
alias tree='tree -C'
alias ns='notify-send "Done" "I am done!"'

alias subl='~/sublime_text_3/sublime_text'

# View env var split by semicolon
listenv () { sed "s/:/\n/g" <<< "$@"; }

# Kill process
alias pk='killall -9'
alias pkp='pk python'

# Django
alias migrate='python manage.py migrate'
alias makemigrations='python manage.py makemigrations'
alias rs='python manage.py runserver &'
alias createsuperuser='python manage.py createsuperuser'

# Python
which_python () {
python - <<EOF
import $@
for attribute in ["__file__", "__version__"]:
    try:
        print attribute, "=", getattr($@, attribute)
    except AttributeError, e:
        print e
EOF
}

alias clean_pyc_files='find . -name "*.pyc" -delete'
