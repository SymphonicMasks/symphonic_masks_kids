## Инструкция по запусу: 

- `pip install -r requirements.txt`
- `cd kids_app`
- `pip install -r requirements.txt`
- `python manage.py makemigrations`
- `python manage.py migrate`
- `python manage.py runserver`

## Инструкция Docker compose: 
- docker build
- docker-compose up
- http://127.0.0.1:8000/upload/
  
## Для тестирования
- открываем ссылку `http://127.0.0.1:8000/upload/`
- загружаем аудио файл
- сайт перенаправляет на страницу в виде `http://127.0.0.1:8000/song/1`
- смотрим на результат :) 
