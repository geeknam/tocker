import requests

IMAGE_TAG = 'mynginx:latest'
RUN_ARGS = {
    '-p': '8080:80'
}


def test_nginx_content(docker):
    response = requests.get(url='http://localhost:8080')
    assert 'Test Demo' in response.content
