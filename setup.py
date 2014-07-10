from setuptools import setup, find_packages

setup(
    name='python-zanox-api',
    version=__import__('zanox').__version__,
    description='Python Zanox API - https://developer.zanox.com',
    long_description=open('README.rst').read(),
    # Get more strings from http://www.python.org/pypi?:action=list_classifiers
    author='Bas Koopmans',
    author_email='email@baskoopmans.nl',
    url='http://github.com/baskoopmans/python-zanox-api',
    download_url='http://github.com/baskoopmans/python-zanox-api/downloads',
    license='BSD',
    packages=find_packages(exclude=['ez_setup']),
    include_package_data=True,
    zip_safe=True,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
