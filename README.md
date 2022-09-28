# Сервис рассылки сообщений

Сервис оплаты заказов (DJANGO + Stripe).
Добавление товаров и заказов в базу данных возможно как через сервис API, так и через админку, доступную по адресу:
http://localhost:8000/admin

***

## Краткая инструкция по запуску

1. Склонируйте проект в локальный репозиторий

2. Откройте файл docker-compose.yml и добавьте в services: web: environment: API_KEY (Ваш приватный ключ) 
для работы платежной системы Stripe+

3. Установите приложение Docker (если оно не было установлено ранее) и запустите его

4. В терминале: перейдите в корневую директорию проекта payment_servise

5. Введите команду:

```
docker-compose up
```

***

### Для создания учетной записи панели администратора:

 - войдите в контейнер web. Введите в терминале:
 ```
 docker exec -it <id контейнера> bash 
 ```
  > - посмотреть id всех контейнеров (там найти и скопировать нужный), можно командой:
  > ```
  > docker ps -a
  > ```
 - находясь внутри контейнера, введите команду:
 ```
 python manage.py createsuperuser
 ```
 + Далее введите имя пользователя, эл.почту(не обязательно) и пароль.

 - Для выхода и контейнера выполните команду:
 ```
 exit
 ```

 ***

## Работа с API

Сервис API расположен по адресу:

```
http://localhost:8000/api
```
Просмотр и добавление товаров:
```
http://localhost:8000/api/item/
```
Изменение и удаление товара:
```
http://localhost:8000/api/item/<id товара>/
```
Просмотр и добавление заказов:
```
http://localhost:8000/api/order/
```
Добавление товаров в заказ, изменение и удаление товаров в заказе:
```
http://localhost:8000/api/order/<id заказа>/
```
Переход к оплате заказа:
```
http://localhost:8000/buy/<id заказа>/
```

### Для тестирования платежной системы используйте номер карты:
> 4242 4242 4242 4242

Подробнее на странице документации [Stripe](https://stripe.com/docs/testing)


<details>
<summary>Открыть описание технического задания:</summary>

[Ссылка на задание](https://docs.google.com/document/d/1RqJhk-pRDuAk4pH1uqbY9-8uwAqEXB9eRQWLSMM_9sI/edit?usp=sharing)

## Описание
stripe.com/docs - платёжная система с подробным API и бесплатным тестовым режимом для имитации и тестирования платежей. С помощью python библиотеки stripe можно удобно создавать платежные формы разных видов, сохранять данные клиента, и реализовывать прочие платежные функции.  
Мы предлагаем вам познакомиться с этой прекрасной платежной системой, реализовав простой сервер с одной html страничкой, который общается со Stripe и создает платёжные формы для товаров.   
Для решения нужно использовать Django. Решение бонусных задач даст вам возможность прокачаться и показать свои умения, но это не обязательно.  
Задание

## Задача
Реализовать Django + Stripe API бэкенд со следующим функционалом и условиями:
- Django Модель Item с полями (name, description, price)
- API с двумя методами:
  - GET /buy/{id}, c помощью которого можно получить Stripe Session Id для оплаты выбранного Item. При выполнении этого метода c бэкенда с помощью python библиотеки stripe должен выполняться запрос stripe.checkout.Session.create(...) и полученный session.id выдаваться в результате запроса
  - GET /item/{id}, c помощью которого можно получить простейшую HTML страницу, на которой будет информация о выбранном Item и кнопка Buy. По нажатию на кнопку Buy должен происходить запрос на /buy/{id}, получение session_id и далее  с помощью JS библиотеки Stripe происходить редирект на Checkout форму stripe.redirectToCheckout(sessionId=session_id)
  - Пример реализации можно посмотреть в пунктах 1-3 тут
- Залить решение на Github, описать запуск в Readme.md
- Опубликовать свое решение чтобы его можно было быстро и легко протестировать. Решения доступные только в виде кода на Github получат низкий приоритет при проверке.

## Бонусные задачи
- Запуск используя Docker
- Использование environment variables
- Просмотр Django Моделей в Django Admin панели
- Запуск приложения на удаленном сервере, доступном для тестирования
- Модель Order, в которой можно объединить несколько Item и сделать платёж в Stripe на содержимое Order c общей стоимостью всех Items
- Модели Discount, Tax, которые можно прикрепить к модели Order и связать с соответствующими атрибутами при создании платежа в Stripe - в таком случае они корректно отображаются в Stripe Checkout форме. 
- Добавить поле Item.currency, создать 2 Stripe Keypair на две разные валюты и в зависимости от валюты выбранного товара предлагать оплату в соответствующей валюте
- Реализовать не Stripe Session, а Stripe Payment Intent.

</details>

---
