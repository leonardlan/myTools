#!/bin/bash
# Changes desktop wallpaper to random picture in ~/Pictures

# Need to set DBUS_SESSION_BUS_ADDRESS for dconf to work
PID=$(pgrep mate-session)
export DBUS_SESSION_BUS_ADDRESS=$(grep -z DBUS_SESSION_BUS_ADDRESS /proc/$PID/environ|cut -d= -f2-)

random_pic=`shuf -n1 -e $HOME/Pictures/*`
dconf write /org/mate/desktop/background/picture-filename "'${random_pic}'"
