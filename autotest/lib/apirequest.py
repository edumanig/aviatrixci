__author__ = 'lmxiang'

'''
Cloud API request mechanism.
'''
import logging

from tests.utils.tools import retry


class APIRequestError(Exception):
    '''
    API error.
    '''
    pass


class APIRequest(object):
    '''
    Cloud API request class.
    '''

    def __init__(
            self,
            retries=8,
            delay=1,
            max_delay=None,
            backoff=2,
            retry_callback=None,
            exceptions=None,
            return_vals=None):
        self.logger = logging.getLogger('cloudx')
        self.retries = retries
        self.delay = delay
        self.max_delay = max_delay
        self.backoff = backoff
        self.retry_callback = retry_callback
        self.exceptions = exceptions
        self.return_vals = return_vals

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, traceback):
        pass

    def execute(self, api, *args, **kwargs):
        '''
        Perform a cloud API call and return results.
        '''
        self.logger.info('Executing API request %s', api.__name__)
        result = retry.invoke(
            api,
            fargs=args,
            fkwargs=kwargs,
            retry_callback=self.retry_callback,
            exceptions=self.exceptions,
            return_vals=self.return_vals,
            tries=self.retries,
            delay=self.delay,
            max_delay=self.max_delay,
            backoff=self.backoff)
        return result
