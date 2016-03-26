import testinfra
import pytest
from tocker import Builder


@pytest.fixture(scope="module")
def docker(request, LocalCommand):
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

    # Run a new container
    docker_id = LocalCommand.check_output(
        "docker run -d %s tail -f /dev/null" % tag
    )
    print('Running container: %s' % docker_id)

    def teardown():
        print('\nRemoving container: %s' % docker_id)
        LocalCommand.check_output("docker kill %s", docker_id)
        LocalCommand.check_output("docker rm %s", docker_id)

    # At the end of all tests, we destroy the container
    request.addfinalizer(teardown)

    return testinfra.get_backend("docker://%s" % (docker_id,))
