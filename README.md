# Andrew's Webserver
Runs a variety of microservices in docker containers. Developed on an ARM based Rasberry Pi 4. No promises this works on other platforms.

## Install instructions
- `./build_setup.sh`
- `./bootstrap`

## Configuration
- The `.env` file stores a few configuration settings
- Default config runs the server on `localhost:8080` without TLS

## Start Server
- `./start.sh` to start the webserver and other services
- `docker compose down` to stop all services

### Local Access
Navigate your browser to `http://localhost:8080`. No other changes should be neccessary.

### External Access
This section is a work in progress. In short you need to:
- Get a domain and point it to the server running this webpage
  - If you run this from a typical residential internet connection, your server is likely behind your router's NAT and assigned a local IP address. The router's address is likely DHPC assigned by the ISP and is likely to change from time to time. You will need to run something like `dyndns` to periodically update your DNS record with your DHCP assigned address.
  - You will additionally need to setup your routers NAT to send traffic coming from Port 80 to the local IP address of your server at Port 9042
- Get an SSL certificate using a tool like `certbot`
  - These instructions are a WIP
  
### Self Signed Cert
- Don't do this, but if you want to do this, run 
```
export ROOT_PASS=<insert your pass>
./webserver/generate_local_certs.sh
```
- Set `NGINX_USE_TLS=0` in `.env` file

## Developing
Run `./bootstrap` regularaly to stay up to date on Python dependenceis
