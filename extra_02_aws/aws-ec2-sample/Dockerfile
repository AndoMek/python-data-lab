FROM python:3.8-slim

# Copy requirements.txt to Docker image
COPY requirements.txt /requirements.txt

# Install dependencies
RUN pip install --upgrade pip wheel setuptools \
    && pip install -r /requirements.txt \
    && rm -fr \
        /root/.cache/pip/*

# Copy default entrypoint script
COPY app/* /srv/api/

WORKDIR "/srv/api"
EXPOSE 5000
ENTRYPOINT ["python", "app.py"]
