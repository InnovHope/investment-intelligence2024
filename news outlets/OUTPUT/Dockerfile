FROM python:latest

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1


# Install pip requirements
COPY requirements.txt .
RUN python -m pip install -r requirements.txt
RUN python -m spacy download en_core_web_sm


WORKDIR /app
COPY . /app


# During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
CMD ["python", "news_main.py"]


##execute docker run -d --network="host" newsoutlets