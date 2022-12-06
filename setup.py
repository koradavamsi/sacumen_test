from turtle import setup
import setuptools

setuptools.setup(
	name='sacumen_test',
	version='1.0',    
	description='A tool to convert yaml, cfg, conf files to json, env files and set os environment', 
	url='https://github.com/koradavamsi',
	author='Vamsi Korada',
	packages=setuptools.find_packages(),
	classifiers = [
		'Programming Language :: Python :: 3',
		'Operating System :: OS Independent',
	],
	python_requires='>=3.6',

)
