FROM python:3.9
WORKDIR /cat304-api
COPY ./requirements.txt /cat304-api/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /cat304-api/requirements.txt
COPY ./app /cat304-api/app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]