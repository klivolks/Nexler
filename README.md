# Nexler by klivolks

---

<p align="left">
  <a href="https://www.python.org/"><img alt="Python" src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white"/></a>
</p>

![Python](https://img.shields.io/badge/python-v3.7+-blue.svg)
![Docker](https://img.shields.io/badge/docker%20build-automated-066da5.svg)

---

Nexler is a lightweight yet powerful framework for simplifying the development of RESTful APIs in Python. With a strong focus on component generation and URL handling, Nexler provides a streamlined process for building and managing your API components. Its modular structure makes it easy to develop, maintain, and understand your codebase.

Compared to existing frameworks like Flask, FastAPI, and Django, Nexler focuses on providing developers with more built-in tools for common tasks in API development. It has an integrated UserService for user authentication and a create command for automating the creation of components, logic modules, and routes.

- Unlike Flask, Nexler's built-in tools eliminate the need for additional plugins for tasks like user authentication and module generation. This simplifies the development process and reduces potential compatibility issues between different plugins.

- Compared to FastAPI, Nexler does not require Pydantic for data validation and serialization. Instead, it uses simple decorators and intuitive Python syntax, making it easier for beginners and more convenient for experienced developers.

- While Django is a full-fledged framework designed for building complex web applications, Nexler is designed specifically for building APIs. This makes Nexler more lightweight and efficient for API development.

Remember that Nexler, Flask, FastAPI, and Django all have their own strengths and are better suited for different types of projects. Choose the one that best fits your specific needs.

## Table of Contents

1. [Features](#features)
2. [Installation](#installation)
3. [Structure](#structure)
4. [Usage](#usage)
5. [Difference from Other Frameworks](#difference-from-other-frameworks)
6. [UserService](#userservice)
7. [Database Migrations](#database-migrations)
8. [Optional Commands](#optional-commands)
9. [Upgrade](#upgrade)
10. [Documentation](#documentation)
11. [Contributing](#contributing)
12. [License](#license)

## Features

- **Component Generation:** Nexler automates the creation of Python components with basic HTTP method templates.
- **URL Handling:** Nexler provides an easy way to map your new components to specific URLs in your application.
- **Error Handling:** Nexler implements a standard approach for error handling in your API, improving code readability.
- **Database Operations:** Nexler uses Daba for database operations. For more information on Daba, visit https://pypi.org/project/daba/
- **UserService:** UserService simplifies user authentication and authorization, offering built-in methods to protect API routes.
- **Database Migration:** Nexler provides an automatic migration command for JSON files inside the migrations folder.
- **API Verification:** The ApiService can be enabled by setting API_VERIFICATION=on in the .env file. This verifies the APIs against predefined rules.

## Installation

1. Clone the repository to your local machine. Make sure the directory is empty.
```shell
git clone https://github.com/klivolks/nexler.git .
```

2. Install Nexler.
```shell
pip install .
```

## Structure

Nexler uses a clean and organized structure. The `app/` directory is the main source folder, it contains:

- `components

/`: Stores all the components.
- `logic/`: Houses the logic modules associated with components.
- `routes/`: Contains route definitions for the application.
- `models/`: Contains all the data models used in the application.
- `services/`: Houses services like UserService.
- `utils/`: Contains various utilities to keep the code DRY.
- `docs/`: Contains documentation for Nexler and its usage.

## Usage

### Creating a Component

You can create a new component using the `create` command. The command requires the component's name and its URL. You can also specify optional URL variables.

```shell
nexler create component MyComponent --url "/mycomponent" --variables=id,name
```

In this example, a new component named 'MyComponent' is created and mapped to the '/mycomponent' URL. The component will have `id` and `name` as parameters for its methods, specified by the `--variables` argument.

### Creating Logic

You can create new logic for a component using the `create` command. The command requires the name of the module and the component.

```shell
nexler create logic MyLogic MyComponent
```

In this example, a new logic named 'MyLogic' is created for the component named 'MyComponent'.

## Difference from Other Frameworks

Nexler stands out from other Python web frameworks like Flask, FastAPI, and Django with its approach to simplifying RESTful API development.

1. **Nexler vs Flask:** Flask is a micro-framework that leaves much of the decision making to developers. Unlike Flask, Nexler comes with more built-in tools like UserService for user authentication and a `create` command for automating module generation. These tools make the development process smoother and remove the need for additional plugins.

2. **Nexler vs FastAPI:** FastAPI uses Pydantic for data validation and serialization, which can be verbose and cumbersome. Nexler, on the other hand, uses simpler decorators and intuitive Python syntax for these tasks. This makes Nexler easier to grasp for beginners and more convenient for experienced developers.

3. **Nexler vs Django:** Django is a full-featured framework designed for creating complex web applications, whereas Nexler is primarily designed for building RESTful APIs. This makes Nexler more lightweight and efficient for API development.

## UserService

UserService provides a way to manage user authentication and authorization. This service can be imported from `app.services.UserService`. UserService exposes a `userId` property to access the authenticated user's ID and a `protected` decorator to protect routes that require user authentication.

Example usage:

```python
from flask_restful import Resource
from app.services.UserService import user, protected

class Test(Resource):
  # protect a route
  @protected
  def get(self):
      return "This route is protected!"
```

## Database Migrations

To migrate all JSON files inside the migrations folder automatically, use the `nexler migrate` command. The name of each JSON file should correspond with the collection name, and the contents should follow the format `[{doc1},{doc2},...]`.

```shell
nexler migrate
```

## Optional Commands

You can customize the creation of components and logic with optional arguments. Here are a few examples:

1. To specify optional URL variables during component creation:

```shell
nexler create component MyComponent --url "/mycomponent" --variables=doc,id
```

2. To create a protected component that requires user authentication:

```shell
nexler create component MyProtectedComponent --url "/myprotectedcomponent" --protected
```

3. To specify the HTTP methods for a component:

```shell
nexler create component MyComponent --url "/myurlcomponent" --methods=get


```

## Upgrade

You can upgrade to the latest version of Nexler by running the following command:

```shell
nexler upgrade
```

## Documentation

More detailed documentation can be found in the `docs/` folder of the repository. It provides a comprehensive guide on using and extending the Nexler framework.

## Contributing

We welcome contributions to Nexler. To contribute, please fork the repository and create a pull request with your changes.

## License

Nexler is open-source software, licensed under the [AGPL 3.0 license](LICENSE).

---

For more information about Nexler, feel free to contact klivolks or open an issue on GitHub.

**Disclaimer:** Nexler is a work in progress. There may be occasional updates, and we welcome any feedback or suggestions for improvement.