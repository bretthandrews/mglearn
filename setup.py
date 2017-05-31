from setuptools import setup, find_packages

setup(
    name='mglearn',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'numpy',
        'Click',
        'astropy',
        'sdss-marvin'
    ],
    entry_points='''
        [console_scripts]
        hello=mglearn.scripts.click_demo:hello
        select_sample=mglearn.scripts.mglearn_select_sample:select_sample
    ''',
)