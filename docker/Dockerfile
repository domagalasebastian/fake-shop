FROM prestashop/prestashop:1.7

COPY ./pre-install-setup/* /tmp/pre-install-scripts/
COPY ./post-install-setup/* /tmp/post-install-scripts/
COPY ./mail_tpl.tar.gz /tmp/mail_tpl.tar.gz
COPY ./img /var/www/html/img

RUN chmod -R 777 /tmp/post-install-scripts /tmp/pre-install-scripts/
RUN chmod -R 777 /var/www/html/img 

