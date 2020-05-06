FROM python:3.8.0-slim

# http://bugs.python.org/issue19846
ENV LANG C.UTF-8
ENV PYTHONUNBUFFERED 1
ENV USR_HOME=/home/ghost
ENV APP_HOME=/home/ghost/web
ENV LOG_PATH=/var/log/django/ghost

WORKDIR ${APP_HOME}

RUN pip install --upgrade pip

RUN mkdir -p ${USR_HOME} && \
	adduser --system --home=${USR_HOME} --no-create-home --disabled-password --group ghost && \
	mkdir -p ${LOG_PATH} && \
	mkdir -p ${APP_HOME}

COPY requirements.txt ${APP_HOME}/requirements.txt
RUN pip install -r requirements.txt

COPY . ${APP_HOME}
RUN chown -R ghost:ghost ${APP_HOME} && \
	chown -R ghost:ghost ${LOG_PATH}

RUN mkdir -p /var/ghost/static && chown -R ghost:ghost /var/ghost

USER ghost

ENTRYPOINT [ "/home/ghost/web/entrypoint.sh" ]