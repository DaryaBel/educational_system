## Технологии

- Vue
- Webpack
- Django
- Sentry
- Docker
- Docker-Compose
- Nginx
- Git (Github)
- Mailhog
- Graphql

## Использование

Установите [Docker](https://docs.docker.com/install/) и [Docker-Compose](https://docs.docker.com/compose/). Запустите виртуальные контейнеры с помощью следующей команды:

docker-compose up --build

Если всё работает отлично, вам необходимо создать суперпользователя для админпанели с помощью следующей команды:

docker-compose run backend python manage.py createsuperuser
