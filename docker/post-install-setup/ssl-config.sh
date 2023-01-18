#!/bin/sh
echo "[ req ]\ndistinguished_name       = req_distinguished_name\nextensions               = v3_ca\nreq_extensions           = v3_ca\n\n[ v3_ca ]\nbasicConstraints         = CA:TRUE\n\n[ req_distinguished_name ]\ncountryName              = Country Name (2 letter code)\ncountryName_default      = PL\ncountryName_min          = 2\ncountryName_max          = 2\norganizationName         = Organization Name (eg, company)\norganizationName_default = StrefaKursow\n" >> /etc/apache2/cert.conf

openssl req -x509 -nodes -days 366 -newkey rsa:2048 -keyout /etc/ssl/private/apache-selfsigned.key -out /etc/ssl/certs/apache-selfsigned.crt -subj "/C=PL/ST=Mazury/L=Wegorzewo/O=StrefaKursow/OU=StrefaKursow/CN=localhost" -config /etc/apache2/cert.conf

sed -i 's/ssl-cert-snakeoil.pem/apache-selfsigned.crt/g' /etc/apache2/sites-available/default-ssl.conf
sed -i 's/ssl-cert-snakeoil.key/apache-selfsigned.key/g' /etc/apache2/sites-available/default-ssl.conf
a2enmod ssl
a2ensite default-ssl
