
### Начало разработки

Зайти в корневую директорию проекта  
(ту, в которой лежат файлы `manage.py`, `package.json` etc).

Нужен установленный `poetry` (pip install poetry).

Далее активировать окружение: `poetry shell`.

Я всё делал на `python 3.10`, но с другими не слишком старыми тоже должно быть всё ок.

(Можно poetry установить не глобально, тогда окружение активировать,
например, так: `python -m venv .venv`, затем `source .venv/bin/activate`
на Windows последнее немного по-другому, что-то типа `.venv/bin/activate.bat`.

Далее установить зависимости бэка: `poetry install`  
Далее зависимости фронта: `yarn install` или `npm install`  

Создать файл локальных настроек (по нему приложение определит, что сервер локальный):  
`touch gn/local_settings.py` (на Windows м.б. touch нет, не знаю, просто руками как-то создать тогда).

Миграции (сейчас используется база sqlite, создаётся в корне проекта):  
`python manage.py migrate`

Запуск локального сервера для разработки:  
`yarn run serve`

Далее зайти на http://127.0.0.1:8000  
Показан пример использования компонента React,
получение данных с бэка через REST-api,
передачи данных в HTML с бэка,
используются стили из .scss-файла.


### Структура директорий проекта

Структура директорий сейчас типовая для Django, кроме:
- фронт в папке `front` (прописано в `vite.config.ts`)
- роутинг Django Rest Framework (DRF) подключается во внешнем `urls.py` (`gn/urls.py`),
  это позволяет DRF автоматически формировать URL-ы в некоторых местах
- вьюсеты DRF расположены сейчас в `main/api`, сериализаторы в `main/serializers`


### Разработка автоматически встраиваемых компонентов React

1. Создать во `front/js/components/root` файл компонента по аналогии с `hw.tsx`
2. В html создать тег, в котором будет прописано наименование этого файла: `<div data-js-component="hw">Loading...</div>`
   в этот тег компонент автоматически встроится после готовности DOM.
