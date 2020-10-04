import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='persistent-memoization', # Replace with your own username
    version='0.0.1',
    author='Ittay Eyal, Adam Matan',
    author_email='ittay@tx.technion.ac.il, adam@matan.name',
    description='Python persistent memoization package',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/adamatan/python-persistent-memoization',
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3.6',
        'License :: OSI Approved :: MIT License',
        'Development Status :: 3 - Alpha',
        'Operating System :: POSIX',
        'Operating System :: MacOS',
        'Intended Audience :: Science/Research'
    ],
    python_requires='>=3.6',
)
