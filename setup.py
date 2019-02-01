from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


setup(
    name='osrsbox',
    version='1.0.0',
    description='A sample Python project',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/osrsbox/osrsbox-db',
    author='The Python Packaging Authority',  # TODO(@PH01L): What do you want the author field to be?
    author_email='email@address.com',  # TODO(@PH01L): What do you want the author email field to be?

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],

    keywords='database tools api runescape',
    packages=find_packages(exclude=['test']),
    python_requires='>=3.6',

    install_requires=['requests', 'mwparserfromhell', 'dateparser'],  # TODO(@PH01L): what other third party packages are there?

    # If there are data files included in your packages that need to be
    # installed, specify them here.
    #
    # If using Python 2.6 or earlier, then these have to be included in
    # MANIFEST.in as well.
    package_data={  # Optional
        'osrsbox_db': [path.join('docs', '*.json')]
    },

    # Although 'package_data' is the preferred approach, in some case you may
    # need to place data files outside of your packages. See:
    # http://docs.python.org/3.4/distutils/setupscript.html#installing-additional-files
    #
    # In this case, 'data_file' will be installed into '<sys.prefix>/my_data'
    # data_files=[('my_data', ['data/data_file'])],  # Optional
    project_urls={
        'Bug Reports': 'https://github.com/osrsbox/osrsbox-db/issues',
        'OSRSBox': 'https://www.osrsbox.com/',
    },
)
