# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.9 as builder

WORKDIR /usr/src/app

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1
# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1


# install psycopg2 dependencies
RUN apt-get update
RUN apt-get upgrade -y  && apt-get -y install postgresql gcc python3-dev musl-dev

# Install pip requirements
RUN python -m pip install --upgrade pip

COPY ./req.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /usr/src/app/wheels -r req.txt

COPY . .

FROM python:3.9

RUN mkdir -p /home/app

RUN groupadd app
RUN useradd -m -g app app -p dfqw12fewefwq
RUN usermod -aG app app

ENV HOME=/home/app
ENV APP_HOME=/home/app/qr_tatu

RUN mkdir $APP_HOME
RUN mkdir $APP_HOME/static
RUN mkdir -m=777 $APP_HOME/media
WORKDIR $APP_HOME

RUN apt-get update\
    && apt-get install -y netcat

COPY --from=builder /usr/src/app/wheels /wheels
COPY --from=builder /usr/src/app/req.txt .
RUN pip install --no-cache /wheels/*

COPY . $APP_HOME

RUN chown -R app $APP_HOME

USER app
