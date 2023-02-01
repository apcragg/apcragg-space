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

dir=$(dirname "$(readlink -f -- "$0")")

echo_em "Generating SSL certificates and keys"
run_sudo openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout $dir/ssl/privkey.pem -out $dir/ssl/fullchain.pem -config $dir/ssl/localhost.conf -subj "/"

echo_em "Generating Diffie Helman key"
run_sudo openssl dhparam -out $dir/ssl/dhparam.pem 2048
