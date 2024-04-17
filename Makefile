start:
	sudo docker compose up --build

migrate:
	sudo docker exec -it sso  python manage.py migrate

migrations:
	sudo docker exec -it sso  python manage.py makemigrations

attach:
	sudo docker attach sso

shell:
	sudo docker exec -it sso sh

superuser:
	sudo docker exec -it sso python manage.py createsuperuser

test:
	sudo docker exec -it sso  python manage.py test

generate_key:
	sudo docker exec -it sso python manage.py gen_key
