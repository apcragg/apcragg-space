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

# echo_em "Generating SSL certificates and keys"
# run_sudo openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout $dir/ssl/privkey.pem -out $dir/ssl/fullchain.pem -config $dir/ssl/localhost.conf -subj "/"

# Source local environment variables
. $dir/../.env

######################
# Become a Certificate Authority
######################
echo_em "Becoming Certificate Authority"

# Generate private key
openssl genrsa -des3 -passout pass:$ROOT_PASS -out $dir/ssl/my_ca.key 2048
run_sudo chmod 644 $dir/ssl/my_ca.key
# Generate root certificate
openssl req -x509 -new -nodes -passin pass:$ROOT_PASS -key $dir/ssl/my_ca.key -sha256 -days 825 -out $dir/ssl/my_ca.pem -subj "/CN=localhost/O=Astranis/OU=NetOps"

######################
# Create CA-signed certs
######################
echo_em "Generating Self-signed SSL certificates and keys"

NAME=$NGINX_HOSTNAME # Use your own domain name
# Generate a private key
openssl genrsa -out $dir/ssl/$NAME.key 2048
# Create a certificate-signing request
openssl req -new -key $dir/ssl/$NAME.key -out $dir/ssl/$NAME.csr -config $dir/ssl/localhost.conf -subj "/CN=localhost/O=Astranis/OU=NetOps"

# Create a config file for the extensions
>$dir/ssl/$NAME.ext cat <<-EOF
authorityKeyIdentifier=keyid,issuer
basicConstraints=CA:FALSE
keyUsage = digitalSignature, nonRepudiation, keyEncipherment, dataEncipherment
subjectAltName = @alt_names
[alt_names]
DNS.1 = $NAME
EOF
# Create the signed certificate
openssl x509 -req -in $dir/ssl/$NAME.csr -passin pass:$ROOT_PASS -CA $dir/ssl/my_ca.pem -CAkey $dir/ssl/my_ca.key -CAcreateserial \
-out $dir/ssl/$NAME.crt -days 825 -sha256 -extfile $dir/ssl/$NAME.ext

echo_em "Generating Diffie Helman key"
run_sudo openssl dhparam -out $dir/ssl/$NAME.dhparam.pem 2048
