## Gobbie Webhook
This is a python script written to generate a webhook from [Raelys' Lodestone API](https://documenter.getpostman.com/view/1779678/TzXzDHVk), which is an API for getting news/updates for the game, _Final Fantasy XIV: A Realm Reborn_.

It was written in python for simplicity and easy of adjustment.

### Setup

Create a `.env` file in the root of the project and add the following:
``` env
# This can be any webhook URL (though it is designed for Guilded.gg)
WEBHOOK_URL="https://<your-webhook-url>"
# Change region to match yours. Acceptable parameters: na, eu, fr, de, jp
LODESTONE_API_BASE_URL="http://eu.lodestonenews.com/news/"
```

### Usage

``` bash
git clone https://github.com/ashcorpdev/gobbie-webhook
cd gobbie-webhook
python3 webhook.py
```

The bot pulls data every 20 minutes. Some announcements may be missed if posted more frequently than this; however, all topics should post regardless, which should catch any missed ones.
