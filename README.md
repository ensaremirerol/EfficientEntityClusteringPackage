# Efficient Entity Clustering Package (subject to change)

## 🖇️ Purpose

This package is designed to provide a base for Efficient Entity Clustering (EEC) application. It provides set of function and classes to build a the EEC application.

## 📦 What is included

It includes the following abstract classes:

-   IEntityRepository: interface for entity repository
-   IClusterRepository: interface for cluster repository
-   IMentionClusteringMethod: interface for mention clustering method
-   IUserRepository: interface for user repository

following Data classes:

-   EntityModel: data class for entity
-   ClusterModel: data class for cluster
-   UserMentionModel: data class for user

and the following concrete classes:

-   BaseEntityRepository: base class for entity repository
-   BaseClusterRepository: base class for cluster repository
-   BaseMentionClusteringMethod: base class for mention clustering method
-   BaseUserRepository: base class for user repository

-   Neo4jEntityRepository: concrete class for entity repository
-   Neo4jClusterRepository: concrete class for cluster repository
-   Neo4jUserRepository: concrete class for user repository

Those concrete classes are able to provide a base for EEC application.

## 🛠️ How to install

On the root directory of the project, run the following command:

```bash
pip install ./package
```

-   Note: the package is not available on PyPI and not planned to be.

## 🛫 How to use

A demo file is provided in the `demo` directory. It shows the basic functionalities of the package. But it is not exhaustive.
Also, if you want to use Neo4J as a database, you need to serve a Neo4J database.

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details
