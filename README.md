
## env vars

* `KEGBOT_DEBUG` -- set to `true` to enable
* `KEGBOT_DB_NAME`
* `KEGBOT_DB_HOST`
* `KEGBOT_DB_USER`
* `KEGBOT_DB_PASSWORD`

If using email:

* `KEGBOT_EMAIL_FROM`
* `KEGBOT_EMAIL_HOST`
* `KEGBOT_EMAIL_PORT` -- defaults to `25`
* `KEGBOT_EMAIL_USER`, `KEGBOT_EMAIL_PASSWORD` -- optional; defaults to no auth
* `KEGBOT_EMAIL_USE_SSL` -- defaults to `False`
* `KEGBOT_EMAIL_USE_TLS` -- defaults to `False`

## initial setup

requires volume, which does not exist in container.  written to by `nobody` user
in container, id `99`.  set perms appropriately.

    mkdir -p /path/to/data/dir/{static,media,redis}
    chown -R nobody:nobody /path/to/data/dir

create mysql database, then:

    docker run -i -t \
        -e KEGBOT_DB_NAME=kegbot \
        -e KEGBOT_DB_HOST=10.0.1.3 \
        -e KEGBOT_DB_USER=root \
        -e KEGBOT_DB_PASSWORD= \
        -e KEGBOT_DEBUG=true \
        -v /path/to/data/dir:/var/lib/kegbot \
        -u nobody \
        blalor/kegbot-server \
        /usr/local/bin/kegbot_wrapper.sh syncdb --all --noinput -v 0

    docker run -i -t \
        -e KEGBOT_DB_NAME=kegbot \
        -e KEGBOT_DB_HOST=10.0.1.3 \
        -e KEGBOT_DB_USER=root \
        -e KEGBOT_DB_PASSWORD= \
        -e KEGBOT_DEBUG=true \
        -v /path/to/data/dir:/var/lib/kegbot \
        -u nobody \
        blalor/kegbot-server \
        /usr/local/bin/kegbot_wrapper.sh migrate --all --fake --noinput -v 0

    docker run -i -t \
        -e KEGBOT_DB_NAME=kegbot \
        -e KEGBOT_DB_HOST=10.0.1.3 \
        -e KEGBOT_DB_USER=root \
        -e KEGBOT_DB_PASSWORD= \
        -e KEGBOT_DEBUG=true \
        -v /path/to/data/dir:/var/lib/kegbot \
        -u nobody \
        blalor/kegbot-server \
        /usr/local/bin/kegbot_wrapper.sh collectstatic --noinput

complete setup wizard.  kegbot doesn't appear to honor the port when proxied
through nginx, so you'll need to run this thing on port 80.  start kegbot
container:

    docker run -i -t \
        -e KEGBOT_DB_NAME=kegbot \
        -e KEGBOT_DB_HOST=10.0.1.3 \
        -e KEGBOT_DB_USER=root \
        -e KEGBOT_DB_PASSWORD= \
        -e KEGBOT_DEBUG=true \
        -v /path/to/data/dir:/var/lib/kegbot \
        -p 80:80 \
        blalor/kegbot-server

then visit `http://localhost/`
