__author__ = 'lmxiang'


class CloudxErr(Exception):
    '''
    Root exception.
    '''
    def __init__(self, message, **kwargs):
        self.kwargs = kwargs
        super(CloudxErr, self).__init__(message)

    def __getattr__(self, name):
        return self.kwargs.get(name)


class RunOsCommandsErr(CloudxErr):
    pass
