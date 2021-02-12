FROM python:3.8-slim

WORKDIR "/srv/producer"

# Copy default entrypoint script
COPY ./info.py /srv/producer/info.py

ENTRYPOINT ["python", "info.py"]

