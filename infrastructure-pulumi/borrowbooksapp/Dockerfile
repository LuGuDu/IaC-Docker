FROM python:3.9

COPY .. /app

WORKDIR /app/borrowbooksapp

RUN pip install --upgrade pip

RUN pip install flask && pip install flask_pymongo

CMD ["python", "app.py"]

EXPOSE 5000