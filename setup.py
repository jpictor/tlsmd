import os
from numpy.distutils.core import setup, Extension

tlsmdmodule = Extension(
    name = 'tlsmdmodule',
    define_macros = [('MAJOR_VERSION', '1'), ('MINOR_VERSION', '0')],
    include_dirs = ['/usr/local/include'],
    libraries = ['lapack', 'blas'],
    library_dirs = ['/usr/local/lib'],
    sources = map(lambda x: os.path.join('c-modules', 'tlsmdmodule', x), [
        'structure.cpp',
        'dgesdd.cpp',
        'tls_model.cpp',
        'tls_model_nl.cpp',
        'tls_model_engine.cpp',
        'tlsmdmodule.cpp'])
)

tlsvld = Extension(
    name = 'tlsvld',
    sources = ['c-modules/tlsvld/tlsvld.f']
)

LONG_DESCRIPTION = """\
"""

setup(
    name = 'TLSMD',
    version = '1.0',
    description = 'TLS motion analysis for crystallographically determined protein structures.',
    author = 'Jay Painter',
    author_email = 'jay.painter@gmail.com',
    url = 'https://github.com/jpictor/',
    long_description = LONG_DESCRIPTION,
    ext_modules = [tlsmdmodule, tlsvld]
)
