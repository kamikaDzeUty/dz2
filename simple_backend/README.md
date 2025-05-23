# Задачи
**Во всех заданиях обязательно создание pull-request по аналогии из задачи блока git!**

**Ваш код обязательно должен запускаться и проверяться на работоспособность**
## Задание 1
Нужно локально запустить backend приложение. Пройдитесь по шагам:
1. Если еще не склонирован этот репозиторий, то склонируйте
2. Создайте в папке `simple_backend/src/task_tracker` виртуальное окружение
3. Активируйте `venv`
4. Установите записимости из `requirements.txt`
5. Запустите сервер с помощью команды `uvicorn main:app`
6. Перейдите по ссылке http://127.0.0.1:8000/docs и проверьте, что бэк работает
## Задание 2
Вам нужно оживить бекенд из первой задачи и создать простой API для управления списком задач. Данные нужно хранить в оперативной памяти (например в списке Python).
В каждой из функций нужно прописать логику:
- get_tasks должен возвращать список всех задач
- create_task должен создавать новую задачу
- update_task должен обновлять информацию о задаче
- delete_task должен удалять задачу

У задачи должны быть параметры: id, название, статус задачи.

### Подзадачи
- Прочитайте, что такое "Хранение состояния", создайте в task_tracker readme.md файл и напишите в чём минусы подхода с хранением задач в оперативной памяти (списке python)
- Исправьте ситуацию и переделайте хранение информации о задачах в файле проекта. Информацию можно хранить например в формате json.
- Напишите в readme.md:
    - что улучшилось после того, как список из оперативной памяти изменился на файл проекта?
    - избавились ли мы таким способом от хранения состояния или нет?
    - где еще можно хранить задачи и какие есть преимущества и недостатки этих подходов?
- Напишите класс для работы с файлом хранения задач в task_tracker и измените код проекта так, чтобы он работал с объектом этого класса.
- Сделайте свой backend - stateless с помощью интеграции с облачным сервисом (jsonbin.io, mockapi.io, github gist). Организуйте хранение и обновление json файла во внешнем сервисе.
- Прочитайте что такое "состояние гонки" и напишите в readme файле о том, какие проблемы остались в бекенде на данном этапе проекта. Есть ли у вас какое-то решение этой проблемы?


## Задание 3
Давайте прокачаем наш таск-треккер. Хочется, чтобы текст задачи заливался в LLM модель и она выдавала способы решения задачи и добавляла к её тексту.
Для того, чтобы это сделать:
- Настройте интеграцию с сервисом [Cloudflare](https://developers.cloudflare.com/workers-ai/get-started/rest-api/) через REST API. Для этого создайте новый класс для работы с этой API.
- При создании новой задачи отправляйте запрос с её текстом в LLM и просьбой объяснить как решать задачу
- Добавляйте полученный ответ в текст задачи

## Задание 4
Заметили, что в коде для работы с файлами и в коде для работы с LLM API есть похожие участки? Давайте избавимся от дублирования через наследование.
- Сделайте базовый класс BaseHTTPClient и вынесите в него общие функции и методы из двух классов
- Сделайте наследование от базового класса в клиентах
- С помощью абстрактных классов реализуйте абстрактные методы, которые должны быть в классах наследниках
