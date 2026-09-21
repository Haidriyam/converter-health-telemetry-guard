FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get upgrade -y && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY converter/ converter/

USER 10001
CMD ["python", "-c", "from converter.degradation_sentinel import ConverterHealthSentinel; print('Converter Sentinel Online.')"]