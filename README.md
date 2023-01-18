# Andrew's Webserver
Runs a variety of microservices in docker containers. Developed on an ARM based Rasberry Pi 4. No promises this works on other platforms.

## Install instructions
- `./build_setup.sh`
- `./bootstrap`

## Network Setup
This project runs an nginx webserver on `localhost:9042`. You have a few options for accessing the server

### Local Access
Navigate your browser to `localhost:9042`. No other changes should be neccessary.

### External Access
This section is a work in progress. In short you need to:
- Get a domain and point it to the server running this webpage
  - If you run this from a typical residential internet connection, your server is likely behind your router's NAT and assigned a local IP address. The router's address is likely DHPC assigned by the ISP and is likely to change from time to time. You will need to run something like `dyndns` to periodically update your DNS record with your DHCP assigned address.
  - You will additionally need to setup your routers NAT to send traffic coming from Port 80 to the local IP address of your server at Port 9042
- Get an SSL certificate using a tool like `certbot`
  - These instructions are a WIP

## Start Server
- `docker compose up` to start the webserver and other services
- `docker compose down` to stop all services

## Developing
Run `./bootstrap` regularaly to stay up to date on Python dependenceis
