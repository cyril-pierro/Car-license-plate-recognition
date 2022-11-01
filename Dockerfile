# Pull base image
FROM python:3.9

# Create work directory
WORKDIR /usr/src/tracker

RUN apt-get update; apt-get install ffmpeg libsm6 libxext6  -y

#Install poetry env, project dependency and model files
COPY poetry.lock pyproject.toml ./
RUN pip install --no-cache-dir poetry==1.2.0 && poetry config virtualenvs.create false && poetry install --no-interaction --no-ansi

# Copy application files
COPY ./ ./

# Expose port and run application
EXPOSE 8000

#ENTRYPOINT ["/bin/sh", "-c", "uvicorn"," main:app","--host 0.0.0.0"]
# CMD ["uvicorn", "main:app", "--host", "0.0.0.0"]
CMD ["python", "main.py"]

