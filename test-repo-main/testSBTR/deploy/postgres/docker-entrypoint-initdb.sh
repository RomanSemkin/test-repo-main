#!/bin/bash

echo "host replication all 0.0.0.0/0 md5" >> "$PGDATA/pg_hba.conf"
set -e
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
CREATE USER $POSTGRES_STANDBY_USER REPLICATION LOGIN ENCRYPTED PASSWORD '$POSTGRES_STANDBY_PASSWORD';
EOSQL

exec "$@"
