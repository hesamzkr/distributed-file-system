FROM python:3.12-alpine

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

#timezone
ENV TZ=Europe/Warsaw
RUN ln -snf /usr/share/zoneinfo/Europe/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN mkdir /app
WORKDIR /app

# Install dependencies
ADD ./requirements.txt /app/
RUN pip3 install -r requirements.txt

# Copy project
ADD ./ /app/
ENV PYTHONPATH /app
