#!/bin/sh
wget https://github.com/PrestaShop/ps_cashondelivery/releases/download/v2.0.1/ps_cashondelivery.zip -O /var/www/html/modules/ps_cashondelivery.zip
unzip /var/www/html/modules/ps_cashondelivery.zip -d /var/www/html/modules/
rm /var/www/html/modules/ps_cashondelivery.zip
sed -i "/'welcome',/a 'ps_cashondelivery'," /var/www/html/src/PrestaShopBundle/Install/Install.php
