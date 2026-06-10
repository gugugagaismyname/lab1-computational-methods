# Модель: Математичне моделювання розподілу забруднюючих речовин між повітрям, водою та ґрунтом (5 семестр)
# Автор: Апанович Герман, група АІ231

FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY main.py .

CMD ["python", "main.py"]