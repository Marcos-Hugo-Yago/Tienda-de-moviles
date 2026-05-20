FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
    apt-get install -y \
        apache2 \
        libapache2-mod-security2 \
        libapache2-mod-evasive \
        openssl \
        ca-certificates \
        curl \
    && rm -rf /var/lib/apt/lists/*

RUN a2enmod ssl proxy proxy_http proxy_fcgi headers security2 evasive rewrite

RUN mkdir -p /etc/apache2/ssl && \
    openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
        -keyout /etc/apache2/ssl/private.key \
        -out /etc/apache2/ssl/certificate.crt \
        -subj "/C=ES/ST=Madrid/L=Madrid/O=Grupo5peps/OU=PEPS/CN=localhost"

RUN cp /etc/modsecurity/modsecurity.conf-recommended /etc/modsecurity/modsecurity.conf && \
    sed -i 's/SecRuleEngine DetectionOnly/SecRuleEngine On/' /etc/modsecurity/modsecurity.conf && \
    sed -i 's/SecResponseBodyAccess On/SecResponseBodyAccess Off/' /etc/modsecurity/modsecurity.conf

COPY modsecurity_rules.conf /etc/modsecurity/custom_rules.conf
COPY modsecurity_crs/REQUEST-900-EXCLUSION-RULES-BEFORE-CRS.conf /etc/modsecurity/crs/REQUEST-900-EXCLUSION-RULES-BEFORE-CRS.conf

RUN mkdir -p /var/log/modsecurity && chmod 755 /var/log/modsecurity && \
    mkdir -p /var/log/mod_evasive && chmod 777 /var/log/mod_evasive

COPY security.conf /etc/apache2/conf-available/security-custom.conf
COPY mod_evasive.conf /etc/apache2/mods-available/evasive.conf
COPY 000-default.conf /etc/apache2/sites-available/000-default.conf

RUN a2enconf security-custom && \
    echo "ServerName localhost" >> /etc/apache2/apache2.conf

COPY ./static/ /var/www/html/
RUN chmod -R a+rX /var/www/html/

EXPOSE 80 443
CMD ["apachectl", "-D", "FOREGROUND"]
