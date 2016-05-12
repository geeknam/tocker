IMAGE_TAG = 'mynginx:latest'


def test_apt_sources(docker):
    file = docker.get_module('File')
    assert file('/etc/apt/sources.list').contains(
        'http://nginx.org/packages/mainline/debian/'
    )


def test_nginx_installed(docker):
    package = docker.get_module('Package')
    assert package('nginx').is_installed


def test_nginx_directories(docker):
    file = docker.get_module('File')
    assert file('/etc/nginx/conf.d').exists
    assert file('/etc/nginx/conf.d').is_directory


def test_nginx_user(docker):
    user = docker.get_module('User')
    assert user('www-data').exists
    assert user('www-data').uid == 33
    assert user('www-data').home == '/var/www'


def test_nginx_service(docker):
    process = docker.get_module('Process')
    nginx_processes = process.filter(
        user='nginx', comm="nginx"
    )
    assert len(nginx_processes) == 1
