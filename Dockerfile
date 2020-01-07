FROM python:3.7.4-alpine

# set working directory
WORKDIR /usr/src/app

# set environment varibles
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# add and install requirements
COPY ./Pipfile .
COPY ./Pipfile.lock .
RUN pip install pipenv
RUN pip install --upgrade pip
RUN pipenv install --system

# add app
COPY . .

# run server
CMD python manage.py run -h 0.0.0.0
