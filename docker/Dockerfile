FROM python:3.14.3-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --upgrade pip \
    && pip install --no-cache-dir --upgrade "setuptools>=78.1.1" \
    && pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python3"]