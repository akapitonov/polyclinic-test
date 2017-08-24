FROM python:3

RUN apt-get update && apt-get install -y \
		gcc \
		gettext \
		mysql-client libmysqlclient-dev \
		postgresql-client libpq-dev \
		sqlite3 \
	--no-install-recommends && rm -rf /var/lib/apt/lists/*

RUN mkdir -p /app
WORKDIR /app

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt gunicorn psycopg2

COPY . /app

EXPOSE 80

ENV DJANGO_SETTINGS_MODULE=polyclinic.settings.docker

CMD ["gunicorn", "polyclinic.wsgi", "-b", ":80", "--log-file", "-"]