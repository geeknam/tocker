from unittest import TestCase
from tocker import Stream, Builder
import os
from mock import patch


class TockerTestCase(TestCase):

    def test_error(self):
        error_message = 'Docker engine error'
        result = [{
            'errorDetail': {
                'message': error_message
            }
        }]
        stream = Stream(result)
        self.assertEqual(stream.error, error_message)

    @patch('docker.client.Client._retrieve_server_version')
    def test_init_uni_socket(self, mock_version):
        os.environ['DOCKER_HOST'] = 'unix:///var/run/docker.sock'
        mock_version.return_value = '1.10'

        builder = Builder(tag='myimage')
        self.assertEqual(
            builder._client.base_url, 'http+docker://localunixsocket'
        )
        self.assertEqual(
            builder._client._version, '1.10'
        )

    @patch('docker.client.Client._retrieve_server_version')
    def test_init_http(self, mock_version):
        os.environ['DOCKER_HOST'] = 'tcp://192.168.99.100:2376'
        mock_version.return_value = '1.10'

        builder = Builder(tag='myimage')
        self.assertEqual(
            builder._client.base_url, 'http://192.168.99.100:2376'
        )
        self.assertEqual(builder._client._version, '1.10')

    @patch('docker.client.Client.build')
    @patch('docker.client.Client._retrieve_server_version')
    def test_build(self, mock_version, mock_build):
        os.environ['DOCKER_HOST'] = 'tcp://192.168.99.100:2376'
        mock_version.return_value = '1.10'

        builder = Builder(tag='myimage')
        builder.build()
        mock_build.assert_called_with(
            path='.', rm=True, forcerm=True,
            tag='myimage'
        )
