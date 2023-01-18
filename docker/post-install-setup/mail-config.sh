#!/bin/sh
sed -i "254s/.*/\$options \= array_merge(\$options, array('ssl' => array('allow_self_signed' => true, 'verify_peer' => false)));/" /var/www/html/vendor/swiftmailer/swiftmailer/lib/classes/Swift/Transport/StreamBuffer.php

rm -rf /var/www/html/mails/pl /var/www/html/mails/themes
tar xvf /tmp/mail_tpl.tar.gz -C /var/www/html/mails
rm /tmp/mail_tpl.tar.gz
