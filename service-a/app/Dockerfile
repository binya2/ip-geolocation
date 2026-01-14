FROM python:3.11-slim

WORKDIR /ip-geolocation

COPY service-a/app/requirements.txt ./service-a/app/
RUN pip install --no-cache-dir -r service-a/app/requirements.txt

COPY service-a/ ./service-a/
COPY shared/ ./shared/
ENV PYTHONPATH=/ip-geolocation

EXPOSE 8000

CMD ["python", "service-a/app/main.py"]