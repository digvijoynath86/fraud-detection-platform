FROM python:3.10-slim

WORKDIR /app

COPY . /app

RUN pip install --upgrade pip

RUN pip install --no-cache-dir -r requirements-api.txt

ENV PYTHONPATH=/app

EXPOSE 8000

CMD ["uvicorn", "src.api.inference_api:app", "--host", "0.0.0.0", "--port", "8000"]