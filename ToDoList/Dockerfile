FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

# 🔁 انسخ requirements.txt قبل أي حاجة
COPY requirements.txt .

# ✅ ثبّت متطلبات النظام والبكجات
RUN apt-get update && \
    apt-get install -y build-essential libssl-dev libffi-dev default-libmysqlclient-dev gcc && \
    pip install --upgrade pip && \
    pip install -r requirements.txt

# 🧠 بعدين انسخ باقي المشروع
COPY . .

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
