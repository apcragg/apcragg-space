FROM nginx:1.23.3

COPY ./nginx.conf /etc/nginx/nginx.conf
COPY ./default-selfsigned.conf.template /etc/nginx/templates/default.conf.template
COPY ./dist/ /usr/share/nginx/default/
