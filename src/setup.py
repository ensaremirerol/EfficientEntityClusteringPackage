from setuptools import setup, find_packages

setup(
    name='eec',  # Subject to change
    version='0.0.1',
    description='Efficient Entity Clustering',
    author='Ensar Emir EROL',
    author_email='ensaremir.erol99@gmail.com',
    packages=find_packages(),
    install_requires=['numpy', 'gensim', 'neo4j'],
    python_requires='>=3.10',
)
