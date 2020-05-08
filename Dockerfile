FROM python:3.7.6

COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip install -r requirements.txt

COPY ./app/app.py /app/app.py

EXPOSE 5000

ENTRYPOINT ["python"]
CMD ["app.py"]
