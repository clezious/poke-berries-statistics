FROM python:3.8

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir  --upgrade -r /app/requirements.txt

COPY ./app /app

CMD ["hypercorn", "main:app", "--bind", "0.0.0.0:80"]

EXPOSE 80
