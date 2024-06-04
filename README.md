# CRM-система для бизнеса

![Static Badge](https://img.shields.io/badge/python-3.10.12-blue?style=for-the-badge) ![Static Badge](https://img.shields.io/badge/django-5.0.1-blue?style=for-the-badge) ![Static Badge](https://img.shields.io/badge/drf-gray?style=for-the-badge) ![Static Badge](https://img.shields.io/badge/postgresql-14.11-blue?style=for-the-badge) ![Static Badge](https://img.shields.io/badge/nginx-1.26.0-blue?style=for-the-badge) ![Static Badge](https://img.shields.io/badge/docker-gray?style=for-the-badge)

#### Данная crm-система предназначена для:
* Создания и учета новых лидов (заявок)
* Постановка задач для обработки каждого нового лида
* Ведение статистики количества новых лидов / сделок / продаж
* Осуществление контроля за работой менеджеров (что лид создан, задачи новому лиду поставлены, задачи своевременно выполняются)

#### Краткая инструкция по использованию сервиса:
* Создаем новый лид (Меню - Создать лида). Попадаем на страницу нового лида.
* Создаем лиду задачу (кнопка Добавить задачу). Например, "Позвонить". 
* Допустим, звонок был успешный (инфомацию о звонке указываем в комментарии). Нажимаем кнопку "Завершить и создать новую" - текущую задачу мы завершаем и открылось окно для новой задачи - запланировали следущую задачу на другое число и нажали "Создать задачу". В указаный день запланированная задача у нас высветится в разделе меню "Задачи".
* Ежедневно менеджер работает с разделом меню "Задачи" - в нем все задачи на сегоднящний день и плюс просроченные, если есть. В этом разделе можно перейти на страницу Лида, для которого поставлена задача и в его профиле посмотреть историю задач (история касаний/взаимодействия), чтобы понимать, на каком этапе находится данный лид. В задаче нажимаем Редактировать и алгоритм действий см. выше.
* Задачи лиду ставятся до тех пор, пока он не купит или пока не будет отказа.
* Если лид купил (состоялась сделка), на странице Лида в разделе Сделки нажимаем "Добавить сделку", в ней указываем "Наименование сделки", "Сумму" и сохраняем.
* В разделе меню "Воронка продаж" можно посмотреть статистику по Лидам/Сделкам/Продажам за выбранный период.
* В меню сайта есть возможность поиска лида по номеру телефона (если поступает звонок, можно найти данного человека в базе и перейти к нему на страницу, чтобы посмотреть информацию и данном лиде).

#### Развертывание проекта на локальном сервере:
* Клонируем репозиторий
  ```
  git clone https://github.com/NikitaBogush/crm-system
  ```
* Переходим в папку с проектом
  ```
  cd crm-system
  ```
* Запускаем docker-compose
  ```
  docker compose up -d
  ```
* Выполняем миграции
  ```
  docker compose exec web python manage.py migrate
  ```
* Создаем суперпользователя
  ```
  docker compose exec web python manage.py createsuperuser
  ```
* Собираем статику
  ```
  docker compose exec web python manage.py collectstatic --no-input
  ```
* Проект доступен по адресу
  ```
  http://localhost/
  ```