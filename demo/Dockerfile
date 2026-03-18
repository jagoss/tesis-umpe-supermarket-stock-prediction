FROM nginx:alpine
COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY index.html /usr/share/nginx/html/index.html.template
COPY assets/ /usr/share/nginx/html/assets/
CMD ["/bin/sh", "-c", "envsubst '${ONYX_WIDGET_API_KEY}' < /usr/share/nginx/html/index.html.template > /usr/share/nginx/html/index.html && nginx -g 'daemon off;'"]
