# Efficient Entity Clustering Package (subject to change)

## 🖇️ Purpose
This package is designed to provide a base for Efficient Entity Clustering (EEC) application. It provides set of function and classes to build a the EEC application.

## 📦 What is included
It includes the following abstract classes:
- IEntity: interface for entity
- IEntityRepository: interface for entity repository
- ICluster: interface for cluster
- IClusterRepository: interface for cluster repository
- IMentionClusteringMethod: interface for mention clustering method

and the following concrete classes:
- BaseEntity: base class for entity
- BaseEntityRepository: base class for entity repository
- BaseCluster: base class for cluster
- BaseClusterRepository: base class for cluster repository
- BaseMentionClusteringMethod: base class for mention clustering method

Those concrete classes are able to provide a base for EEC application.

## 🛠️ How to install
On the root directory of the project, run the following command:
```bash
pip install src/
```
- Note: the package is not available on PyPI and not planned to be.

## 🛫 How to use

A demo file is provided in the `demo` directory. It shows the basic functionalities of the package. But it is not exhaustive. 

## 📝 License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details



