from setuptools import setup
import subprocess
import os.path

long_description = (open('README.rst').read() + 
                    open('CHANGES.rst').read() +
                    open('TODO.rst').read())

setup(
    name='django-ajaxwidgets',
    version='0.0.1',
    description='AJAX Widgets for Django.',
    author='Jeff Schwaber, LoFi Art',
    author_email='freyley@gmail.com',
    long_description=long_description,
    url='',
    packages=['ajaxwidgets'],
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
        'ajaxwidgets': [
            'static/ajaxwidgets/js/*.js',
        ]
    },
)
