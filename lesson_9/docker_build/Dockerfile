FROM postgres:11

# Install curl and CA and cleanup
RUN apt-get update -yqq \
    && apt-get install -yqq --no-install-recommends curl ca-certificates \
    && update-ca-certificates \
    && apt-get clean \
    && rm -rf \
        /var/lib/apt/lists/*

# Download citus tutorial data
RUN curl https://examples.citusdata.com/tutorial/events.csv > /events.csv && \
    curl https://examples.citusdata.com/tutorial/users.csv > /users.csv

# Add setup script to Database initialise
COPY *.sql /docker-entrypoint-initdb.d/
ADD simple-citus-data-init.sql /docker-entrypoint-initdb.d
RUN chmod a+r /docker-entrypoint-initdb.d/*

EXPOSE 5432
