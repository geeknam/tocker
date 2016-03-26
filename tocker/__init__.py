import docker as dockerpy


class Stream(object):

    def __init__(self, stream):
        self.stream = stream

    @property
    def error(self):
        for line in self.stream:
            if 'errorDetail' in line:
                return line['errorDetail']['message']
        return


class Builder(object):

    def __init__(self, tag, ssl_version=None, assert_hostname=False):
        kwargs = dockerpy.utils.kwargs_from_env(
            ssl_version, assert_hostname
        )
        self._client = dockerpy.Client(
            version='auto', **kwargs
        )
        self.tag = tag
        self.result = []

    def build(self):
        print('\nBuilding image: %s' % self.tag)
        for line in self._client.build(
            path='.', rm=True, forcerm=True,
            decode=True, tag=self.tag
        ):
            try:
                print line['stream']
            except KeyError:
                print line
            self.result.append(line)
        return self.tag

    @property
    def error(self):
        return Stream(self.result).error
