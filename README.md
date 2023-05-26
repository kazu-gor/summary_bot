# summary_bot
Improve efficiency by using summary AI !!!!!


# Setup

Install the package.
```
$ pip install -r ./requirements.txt
```

Create `.env` file.
```
$ touch .env
```

Please access [here](https://platform.openai.com/account/api-keys) to obtain an API key and add it to your `.env` file.
```
$ echo OPENAI_API_KEY=XXXXXXX >> .env
```

Please access [here](https://api.slack.com/messaging/webhooks) to obtain an Slack API key and add it to your `.env` file.
```
$ echo WEB_HOOK_URL=XXXXXXX >> .env
```

# Usage

Execute the following to output a summary of the specified URL (default is TechCrunch) to Slack.
```
$ python3 main.py
```

If you wish to specify your own URL, change the `URL` in `main.py`.

```py:main.py
if __name__ == '__main__':

    URL = "https://techcrunch.com/"  # Change here
    url_list = get_urls(URL)
```

It is convenient to use cron.

## License

MIT
