echo "Running Database Migrations"

python manage.py makemigrations 
python manage.py migrate

if [ $(($1 = "user")) ]; then
    python manage.py createsuperuser
fi

if [ $(($1 = "run" )) ]; then 
    python manage.py runserver
fi

exec "$@"