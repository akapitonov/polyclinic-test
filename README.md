# Polyclinic
*Django сервис, организующий запись к врачу на прием в поликлиннику.*

##Тестирование
[![Build Status](https://travis-ci.org/notsnake/polyclinic-test.svg?branch=master)](https://travis-ci.org/notsnake/polyclinic-test)

**Версия python: 3**


Порядок работы с приложением
------------
- Создать файл с настройками для проекта на основе: polyclinic/settings/dev.py и далее в инструкции везде заменить dev на имя своего файла,
    если файл не будет создан следует использовать файл dev.py
- Создать базу данных, для этого выполнить все миграции: ./manage.py migrate --settings=polyclinic.settings.dev
- Создать пользователя - администратора сайта: ./manage.py createsuperuser --settings=polyclinic.settings.dev
- Для начала работы, через web-интерфейс django/admin нужно добавить список врачей, которые осуществляют прием.
- Запуск django-приложения: ./manage.py runserver --settings=polyclinic.settings.dev
- Запуск тестов: coverage run --source=. manage.py test -v 2 --settings=polyclinic.settings.dev
- Сформировать отчет по результатам тестов командой: coverage html, просмотреть результаты тестов можно в каталоге htmlcov, в том числе процентный показатель покрытия тестами исходного кода.

Запуск приложения в docker
------------

- Для запуска приложения в docker-container нужно создать docker-compose.yml и сначала собрать образ:
    docker-compose build web, а потом запустить: docker-compose up, для примера выложил свой docker-compose в репозиторий
- Для запуска тестов в контейнере, сначала нужно подключиться к нему с помощью команды: docker exec -it CONTAINER bash и затем запустить тесты способом указаннаом в разделе выше.
