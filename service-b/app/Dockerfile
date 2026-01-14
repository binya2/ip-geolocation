FROM python:3.11-slim

WORKDIR /ip-geolocation

COPY service-b/app/requirements.txt ./service-b/app/
RUN pip install --no-cache-dir -r service-b/app/requirements.txt

COPY service-b/ ./service-b/
COPY shared/ ./shared/
ENV PYTHONPATH=/ip-geolocation

RUN useradd -m -u 1000 appuser && chown -R appuser:appuser .
USER appuser

EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health') or exit(1)"
CMD ["python", "service-b/app/main.py"]