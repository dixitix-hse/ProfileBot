FROM python:3

RUN pip install asyncio
RUN pip install aiogram

COPY . .

ENTRYPOINT ["python3", "./main.py", "5800804042:AAGc2pGppN-hpb3Sxng4tAwBUY1YTWoipT4"]
