FROM nginx:1.23.3

COPY ./nginx.conf /etc/nginx/nginx.conf
COPY ./default.conf.template /etc/nginx/templates/default.conf.template
COPY ./default-nossl.conf.template /etc/nginx/templates/default-nossl.conf.template
COPY ./dist/ /usr/share/nginx/default/
COPY ./ssl /ssl/

ARG NGINX_USE_TLS
RUN if [ $NGINX_USE_TLS -eq 1 ] ; then \
        rm /etc/nginx/templates/default-nossl.conf.template ; \
    else \
        mv /etc/nginx/templates/default-nossl.conf.template /etc/nginx/templates/default.conf.template ; \
    fi
