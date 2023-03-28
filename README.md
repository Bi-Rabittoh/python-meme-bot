# MemeBot
Telegram Bot that uses the Pillow library to compute light image processing.

## How to use

Copy the `.env.example` file into `.env` and insert your Telegram Bot Token.

Create a new virtual environment and install required packages:
```
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Then, start the bot by running:
```python main.py```

## Commands

* **/lang**: change the bot's display language;
* **/pic**: get a random anime picture;
* **/ttbt**: generate a meme in the top text, bottom text format;
* **/tt**: only use top text;
* **/bt**: only use bottom text;
* **/splash**: generate an authored quote;
* **/wot**: generate a wall of text;
* **/text**: display a short text over an image;
* **/spin**: spin a slot machine;
* **/bet**: change your bet;
* **/cash**: display current balance.
