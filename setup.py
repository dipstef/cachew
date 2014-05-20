from distutils.core import setup

VERSION = '0.1'

desc = """Sqlite response cache for httpy. Used together with an httpy_client will retrieve cached responses or
 store responses from the client."""

name = 'httpy_cache'

setup(name=name,
      version=VERSION,
      author='Stefano Dipierro',
      author_email='dipstef@github.com',
      url='http://github.com/dipstef/{}/'.format(name),
      description=desc,
      packages = ['httpy.cache'],
      platforms=['Any'],
      requires=['urlo', 'httpy', 'quelo']
)