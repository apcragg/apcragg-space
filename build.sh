#!/bin/bash
# Basic script to get development environment set up.
# Developed on Ubuntu 22.04 on AMR64 platform. Not tested on other platforms.

set -o errexit
set -o pipefail

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

echo_em "WARNING: This script does nothing right now"
