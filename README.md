# QR Food-Ordering System

This is the backend for the QR Food Ordering System

## Descriptions

This project is built with FastAPI and MongoDB

## Installations

Clone the repository

```
git clone https://github.com/khooihzhz/cat304-api.git
```

Run Directly on your own machine

```
# install packages with pip
pip install -r requirements .txt

# run application with uvicorn
uvicorn app.main:app --reload
```

**OR**

Run the application with Docker

```
# build Docker Image
docker build -t myimage .

# run Docker container
docker run -d --name mycontainer --env-file .env -p 80:80 myimage

Note: You need to include your own env files containing :
- DB_URL
- DB_NAME
- SECRET_KEY

```

## Usage

Go to

> localhost:<your_port_choice>/docs

to try out the API and read the Docs

## Acknowledgments

- [FastAPI](https://fastapi.tiangolo.com/)
- [MongoDB](https://www.mongodb.com/)
- [motor](https://docs.mongodb.com/drivers/motor/)
