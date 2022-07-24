# Setup

`git clone https://github.com/Madara225/telegram-raid-botnet-pyrogram`

`cd telegram-raid-botnet-pyrogram`

`pip3 install -r requirements.txt`

`python3 main.py`

Authorize: https://my.telegram.org/

After authorizing and creating the application, take your api_id and api_hash

# Adding accounts
`cd sessions`

`python3 add_acc.py`

To start, start the first function, enter the account phone number or bot token.

After you have added all the accounts, start the second function, it will bind the accounts to the botnet.

The third function checks accounts for validity; if an account is invalid, the session is moved to the sessions/dead folder, thereby no longer being used by the botnet, after which you **must** run the second function again.
 

 
# Config
`cd settings`

`nano config.py` (All variables are commented in the config)

# Start

`python3 main.py`
 
Video tutorial on how to start a botnet: [YouTube](https://www.youtube.com/watch?v=DKKpfHzMR78)

If you have any questions, you can contact our [chat](https://t.me/pepe_devs)

I got the idea and part of the code from [huis_bn](https://t.me/huis_bn)

Botnet [huis_bn](https://t.me/huis_bn) > [json1c/telegram-raid-botnet](https://github.com/json1c/telegram-raid-botnet)
