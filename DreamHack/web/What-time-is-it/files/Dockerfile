FROM python:3.11-slim
WORKDIR /app

RUN pip install --no-cache-dir Flask==3.0.3

COPY app.py session.py ./
COPY templates ./templates
COPY flag.txt /flag.txt

EXPOSE 5000
CMD ["python", "app.py"]
