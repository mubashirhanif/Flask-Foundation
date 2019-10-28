 
#!/usr/bin/env bash

echo "Waiting for MySQL..."

while ! nc -z database 3306; do
  sleep 0.5
done

echo "MySQL started"

cd /app

./manage.py createdb

./manage.py server