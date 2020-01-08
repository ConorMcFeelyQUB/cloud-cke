FROM python:3.7-slim

# Copy local code to the container image.
ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . ./

# Install production dependencies.
RUN pip install Flask gunicorn mysql-connector-python requests beautifulsoup4

CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 app:app