#!/usr/bin/env bash

# Notify me the time

# Need this for notify-send to work in cron job
export DISPLAY=:0.0
export XAUTHORITY=/home/llan/.Xauthority

hour=`date +%-l`
msg="It's $hour o'clock!"

case "$hour" in
    9) msg+=" Good morning!";;
    1) msg+=" Time for lunch?";;
    5) msg+=" Almost done!";;
    6) msg+=" Time to go!";;
    *) msg+=" Drink some water!"
esac

notify-send -i face-laugh 'Hey!' "$msg"
play `dirname $0/`/sounds/quite-impressed.ogg
