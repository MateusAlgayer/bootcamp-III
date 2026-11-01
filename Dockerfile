FROM python:3.12-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DATABASE_PATH=/app/data/finance.db

COPY pyproject.toml README.md ./
COPY src ./src

# Instalação editável: o runtime importa sempre /app/src, sem cópias divergentes
# em site-packages.
RUN pip install --no-cache-dir -e . \
    && mkdir -p /app/data

EXPOSE 8501

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8501/_stcore/health')" || exit 1

CMD ["streamlit", "run", "src/views/home.py", "--server.address", "0.0.0.0", "--server.port", "8501", "--server.headless", "true"]
