from distutils.core import setup

setup(
    name='BulkWhois',
    version='0.2.0',
    author='CSIRT Foundry / Chris Horsley',
    author_email='chris.horsley@csirtfoundry.com',
    packages=['bulkwhois'],
    scripts=['bin/simple_bulk_whois.py'],
    url='http://pypi.python.org/pypi/BulkWhois/',
    download_url='https://github.com/csirtfoundry/BulkWhois/tarball/master',
    license='LICENSE.txt',
    description='Interfaces for popular bulk WHOIS servers',
    long_description=open('README.txt').read(),
 )
