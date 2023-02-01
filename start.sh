#!/bin/bash
# Basic script to get development environment set up.
# Developed on Ubuntu 22.04 on AMR64 platform. Not tested on other platforms.

set -o errexit

display_line() {
  if [ -z "$2" ] ; then
    CHAR="-"
  else
    CHAR=$2
  fi
  printf -- "$CHAR%.0s" {1..80}
  echo ""
}

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

find_pluto() {
  PLUTO_URI=$(iio_info -s | sed -rEn 's/^.*\[(usb.*)]/\1/p')
  export PLUTO_URI
  if [[ ${#PLUTO_URI} -gt 0 ]]; then
    echo "Found PlutoSDR at '$PLUTO_URI'"
  else
    echo "Did not find a PlutoSDR"
  fi
}

end_running_container() {
  echo "Currently running containers:"
  running_containers=$(docker ps | sed -rEn 's/^.*\s(.*)\s/\1/p' | tail +2)
  if [[ ${#running_containers} -gt 0 ]]; then
     echo "$running_containers"
  else
    echo "Found no running containers"
  fi

  display_line '-'
  echo "Stopping containers"
  docker compose down
}

# ============================================================================
# Run commands to start application
# ============================================================================
echo_em "Setting up environment"
echo "Looking for PlutoSDR"
find_pluto

echo_em "Ending running containers"
end_running_container

echo_em "Build Frontend Bundle"
# Print output if build command has error
output="$(npm install --prefix ./webserver) 2>&1" || echo "$output"
output="$(npm run build --prefix ./webserver) 2>&1" || echo "$output"

echo_em "Building Frontend and Backend Containers"
# Print output if build command has error
output="$(docker compose build) 2>&1" || echo "$output"

echo_em "Environment Settings"
cat .env

echo_em "Deploying Containers"
docker compose up
