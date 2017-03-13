import testinfra
import pytest
from tocker import Builder


# Use testinfra to get a handy function to run commands locally
local_command = testinfra.get_backend('local://').get_module('Command')


@pytest.fixture(scope="module")
def docker(request):
    # Build image and get the right tag
    try:
        tag = request.module.IMAGE_TAG
    except AttributeError:
        raise AssertionError(
            'Missing IMAGE_TAG in test module'
        )
    builder = Builder(tag=tag)
    builder.build()

    if builder.error:
        raise AssertionError(
            'Dockerfile failed to build: %s' % builder.error
        )

    try:
        run_args = request.module.RUN_ARGS
    except AttributeError:
        run_args = {}

    # Run a new container
    args = ' '.join(['%s %s' % (k, v) for k, v in run_args.items()])
    docker_command = "docker run -d %s %s" % (args, tag)
    docker_id = local_command.check_output(docker_command)
    print('Executing: "%s"' % docker_command)
    print('Running container: %s' % docker_id)

    def teardown():
        print('\nRemoving container: %s' % docker_id)
        local_command.check_output("docker kill %s", docker_id)
        local_command.check_output("docker rm %s", docker_id)

    # At the end of all tests, we destroy the container
    request.addfinalizer(teardown)

    return testinfra.get_backend("docker://%s" % (docker_id,))
