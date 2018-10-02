from setuptools import setup,find_packages

requirements = [
    'tqdm',
    'beautifulsoup4'
]
with open("README.md", "r") as fh:
    long_description = fh.read()
setup(
   name='mangascandl',
   version='1.0.3',
   description='Tool for downloading mangascan from websites',
   author='Suartha Gautama',
   author_email='suartha.gautama@gmail.com',
   long_description=long_description,
   long_description_content_type="text/markdown",
   url="https://github.com/SuarthaGautama/mangascandl",
   packages=find_packages(),
   entry_points = {
       'console_scripts':[
           'mangascandl = mangascandl.mangascandl:main'
       ]
   } ,
   install_requires=requirements, 
)
