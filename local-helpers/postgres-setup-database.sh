docker-compose down
docker-compose up -d postgres
sleep 1
docker-compose exec postgres psql -U postgres -tc "SELECT 1 FROM pg_database WHERE datname = 'article'" | grep -q 1 || docker-compose exec postgres psql -U postgres -c "CREATE DATABASE article"
