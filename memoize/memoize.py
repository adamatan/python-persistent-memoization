'''
October 2020, Ittay Eyal, ittay@tx.technion.ac.il

References:
[1] The Python Wiki, http://wiki.python.org/moin/PythonDecoratorLibrary#Memoize
[2] Bruce Eckel, Python Decorators II: Decorator Arguments,
    http://www.artima.com/weblogs/viewpost.jsp?thread=240845
'''

import os
import json
import pickle
import pathlib
import hashlib
import functools
from sys import stderr

class Memoize(object):
    '''Decorator. Caches a function's return value each time it is called.
    If called later with the same arguments, the cached value is returned
    (not reevaluated).

    IMPORTANT: Decorate with parentheses, i.e. "@Memoized()" and not "@Memoized"
    '''

    DEBUG = False
    CACHE_DIR = '/tmp/python-memoization-cache'
    # If false, run anyway, and write result to cache
    READ_CACHE = True

    def __init__(self, cacheDir=None, debug=None):
        '''Called once.'''
        cacheDir = cacheDir or Memoize.CACHE_DIR
        pathlib.Path(cacheDir).mkdir(parents=True, exist_ok=True)
        self.debug = debug or Memoize.DEBUG

    def __call__(self, func):
        '''Initialization of the Memoized object. This is called once, with the
        name of the function to be wrapped.
        The actual wrapper is returned.
        '''
        self.func = func
        self.filename = os.path.basename(self.func.__code__.co_filename)

        def wrapped_func(*args, **kwargs):
            '''Memoization wrapper function. The wrapped function is already
            stored in self.func. This one gets the arguments as parameters.

            The hash key is computed with sha1 (due to the conflict probability,
            not cryptographic guarantees) of the function's filename and
            arguments.
            '''
            if not Memoize.CACHE_DIR:
                return self.func(*args, **kwargs)

            key = self.filename + '/' \
                + func.__name__ \
                + json.dumps([args, kwargs], sort_keys=True)
            hash_key = hashlib.sha1(key.encode('utf-8')).hexdigest()
            file_path = self.CACHE_DIR + '/' + hash_key + '.cache'
            ret = None
            if Memoize.READ_CACHE and os.path.exists(file_path):
                result_file = open(file_path, 'rb')
                try:
                    ret = pickle.load(result_file)
                # pylint: disable=W0703
                except Exception as e:
                    print(e)
                    ret = None
                result_file.close()
            if ret is not None:
                if self.debug: stderr.write('Warning! Result of ' +
                                            func.__name__ +
                                            '() in ' +
                                            self.filename +
                                            ' taken from cache.\n')
                return ret
            else:
                ret = self.func(*args, **kwargs)
                result_file = open(file_path, 'wb')
                pickle.dump(ret, result_file)
                result_file.close()
                return ret

        return wrapped_func

    def __repr__(self):
        '''Return the function's docstring.'''
        return self.func.__doc__

    def __get__(self, obj, objtype):
        '''Support instance methods.'''
        return functools.partial(self.__call__, obj)
