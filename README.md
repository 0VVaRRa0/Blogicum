# Blogicum

## Описание проекта
Социальная сеть для публикации постов. Пользователи имеют возможность зарегистрироваться, войти в аккаунт, создавать и изменять посты, а также оставлять комментарии.

## Использованные технологии
- Python 3.9
- Django 3.2.16


## Запуск проекта локально
1. Клонируйте репозиторий `https://github.com/0VVaRRa0/django_sprint4.git`
2. Создайте и активируйте виртуальное окружение `python -m venv venv`    
Bash: `source venv/Scripts/activate`, PowerShell: `venv/Scripts/activate`
4. Выполните миграции `python manage.py migrate`
5. По желанию, загрузите фикстуры с заготовленными постами `python manage.py loaddata db.json`
6. Запустите сервер разработки `python manage.py runserver`

Проект доступен локально по адресу `localhost:8000` или `127.0.0.0:8000`

## Автор: Иван Данилин
GitHub: [0VVaRRa0](https://github.com/0VVaRRa0)    
Gmail: vvarra.work@gmail.com
