FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

RUN addgroup --system ame && adduser --system --ingroup ame ame

COPY requirements.txt .
RUN pip install --no-cache-dir --requirement requirements.txt

COPY app ./app
COPY personality ./personality
COPY main.py README.md ./

USER ame

CMD ["python", "main.py"]
