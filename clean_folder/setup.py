from setuptools import setup, find_packages

setup(
    name='clean_folder',
    version='1.0',
    description='sorts files and extracts archives',
    url='https://github.com/Mykola-Vynnychuk/goit-python-hw-07/tree/main/clean_folder',
    author='Mykola Vynnychuk',
    author_email='nik4779@gmail.com',
    license='MIT',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'clean-folder = clean_folder.clean:main'
        ]
    }
)
