from setuptools import setup,find_packages

requirements = [
    'tqdm',
    'beautifulsoup4'
]

setup(
   name='mangascandl',
   version='1.0',
   description='Tool for downloading mangascan from websites',
   author='Suartha Gautama',
   author_email='suartha.gautama@gmail.com',
   packages=find_packages(),
   entry_points = {
       'console_scripts':[
           'mangascandl = mangascandl.mangascandl:main'
       ]
   } ,
   install_requires=requirements, 
)