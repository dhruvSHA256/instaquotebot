#!/bin/bash
# vim: filetype=bash

# set -eu pipefail

# [ -z "$1" ] && echo "Usage: ${0##*/} args" && exit 1

export DISPLAY=:0
export XAUTHORITY=$HOME/.config/X11/Xauthority
\cd /home/dhruv/repo/igquotes
env python /home/dhruv/repo/igquotes/genimage.py && env python /home/dhruv/repo/igquotes/postinsta.py && dunstify posted
