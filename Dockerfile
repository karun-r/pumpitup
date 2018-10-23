FROM python:3.6-slim

WORKDIR /app

COPY . /app

RUN pip install --trusted-host pypi.python.org -r requirements.txt

EXPOSE 80

EXPOSE 5000

ENV NAME World

CMD ["python","model.py"]


