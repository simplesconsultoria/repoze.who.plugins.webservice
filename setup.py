from setuptools import setup, find_packages
import os

version = '0.6.dev0'

requires = [
      'setuptools',
      # -*- Extra requirements: -*-
      'repoze.who',
]

tests_requires = requires

setup(name='repoze.who.plugins.webservice',
      version=version,
      description="""An IAuthenticatorPlugin plugin for repoze.who
                     which connects to backends and using json validates
                     credentials
                  """,
      long_description=open("README.rst").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from
      # http://pypi.python.org/pypi?:action=list_classifiers
      classifiers=[
          "Programming Language :: Python",
          "Topic :: Internet :: WWW/HTTP",
          "Topic :: Internet :: WWW/HTTP :: WSGI :: Middleware",
        ],
      keywords='web pyramid wsgi repoze who paste',
      author='Simples Consultoria',
      author_email='products@simplesconsultoria.com.br',
      url='https://github.com/simplesconsultoria/repoze.who.plugins.webservice',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['repoze', 'repoze.who', 'repoze.who.plugins'],
      include_package_data=True,
      zip_safe=False,
      install_requires=requires,
      tests_require=tests_requires,
      test_suite="repoze.who.plugins.webservice",
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
