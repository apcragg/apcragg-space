#!/bin/bash
# Basic script to get development environment set up.
# Developed on Ubuntu 22.04 on AMR64 platform. Not tested on other platforms.

set -o errexit
set -o pipefail

# Minimal docker image might need this
LINUX_PACKAGES="lsb-release"
# Packages to install on Linux.
LINUX_PACKAGES+=" build-essential clang-format libusb-dev cmake libtool automake pkg-config"
# Get important python packages
LINUX_PACKAGES+=" python3 python3-pip python3-venv python3-tk"
LINUX_PACKAGES+=" python3-protobuf"
# Docker prerequisites 
LINUX_PACKAGES+=" apt-transport-https ca-certificates curl software-properties-common"

# PIP Packages
PIP3_PACKAGES="coloredlogs"

echo_em() {
  if [ -z "$2" ] ; then
    CHAR="-"
  else
    CHAR=$2
  fi
  for i in {1..80}; do echo -n $CHAR; done
  echo ""
  echo $1
  for i in {1..80}; do echo -n $CHAR; done
  echo ""
}

linux_check_if_all_packages_installed() {
  local pkg
  for pkg in $@; do
    if ! dpkg -s "$pkg" >/dev/null 2>/dev/null; then
      echo "$pkg not installed"
      return 1
    fi
  done
  return 0
}

# Verify docker install by running example image
docker_check() {
  if ! run_sudo systemctl status docker | grep "active (running)">/dev/null 2>/dev/null; then
      echo "Docker not running properly."
      exit 1
  fi

  if ! run_sudo docker run hello-world | grep "Hello from Docker!" >/dev/null 2>/dev/null; then
      echo "Docker not configbured properly."
      exit 1
  fi
}

# Setup docker permissions
setup_sudoless_docker() {
  run_sudo usermod -aG docker ${USER}
}

install_pip_pkgs() {
  if [[ -n "${VIRTUAL_ENV}" ]]; then
    echo_em "Please deactive virtual environment before running this script."
    exit 1
  fi
  pip3 install --quiet --user ${PIP3_PACKAGES}
}

install_nginx() {
 NGINX_PKG="nginx"
 if linux_check_if_all_packages_installed $NGINX_PKG; then
  echo_em "Nginx already installed"
 else
 run_sudo apt-get install --yes $NGINX_PKG 
 fi
}

install_docker() {
  DOCKER_PKG="docker-ce"
  DOCKER_COMPOSE_PKG="docker-compose-plugin"
  GROUP="docker"

  if linux_check_if_all_packages_installed $DOCKER_PKG $DOCKER_COMPOSE_PKG; then
    echo_em "Docker packages already installed"
  else
    # Get easy setup script
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --yes --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
    # Add docker repo to sources
    echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
    # Update and ensure we install from correct source
    run_sudo apt-get update
    run_sudo apt-cache policy $DOCKER_PKG
    # Install docker engine
    run_sudo apt-get install $DOCKER_PKG --yes
    # Instlal docker compose plugin
    run_sudo apt-get install --yes docker-compose-plugin
  fi
  docker_check  

  if id -nG "$USER" | grep -qw "$GROUP"; then
    :
  else
    echo $USER does not belong to $GROUP
    setup_sudoless_docker
  fi
  echo_em "Docker is setup correctly"
}

# Checks that we are not running as root.
verify_not_root() {
  if [ "$(id -u)" == "0" ]; then
    echo_em 'You should run this script as a regular user, not root.' "@"
    exit 1
  fi
}

verify_not_venv() {
  if [[ -n "${VIRTUAL_ENV}" ]]; then
    echo
    echo_em "ERROR You are using a virtual environment, please deactivate!" "@"
    echo
    exit 1
  fi
}

# Wrapper for running functions as sudo
run_sudo() {
  echo "Running: $@"
  sudo "$@"
}

install_linux() {
  if linux_check_if_all_packages_installed $LINUX_PACKAGES; then
    echo_em "All Linux packages already installed"
  else
    run_sudo apt-get update
    run_sudo ACCEPT_EULA=Y apt-get --yes install $LINUX_PACKAGES
  fi
}

# Run install functions
verify_not_root
verify_not_venv
install_linux
install_pip_pkgs
install_docker
install_nginx