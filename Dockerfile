# Build Stage
FROM python:3.12.0-alpine as build
RUN apk update

# Install build dependencies
RUN apk add --update --no-cache --virtual .tmp-build-deps \
    --repository=http://dl-cdn.alpinelinux.org/alpine/edge/community \
    librdkafka librdkafka-dev gcc libc-dev linux-headers

RUN apk add --no-cache g++ libffi-dev

# Upgrade pip
RUN pip install --upgrade pip

# Set working directory
WORKDIR /app

# Copy application code to the docker image
COPY . /app
#COPY .env.production /app/.env
# uncomment if you're not using manifest environments

# Install the Python dependencies
COPY requirements.txt /app/requirements.txt
RUN pip install .

# Remove temporary build dependencies
RUN apk del .tmp-build-deps


# Interim Stage for Installing System Updates and ffmpeg
FROM python:3.12-alpine AS production_base

# Install system updates and ffmpeg
RUN apk update && \
    apk add --no-cache ffmpeg librdkafka

# Create a non-root user to run the application
RUN adduser -D deploy
USER deploy    
    
# Production Stage using production_base Image as Base
FROM production_base as production

# Copy the Python environment and application from the build stage
COPY --from=build /usr/local /usr/local
COPY --from=build --chown=deploy /app /app

# Set the working directory
WORKDIR /app

# Expose the necessary port
EXPOSE 5001

# Set the entry point to run the Python application directly
CMD ["python", "run.py"]
