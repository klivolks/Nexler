# Nexler by klivolks

---

<p align="left">
  <a href="https://www.python.org/"><img alt="Python" src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white"/></a>
</p>

![Python](https://img.shields.io/badge/python-v3.7+-blue.svg)
![Docker](https://img.shields.io/badge/docker%20build-automated-066da5.svg)

---

Nexler is a framework for simplifying the development of RESTful APIs. It helps in the creation of components, logic modules, routes, models, and utilities to be used in Python-based web applications.

## Table of Contents

1. [Features](#features)
2. [Installation](#installation)
3. [Structure](#structure)
4. [Usage](#usage)
5. [Optional Commands](#optional-commands)
6. [Upgrade](#upgrade)
7. [Documentation](#documentation)
8. [Contributing](#contributing)
9. [License](#license)

## Features

* Easy module generation: Nexler allows the automatic creation of Python modules with basic HTTP method templates.
* URL handling: Nexler makes it easy to link your new modules to specific URLs in your application.
* Error handling: Nexler incorporates a standard approach for error handling in your API, making your code cleaner and more readable.
* Database operations: Daba is used for database operations, the documentation for which can be found at https://pypi.org/project/daba/
* Optional API verification: The ApiService can be turned on using API_VERIFICATION=on in .env file.

## Installation

1. Clone the repository to your local machine.
```shell
git clone https://github.com/klivolks/nexler.git
```

2. Move to the main Nexler directory.
```shell
cd nexler
```

3. Install Nexler.
```shell
pip install .
```

## Structure

Nexler uses a clean and organized structure. The `app/` directory is the main source folder, it contains:

- `components/`: This is where all the components are stored.
- `logic/`: This directory houses the logic modules associated with components.
- `routes/`: Route definitions for the application are placed here.
- `models/`: All the data models used in the application reside in this folder.
- `utils/`: This contains various utilities which help to DRY out the code. It includes:
    - `dt_util`
    - `request_util`
    - `file_util`
    - `response_util`
    - `mongo_util`
    - `error_util`
    - `str_util`
    - `dir_util`
    - `config_util`
- `docs/`: This folder contains documentation for Nexler and how to use it.

## Usage

### Creating a component

Use the `create` command followed by `component`, the name of the module, and the name of the component to create a new component.

```shell
nexler create component MyComponent --url "/mycomponent" --variables=id,name
```

This will create a new component named 'MyComponent' and map it to the '/mycomponent' URL. The `--variables` argument is optional and if provided, the component will have `id` and `name` as parameters for its methods.

### Creating logic

Use the `create` command followed by `logic`, the name of the module, and the name of the component to create a new logic.

```shell
nexler create logic MyLogic MyComponent
```

This will create a

 new logic named 'MyLogic' for the component named 'MyComponent'.

## Optional Commands

### Creating a protected component

If you want to create a protected component that requires user authentication, use the `--protected` command.

```shell
nexler create component MyProtectedComponent --url "/myprotectedcomponent" --variables=id,name --protected
```

This will create a new protected component named 'MyProtectedComponent' and map it to the '/myprotectedcomponent' URL. The `--variables` argument is optional and if provided, the component will have `id` and `name` as parameters for its methods. Every HTTP method will be decorated with the `@protected` decorator, which requires user authentication.

## Upgrade

You can upgrade to the latest version of Nexler by running the following command:

```shell
nexler upgrade
```

This will fetch the latest version of Nexler from the repository, compare it with your current version, and if an update is available, it will replace the necessary files and directories, followed by a `pip install .` to ensure all dependencies are up-to-date.

## Documentation

Further documentation can be found in the `docs/` folder of the repository. It provides detailed information about the usage and extension of the Nexler framework.

## Contributing

Contributions to Nexler are welcome. Please fork the repository and create a pull request with your changes.

## License

Nexler is open-source software licensed under the [AGPL 3.0 license](LICENSE).

---

For more information about Nexler, please contact klivolks or open an issue on GitHub.

**Disclaimer:** Nexler is a work in progress. There may be occasional updates, and we welcome any feedback or suggestions for improvement.