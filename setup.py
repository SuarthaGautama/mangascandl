from setuptools import setup

requirements = [
    'tqdm',
    'beautifulsoup4',
    'html5lib'
]

setup(
   name='mangadl',
   version='1.0',
   description='Tool for downloading mangascan from websites',
   author='Suartha Gautama',
   author_email='suartha.gautama@gmail.com',
   packages=['mangadl'], 
   entry_points = {
       'console_scripts':[
           'mangadl = mangadl.__main__:main'
       ]
   } ,
   install_requires=requirements, 
)