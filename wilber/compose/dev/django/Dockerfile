FROM python:3.7-slim-buster

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

RUN apt-get update \
  # dependencies for building Python packages
  && apt-get install -y build-essential \
  # psycopg2 dependencies
  && apt-get install -y libpq-dev \
  # Translations dependencies
  && apt-get install -y gettext \
  # pip cache dependencies
  && apt-get install -y rsync iproute2 \
  && apt-get install -y git \
  # cleaning up unused files
  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && rm -rf /var/lib/apt/lists/*


# Requirements are installed here to ensure they will be cached.
# COPY ./requirements /requirements
# RUN pip install -r /requirements/dev.txt




# Rsync local pip folder
COPY ./requirements /requirements
COPY pip-cached-install.sh ./
ARG RSYNC_PASSWORD=""
ENV RSYNC_PASSWORD=$RSYNC_PASSWORD
RUN bash ./pip-cached-install.sh /requirements/dev.txt




COPY ./compose/prod/django/entrypoint /entrypoint
RUN sed -i 's/\r$//g' /entrypoint
RUN chmod +x /entrypoint

COPY ./compose/dev/django/start /start
RUN sed -i 's/\r$//g' /start
RUN chmod +x /start

WORKDIR /app

ENTRYPOINT ["/entrypoint"]
