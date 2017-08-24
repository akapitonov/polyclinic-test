Python(3)

Django сервис, организующий запись к врачу на прием в поликлиннику.

Для начала работы, через django/admin нужно добавить список врачей, которые осуществляют прием.

Порядок работы с приложением:

1. Создать файл с настройками для проекта на основе: polyclinic/settings/dev.py и далее в инструкции заменить dev на имя своего файла.
Если файл не создан слудет использовать файл dev.py

2. Создать базу данных, для этого выполнить все миграции: ./manage.py migrate --settings=polyclinic.settings.dev

3. Создать пользователя - администратора сайта: ./manage.py createsuperuser --settings=polyclinic.settings.dev

4. Через web-интерфейс django/admin добавить докторов, которые будут осуществлять прием

5.1 Для запуска приложения в docker-container нужно создать docker-compose.yml и сначала собрать образ:
    docker-compose build web, а потом запустить: docker-compose up

5.2 Для обычного запуска можно воспользоваться командой: ./manage.py runserver --settings=polyclinic.settings.dev

6. Тесты запускаются командой: coverage run --source=. manage.py test -v 2 --settings=polyclinic.settings.dev, для просмотра отчета выполнить команду:
    coverage html, в директории с проектом будут доступны отчеты в каталоге: htmlcov.
    Для запуска тестов в контейнере, сначала нужно подключиться к нему с помощью команды: docker exec -it CONTAINER bash
