FROM python:3.10-slim

RUN pip install --no-cache-dir \
    pandas==1.5.3 \
    numpy==1.24.3 \
    PyYAML==6.0

WORKDIR /app
COPY main.py scanner.py parser.py graphtaint.py constants.py repro_main.py /app/

ENTRYPOINT ["python", "/app/repro_main.py"]
