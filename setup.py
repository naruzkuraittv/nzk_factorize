from setuptools import setup, find_packages

setup(
    name='nzk_factorize',
    version='1.0',
    description='nzk factorization module via FactorDB',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Lord NaruZkurai',
    author_email='no_you@ur_not_gonna_email_me_just_go_to_my_github.com',
    url='https://github.com/platokun/nzk_factorize',
    packages=find_packages(),
    install_requires=['requests'],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: The Unlicense',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6', 
) # i chat gpt'd this, dm me if i should fix something lmfao
