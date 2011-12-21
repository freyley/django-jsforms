from setuptools import setup
import subprocess
import os.path

long_description = (open('README.rst').read() + 
                    open('CHANGES.rst').read() +
                    open('TODO.rst').read())

setup(
    name='django-jswidgets',
    version='0.0.2',
    description='Javascript Widgets for Django.',
    author='Jeff Schwaber, LoFi Art',
    author_email='freyley@gmail.com',
    long_description=long_description,
    url='',
    packages=['jswidgets'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Django',
    ],
    zip_safe=False,
    #test_suite='tests.runtests.runtests',
    package_data={
        'jswidgets': [
            'static/jswidgets/js/*.js',
        ]
    },
)
