certbot:
    image: certbot/certbot:latest
    command: certonly --webroot --webroot-path=/var/www/html --email margaret.meek@gmail.com --agree-tos --no-eff-email -d mmldemo.com 
    volumes:
      - /home/ubuntu/certbot/conf:/etc/letsencrypt
      - /home/ubuntu/certbot/logs:/var/log/letsencrypt
      - /home/ubuntu/certbot/data:/var/www/html
    depends_on:
      - nginx

sudo docker run -it --rm --name certbot \
            -v "/home/ubuntu/certbot/conf:/etc/letsencrypt" \
            -v "/home/ubuntu/certbot/data:/var/lib/letsencrypt" \
            -p 80:80
            certbot/certbot certonly
