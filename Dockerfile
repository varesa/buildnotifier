FROM registry.esav.fi/base/python3

COPY . /app
WORKDIR /app

CMD ["python3", "-u", "main.py"]
