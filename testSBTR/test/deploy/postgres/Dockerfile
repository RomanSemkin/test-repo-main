ARG VERSION

FROM postgres:${VERSION}

COPY --chown=root:postgres ./deploy/postgres/docker-entrypoint-initdb.sh /docker-entrypoint-initdb.d/docker-entrypoint.sh
RUN chmod 0150 /docker-entrypoint-initdb.d/docker-entrypoint.sh

