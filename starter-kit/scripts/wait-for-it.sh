#!/usr/bin/env bash
set -e
host="$1"
shift
until nc -z ${host%:*} ${host#*:}; do
  sleep 1
done
exec "$@"
