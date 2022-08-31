# RU

## Устанока

`git clone https://github.com/Madara225/telegram-raid-botnet-pyrogram`

`cd telegram-raid-botnet-pyrogram`

`pip3 install -r requirements.txt`

`python3 main.py`

Авторизуемся на [My Telegram](https://my.telegram.org)

Далее берём оттуда API ID и API HASH

## Добавление аккаунтов
`cd sessions`

`python3 add_session.py`

Для начала запускаем первую функцию, вводим номер телефона аккаунта или токен бота.

После того как добавили все аккаунты, запускаем вторую функцию, она привяжет аккаунты к ботнету.

Третья функция проверяет аккаунты на валидность, в случае, если аккаунт не валидный, сессия переносится в папку sessions/dead, тем самым, больше не задействуется в ботнете, после этого нужно **обязательно** запустить ещё раз вторую функцию.
 
## Конфиг
`cd settings`

`nano config.py` (в конфиге прокомментированы все переменные)

## Запуск

`python3 main.py`
 
Видео-инструкция по запуску ботнета: [YouTube](https://www.youtube.com/watch?v=DKKpfHzMR78)

Если есть вопросы, Вы можете обратится в наш [чат](https://t.me/pepe_devs)

Идею и часть кода взял у [huis_bn](https://t.me/huis_bn)

Ботнет [huis_bn](https://t.me/huis_bn) > [json1c/telegram-raid-botnet](https://github.com/json1c/telegram-raid-botnet)

# EN

## Setup

`git clone https://github.com/Madara225/telegram-raid-botnet-pyrogram`

`cd telegram-raid-botnet-pyrogram`

`pip3 install -r requirements.txt`

`python3 main.py`

Authorize: https://my.telegram.org/

After authorizing and creating the application, take your api_id and api_hash

## Adding accounts
`cd sessions`

`python3 add_session.py`

To start, start the first function, enter the account phone number or bot token.

After you have added all the accounts, start the second function, it will bind the accounts to the botnet.

The third function checks accounts for validity; if an account is invalid, the session is moved to the sessions/dead folder, thereby no longer being used by the botnet, after which you **must** run the second function again.
 

 
## Config
`cd settings`

`nano config.py` (All variables are commented in the config)

## Start

`python3 main.py`
 
Video tutorial on how to start a botnet: [YouTube](https://www.youtube.com/watch?v=DKKpfHzMR78)

If you have any questions, you can contact our [chat](https://t.me/pepe_devs)

I got the idea and part of the code from [huis_bn](https://t.me/huis_bn)

Botnet [huis_bn](https://t.me/huis_bn) > [json1c/telegram-raid-botnet](https://github.com/json1c/telegram-raid-botnet)
