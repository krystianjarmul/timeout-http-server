
## Installation 
There are only two prerequisites:
* Docker
* Docker-compose

## Having both, you'll need to clone the repository:
```
git clone https://github.com/krystianjarmul/timeout-http-server.git
```
and go into:
```
cd timeout-http-server
```

## Usage
You'll need to build and run the docker containers:
```
docker-compose up --build
```
Now you have access to the container via:
http://localhost:8000/

API docs: http://localhost:8000/docs

## Testing
Run tests:
```
docker-compose run --rm --no-deps --entrypoint=pytest api /tests/
```
