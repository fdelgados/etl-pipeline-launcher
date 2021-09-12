from setuptools import setup, find_namespace_packages

setup(
    name="web_corpus_builder",
    author="Cisco Delgado",
    author_mail="fdelgados@gmail.com",
    version="0.1",
    packages=find_namespace_packages(
        where="src",
    ),
    package_dir={"": "src"},
)
