# Starts the docker container
up run start:
	docker compose up -d

# Forcibly rebuilds the entire docker application without caching
build:
	docker compose up --build --no-cache -d

# Rebuilds and runs application without detaching
test:
	docker compose up --build --no-cache

.PHONY up run start build test
