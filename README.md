# Микросервис по работе с VK

## Работающий функционал

* Авторизация пользователя
* Получение access и refresh токенов
* Обновление access токена по refresh токену
* Инвалидация токена
* Получение информации по пользователю (Имя, Статус, Количество постов, Количество подписчиков, Количество видео, Количество лайков, комментариев и просмотров каждого видео)


### Автор backend Артём Куликов

tg: [@Berg1005](https://t.me/berg1005)

[GitHub](https://github.com/berg96)

## Используемые технологии 

Проект реализован на языке python c использованием следующего технгологического стека:

* FastAPI
* Uvicorn
* httpx
* Pydantic

## Как запустить проект

Клонировать репозиторий:
```
git clone https://github.com/berg96/microserviceVK_testtask_InvestEra.git
```
Перейти в него в командной строке:
```
cd product_sales_testtask_InCodeWeTrust
```
Создать файл .env с актуальными переменными окружения по примеру .env_example

Для получения client_id нужно зарегистрировать своё приложение по [ссылке](https://dev.vk.com/ru/api/getting-started)

Запустить Docker compose:
```
docker compose up -d
```
Документация при запущенном контейнере доступна по следующему адресу:
[http://localhost/docs](http://localhost/docs)
