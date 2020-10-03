# October 2020, Ittay Eyal, ittay@tx.technion.ac.il 
# 
# References: 
# [1] The Python Wiki, http://wiki.python.org/moin/PythonDecoratorLibrary#Memoize 
# [2] Bruce Eckel, Python Decorators II: Decorator Arguments, 
#     http://www.artima.com/weblogs/viewpost.jsp?thread=240845 

import collections
import functools
import hashlib 
import os 
import json
import pickle 
from sys import stderr 
import queue
import threading 

class Memoize(object):
    '''Decorator. Caches a function's return value each time it is called.
    If called later with the same arguments, the cached value is returned
    (not reevaluated). 

    IMPORTANT: Decorate with parentheses, i.e. "@Memoized()" and not "@Memoized" 
    ''' 
    
    debug = False 
    cacheDir = "/tmp" 
    readCache = True # If false, run anyway, and write result to cache. 
    
    def __init__(self, cacheDir = None, debug = None): 
        """Initialization of the Memozied object. This is called once, when the 
        object is initialized. 
        """
        if cacheDir != None: 
            Memoize.cacheDir = cacheDir 
        if debug != None: 
            self.debug = debug 
    
    def __call__(self, func): 
        """Initialization of the Memoized object. This is called once, with the 
        name of the function to be wrapped. 
        The actual wrapper is returned. 
        Note: Calls to the function must be with named arguments, not positional. 
        """
        self.func = func
        self.filename = os.path.basename( self.func.__code__.co_filename ) 
        
        def wrappedFunc(*args, **kwargs): 
            """Memoization wrapper function. The wrapped function is already 
            stored in self.func. This one gets the arguments as parameters. 
            
            The hash key is computed with sha1 (due to the conflict probability, 
            not cryptographic guarantees) of the function's filename and 
            arguments. 
            """
            if Memoize.cacheDir == None: 
                return self.func(*args, **kwargs) 
            
            nameWithArgs = self.filename + '/' + func.__name__ + json.dumps([args, kwargs], sort_keys=True)
            print(f'nameWithArgs: {nameWithArgs}')
            print(f'func name: {func.__name__}')
            hashKey = hashlib.sha1(nameWithArgs.encode("utf-8")).hexdigest() 
            print(f'Hashkey: {hashKey}')
            filePath = self.cacheDir + "/" + hashKey + ".cache"
            ret = None
            if Memoize.readCache and os.path.exists(filePath): 
                resultFile = open(filePath, "rb") 
                try: 
                    ret = pickle.load(resultFile) 
                except Exception as e: 
                    print(e) 
                    ret = None 
                resultFile.close() 
            if ret != None: 
                if self.debug: stderr.write("Warning! Result of " + 
                                            func.__name__ + 
                                            "() in " + 
                                            self.filename + 
                                            " taken from cache.\n") 
                return ret 
            else: 
                ret = self.func(*args, **kwargs) 
                resultFile = open(filePath, "wb") 
                pickle.dump(ret, resultFile) 
                resultFile.close() 
                return ret 
        
        return wrappedFunc 

    def __repr__(self):
        '''Return the function's docstring.'''
        return self.func.__doc__
    
    def __get__(self, obj, objtype):
        '''Support instance methods.'''
        return functools.partial(self.__call__, obj) 
