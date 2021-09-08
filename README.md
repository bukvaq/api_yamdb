# api_yamdb
Проект YaMDb собирает отзывы пользователей на различные произведения.
***
### Возможности:
* Регистрация (по ник-нейму и электронной почте)
* Получение токена (по ник-нейму и коду подтверждения почты)
* Написание отзыва для произведений 
* Оценка произведений по шкале от 1 до 10
* Комментирование отзыва
* Админ может создавать/удалять жанры, категории, произведения
* Админ может назначать модераторов из пользователей
***
### Как запустить проект:
```
https://github.com/EugeneSal/https:/github.com/EugeneSal/api_yamdb.git
```
Создать и активировать виртуальное окружение:
```
python -m venv env

source venv/bin/activate
```
Обновить pip
```
python -m pip install --upgrade pip
```
Установить зависимости из файла requirements.txt:
```
pip install -r requirements.txt
```
Выполнить миграции:
```
python manage.py migrate
```
Запустить сервер:
```
python manage.py runserver
```
Ссылка на локальный сервер:
http://127.0.0.1:8000/

Документация доступна по адресу:
http://127.0.0.1:8000/redoc/
***
### Пример работы API:

Запрос для создания поста:
```python
import requests
from pprint import pprint
url = 'http://127.0.0.1:8000/api/v1/categories/'
request = requests.get(url).json()
pprint(request)
```
Ответ от API:
```json
{'count': 3,
 'next': None,
 'previous': None,
 'results': [{'name': 'Фильм', 'slug': 'movie'},
             {'name': 'Книга', 'slug': 'book'},
             {'name': 'Музыка', 'slug': 'music'}]}
```
***
## Авторы проекта:
#### * Дарья Понамарёва
#### * Евгений Салахутдинов
#### * Максим Шамшурин
***