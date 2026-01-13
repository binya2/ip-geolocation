FROM python:3.11-slim
WORKDIR /app
COPY . .
RUN pip install --no-cache-dir requirements.txt
RUN useradd -m -u 1000 appuser && \
    chown -R appuser:appuser /app
USER appuser
EXPOSE 8000
# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')"
CMD ["python", "main.py"]
