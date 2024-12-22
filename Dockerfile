FROM python:3.12-alpine

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY fonts ./fonts
COPY python_meme_bot ./python_meme_bot

CMD ["python", "-m", "python_meme_bot"]
