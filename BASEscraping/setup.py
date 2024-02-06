from setuptools import setup, find_packages

setup(
    name='BASEscraping',
    version='0.1',
    author='Luca Brilhaus, Leander Waddel',
    author_email='',
    description='A short webscraping package that allows you to scrape websites behind paywalls using your credentials',
    install_requires = ['openpyxl', 'pandas', 'newspaper3k', 'nltk'],
    packages=find_packages(),  # Automatically discover and include all packages
)