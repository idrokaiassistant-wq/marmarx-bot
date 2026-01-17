# frontend/Dockerfile
FROM nginx:alpine

# Frontend fayllarini Nginx papkasiga ko'chirish
COPY . /usr/share/nginx/html

# Nginx sozlamasini ulash
COPY nginx.conf /etc/nginx/conf.d/default.conf
