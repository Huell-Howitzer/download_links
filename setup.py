from urllib import request
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

with open("requirements.txt", "r") as req_file:
    requirements = req_file.read().splitlines()

setuptools.setup(
    name='download_links',
    use_scm_version=True,
    author='Ryan M. Howell',
    author_email='rmhowell@protonmail.com',
    description='Python link download module',
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=['download_links'],
    install_requires=requirements,
)
