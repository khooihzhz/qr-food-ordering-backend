FROM python:3.9
WORKDIR /qr-food-ordering-backend
COPY ./requirements.txt /qr-food-ordering-backend/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /qr-food-ordering-backend/requirements.txt
COPY ./app /qr-food-ordering-backend/app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
