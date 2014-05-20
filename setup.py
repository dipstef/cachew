from distutils.command.build_py import build_py
from distutils.core import setup
import os
import shutil

VERSION = '0.1'

desc = """Sqlite response cache for httpy. Used together with an httpy_client will retrieve cached responses or
 store responses from the client."""

name = 'httpy_cache'


class CacheInitFileCopy(build_py):

    def run(self):
        build_py.run(self)

        build_file_path = os.path.join(self.build_lib, 'httpy', 'cache', 'cache.sql')

        if os.path.exists(build_file_path):
            os.remove(build_file_path)

        cache_init_path = os.path.join(os.path.dirname(__file__), 'httpy', 'cache', 'cache.sql')
        shutil.copy(cache_init_path, build_file_path)

setup(name=name,
      version=VERSION,
      author='Stefano Dipierro',
      author_email='dipstef@github.com',
      url='http://github.com/dipstef/{}/'.format(name),
      description=desc,
      packages = ['httpy.cache'],
      platforms=['Any'],
      cmdclass={'build_py': CacheInitFileCopy},
      requires=['urlo', 'httpy', 'quelo']
)