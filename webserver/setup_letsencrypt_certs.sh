#!/bin/bash

echo_em() {
  if [ -z "$2" ] ; then
    CHAR="-"
  else
    CHAR=$2
  fi
  printf -- "$CHAR%.0s" {1..80}
  echo ""
  echo "$1"
  printf -- "$CHAR%.0s" {1..80}
  echo ""
}

# Wrapper for running functions as sudo
run_sudo() {
  echo "Running: $*"
  sudo "$@"
}

echo_em "This does nothing right now"
