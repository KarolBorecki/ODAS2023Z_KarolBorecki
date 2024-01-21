FROM byjg/nginx-extras

RUN rm /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/conf.d

COPY cert.pem /etc/nginx/cert.pem
COPY key.pem /etc/nginx/key.pem