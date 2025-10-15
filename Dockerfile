FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 PIP_NO_CACHE_DIR=1

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
   libpq5 curl && rm -rf /var/lib/apt/lists/* \
   libpq5 curl ca-certificates \
&& update-ca-certificates \
&& rm -rf /var/lib/apt/lists/*

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

#EXPOSE 8002
#CMD ["flask", "--app", "wsgi", "--debug", "run", "-h", "0.0.0.0", "-p", "8002", "--reload"]

ENV PORT=8080
CMD ["gunicorn", "wsgi:app", "--bind", "0.0.0.0:8080", "--workers", "2", "--threads", "4", "--timeout", "0"]