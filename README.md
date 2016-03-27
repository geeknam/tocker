tocker: TDD for writing Dockerfile
-----------------------------------

## About

`tocker` is a plugin for [testinfra](https://github.com/philpep/testinfra/) that allows developers to test `docker` images


## Getting Started

    pip install tocker

Set your environment variables to connect to docker engine:

    export DOCKER_HOST=unix:///var/run/docker.sock

If docker engine runs a different host, set the following:

    export DOCKER_TLS_VERIFY=1
    export DOCKER_HOST=tcp://ip:port
    export DOCKER_CERT_PATH=/path/to/certs

If you're using `docker-machine`, you can simply run:

    eval $(docker-machine env myenv)


## Workflow

1. Create a `Dockerfile`
2. Create a `test.py` in the same directory
3. Add `IMAGE_TAG` to test.py. E.g: `mycorp/nginx:1.9.12`
4. Write your tests (find out more about how to use different modules from [testinfra docs](http://testinfra.readthedocs.org/en/latest/modules.html))
5. Run `testinfra test.py` (`-s -v` for verbose mode)
6. Watch your tests fail
7. Edit your `Dockerfile` until the tests pass
8. When you're happy `docker push` the image

## How does it work?

- `tocker` builds an image from `Dockerfile`
- The image will be tagged with `IMAGE_TAG`
- When the image is successfully built, a new container is created
- Tests are run against the created container with `docker exec`
- The container is destroyed at the end of all test cases
- `tocker` uses docker build cache so the consecutive runs are fast
- The resulting image is not removed

## Contribute
If you're looking to add a new module, please contribute to [testinfra](https://github.com/philpep/testinfra/).

If it's more specific to `Docker`, you can add additional fixtures under `tocker/fixtures.py`. Pull requests are welcome.

