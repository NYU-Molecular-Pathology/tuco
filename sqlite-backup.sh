#!/bin/bash
# Backup a SQLite file contents
timestamp="$(date '+%Y-%m-%d-%H-%M-%S')"
db_dir="db"
backup_dir="${db_dir}/backups"

db_file="${1}"
backup_file="${backup_dir}/$(basename "${db_file}").${timestamp}.backup.gz"

mkdir -p "${backup_dir}"

sqlite3 "${db_file}" .dump | gzip > "${backup_file}"
# sqlite3 "${db_file}" .backup > "${backup_file}"
