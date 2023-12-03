FROM python:3.10
COPY . /stock_project
WORKDIR /stock_project
RUN ["pip3", "install", "-r", "requirements.txt"]
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
