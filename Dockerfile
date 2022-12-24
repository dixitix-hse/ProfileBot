FROM python:3.8-slim

EXPOSE 8888
COPY ./ /bot
WORKDIR /bot
RUN pip install -r ./requirements.txt
ENV PYTHONPATH .
CMD ["python3","./bot/bot.py", "5800804042:AAGc2pGppN-hpb3Sxng4tAwBUY1YTWoipT4"]
