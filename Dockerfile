FROM python:3.10-slim

WORKDIR /app

# 1) Install only the dependencies you actually use
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 2) Copy your application code
COPY core     ./core
COPY ranking  ./ranking
COPY cli      ./cli
COPY utils    ./utils

# 3) Set PYTHONPATH so imports resolve
ENV PYTHONPATH=/app

# 4) Entry point
CMD ["python", "-m", "cli.run", \
     "--input_dir", "/app/input", \
     "--output_dir", "/app/output", \
     "--persona", "${PERSONA}", \
     "--job", "${JOB}", \
     "--top_k", "5"]
