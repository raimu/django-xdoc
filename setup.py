from setuptools import setup


with open('requirements.txt') as f:
    required = f.read().splitlines()


setup(
    name='django-xdoc',
    version='0.0.1',
    packages=['xdoc'],
    include_package_data=True,
    zip_safe=False,
    url='https://github.com/raimu/django-xdoc',
    license='AGPL 3',
    install_requires=required
)
