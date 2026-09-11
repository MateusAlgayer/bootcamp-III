FROM python:3.12-alpine

WORKDIR /app

COPY pyproject.toml README.md ./
COPY src ./src

RUN pip install --no-cache-dir .

EXPOSE 80

CMD ["streamlit", "run", "src/views/home.py", "--server.address", "0.0.0.0", "--server.port", "80"]
