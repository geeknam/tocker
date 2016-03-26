

IMAGE_TAG = 'nginx:1.9.12'


def test_apt_sources(docker):
    file = docker.get_module('File')
    assert file('/etc/apt/sources.list').contains(
        'http://nginx.org/packages/mainline/debian/'
    )


def test_nginx_installed(docker):
    package = docker.get_module('Package')
    assert package('nginx').is_installed


def test_nginx_user(docker):
    user = docker.get_module('User')
    assert user('www-data').exists
    assert user('www-data').uid == 33
    assert user('www-data').home == '/var/www'

