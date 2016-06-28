#! /usr/bin/env bash

if [ -n "$HOME" ]; then
    path=$HOME/.aria2/aria2.conf
elif [ -n "$XDG_CONFIG_HOME" ]; then
    path=$XDG_CONFIG_HOME/.aria2/aria2.conf
else
    echo "No home path available. Exiting..."
    exit
fi

home=${path%.aria2/aria2.conf}

mkdir -p $(dirname $path)

envsubst < aria2.conf > $path
