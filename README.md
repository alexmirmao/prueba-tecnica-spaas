# Having into count
There are two codes for the algorithm
- Firstly I coded it linearly (function: load_algorithm)
- Secondly I coded it recursively to get it more optimized (function: load_algorithm_recursively)

The linear algorithm is commented but it can still be run

# How to run the application

# 1. Using DOCKER
## 1.Step
build the Docker image by running the following command in the directory where your Dockerfile is located:
```bash
docker build -t my-app:v1 .
```

## 2.Step
Once your image is built, you can run the container with this command:
```bash
docker run -d -p 8888:8888 --name my-container my-app:v1
```

- -d flag runs the container in background
- -p 8888:8888 This command maps the container ports to our local ports. We are mapping port 8888 to 8888 which is exposed in the flask app in the app.py
- --name gives the container a name

## 3.Step
Using POSTMAN check if it works using a post method through http://127.0.0.1:8888/productionplan


# 2. In LOCAL
## Installation & Usage
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run the API:
   ```bash
   python app.py
   ```