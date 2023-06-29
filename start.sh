docker-compose up -d

if [ ! -d "pgdata" ]; then
  sleep 10
  db_container=$(docker-compose ps -q db)
  docker exec -it $db_container bash -c 'su - postgres -c "psql --dbname=cafehunt -f /docker-entrypoint-initdb.d/dump.sql"'
fi
