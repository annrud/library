FROM python:3.10-alpine
WORKDIR /code
COPY ../requirements.txt ./
RUN python3.10 -m pip install --upgrade pip
RUN pip3 install -r ./requirements.txt
COPY ../library ./
RUN python3.10 manage.py collectstatic
CMD ["gunicorn", "library.wsgi:application", "--bind", "0.0.0.0:8000"]
