# my-telegram-assistant
:robot: Автоматизация переписки в Telegram.

Читать на других языках:
* [Russian](README.ru.md)
* [English](README.md)

## Возможности

### Команды
Команды позволяют обрабатывать запросы пользователя из бесед (аналог [команд у Telegram ботов](https://core.telegram.org/bots)).
Команды бывают двух видов:
* Явные - в сообщении они указываются явно.
* Неявные - вызываюттся без указания.

#### Поддерживаемые команды:

#### Неявные
##### скачивание поста/видео из социальной сети
Поддерживаемые соцсети:
* [x] YouTube
* [ ] TikTok
* [ ] Instagram
* [ ] Twitter

#### Явные
##### `\me [type] [scope]` - выводит контактную информацию о пользователе
##### `\d` - скачивает пост по ссылке из replied сообщения
##### `\all` - упоминание всех участников в чате (works only in basic group chat)
##### `\hello` - самореклама :smirk:

## Установка и запуск
### 1. Установка необходимых переменных окружения
```shell
# Telegram bot (assistant manager)
TELEGRAM_API_TOKEN=
MY_TELEGRAM_ID=

# Assistant client
AIOTDLIB_API_ID=
AIOTDLIB_API_HASH=
PHONE_NUMBER=

# Worker
CELERY_RESULT_BACKEND=
CELERY_BROKER_URL=

# Assistant service
ASSISTANT_GRPC_PORT=
ASSISTANT_GRPC_HOST=
ASSISTANT_GRPC_ADDR=

# Database
DB_NAME=
DB_USER=
DB_PASSWORD=

# RabbitMQ
RABBITMQ_DEFAULT_USER=
RABBITMQ_DEFAULT_PASS=
```

### 2. docker compose up!
