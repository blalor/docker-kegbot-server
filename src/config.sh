#!/bin/bash

set -e -x -u

cd /tmp/src

mv nginx.repo /etc/yum.repos.d/

## kegbot requires python >= 2.7
## it also requires a LOCAL redis install. (╯°□°）╯︵ ┻━┻ 
##   https://github.com/Kegbot/kegbot-server/issues/254
yum install -y centos-release-SCL mysql-devel gcc git nginx redis
yum install --disablerepo=* --enablerepo=scl -y python27-python-devel python27-python-setuptools

mv nginx.conf /etc/nginx/
mv supervisor-kegbot.conf /etc/supervisor.d/
mv program-*.conf /etc/supervisor.d/
mv kegbot_wrapper.sh /usr/local/bin/

## gotta be a better way
export LD_LIBRARY_PATH="$( scl enable python27 'echo ${LD_LIBRARY_PATH}' )"
export PATH="$( scl enable python27 'echo ${PATH}' )"
export PKG_CONFIG_PATH="$( scl enable python27 'echo ${PKG_CONFIG_PATH}' )"

easy_install-2.7 pip

## need version with patched status api endpoint
pip2.7 install git+https://github.com/Kegbot/kegbot-server.git@104a47f257dba1285c0a1cacaf5062254b9d2e02#egg=kegbot

mkdir -p /var/lib/kegbot/redis /etc/kegbot /var/log/kegbot
chown nobody:nobody /var/lib/kegbot /etc/kegbot /var/log/kegbot

## init settings
# runuser -s /bin/bash - nobody -c 'scl enable python27 "/opt/rh/python27/root/usr/bin/setup-kegbot.py \
#     --nointeractive \
#     --verbose \
#     --data_root=/var/lib/kegbot \
#     --settings_dir=/etc/kegbot \
#     "'

mv local_settings.py /etc/kegbot/

## fix up redis config file
sed -i \
    -e 's#daemonize yes#daemonize no#' \
    -e 's#^dir /var/lib/redis/#dir /var/lib/kegbot/redis/#' \
    -e 's#/var/log/redis/redis.log#/var/log/kegbot/redis.log#' \
    /etc/redis.conf

## cleanup
cd /
yum clean all
rm -rf /var/tmp/yum-root* /tmp/src
