FROM nginx:1.23.3

COPY nginx.conf /etc/nginx/nginx.conf
COPY apcragg-space /etc/nginx/sites-enabled/
COPY dist/ /usr/share/nginx/apcragg-space/
COPY static /usr/share/nginx/apcragg-space/static
