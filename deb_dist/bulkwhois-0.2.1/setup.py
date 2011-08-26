from distutils.core import setup

setup(
    name='BulkWhois',
    version='0.2.1',
    author='CSIRT Foundry / Chris Horsley',
    author_email='chris.horsley@csirtfoundry.com',
    packages=['bulkwhois'],
    scripts=[],
    url='http://pypi.python.org/pypi/BulkWhois/',
    download_url='http://github.com/csirtfoundry/BulkWhois/tarball/master',
    license='LICENSE.txt',
    description='Interfaces for popular bulk WHOIS servers',
    long_description=open('README.txt').read(),
 )
