# Nexler by Klivolks

---

<p align="left">
  <a href="https://www.python.org/"><img alt="Python" src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white"/></a>
  <a href="https://www.openai.com/"><img alt="OpenAI" src="https://img.shields.io/badge/OpenAI-4b11a8?style=for-the-badge&logo=openai&logoColor=white"/></a>
  <a href="https://snyk.io/"><img alt="Snyk" src="https://img.shields.io/badge/Snyk-000000?style=for-the-badge&logo=snyk&logoColor=white"/></a>
</p>

![Python](https://img.shields.io/badge/Python-v3.10+-blue.svg)
![Docker](https://img.shields.io/badge/Docker%20Build-Automated-066da5.svg)
![Snyk](https://img.shields.io/badge/Snyk-Security-orange.svg)
![Swagger](https://img.shields.io/badge/Swagger-Auto%20Documented-green.svg)


---

Nexler is a lightweight yet robust Python framework designed to streamline the development of RESTful APIs. 
It emphasizes efficient URL handling and component generation, enabling developers to build and manage API components with ease. 
With its modular structure, Nexler facilitates the development, maintenance, and scalability of codebases, making it an excellent choice for modern software projects. 
By focusing on simplicity and efficiency, it offers a comprehensive solution for API development.

The framework has seen numerous enhancements over its versions. 
In version **v1.2.1**, Nexler introduced **JSON Web Encryption**, significantly boosting the security and reliability of applications. 
Version **v1.2.19** added the **RedisService**, which improved performance and scalability for high-demand systems. 
Additionally, Nexler became the first AI-integrated framework by embedding **ChatGPT**, enabling users to create, edit, and generate content and code seamlessly. 
This innovation accelerates development workflows and enhances the user experience. 
Furthermore, Nexler offers an in-built currency conversion tool that supports the currencies of 194 countries with daily updates, alongside **Argon2**-based password encryption for top-tier security.

Subsequent versions continued to expand Nexler’s capabilities. 
Starting with **v1.3.0**, Nexler integrated automatic **Swagger** documentation, simplifying API development and integration. 
Version **v1.4.0** introduced **KafkaActions**, which allow event-driven development by subscribing to Kafka topics. 
With **v1.4.12**, Nexler redefined its model-handling approach by adding a Type Definition for more structure and encapsulating database operations within a base class. 
These changes provide a more organized and extensible framework while maintaining backward compatibility with models created in earlier versions.

## Table of Contents

1. [Features](#features)
2. [Installation](#installation)
3. [Structure](#structure)
4. [Usage](#usage)
5. [Difference from Other Frameworks](#difference-from-other-frameworks)
6. [AuthService](#authservice)
7. [CurrencyService](#currencyservice)
8. [PasswordEncryption](#passwordencryption)
9. [Documentation](#documentation)
10. [Contributing](#contributing)
11. [License](#license)

## Features

- **Component Generation:** Nexler automates the creation of Python components with basic HTTP method templates.
- **URL Handling:** Nexler provides an easy way to map your new components to specific URLs in your application.
- **Error Handling:** Nexler implements a standard approach for error handling in your API, improving code readability.
- **Database Operations:** Nexler uses Daba for database operations. For more information on Daba, visit https://pypi.org/project/daba/
- **AuthService:** AuthService simplifies user authentication and authorization, offering built-in methods to protect API routes.
- **CurrencyService:** Provides an in-built currency conversion tool that supports the currencies of 194 countries and updates daily.
- **PasswordEncryption:** Implements Argon2 encryption mechanism for secure password management.
- **Database Migration:** Nexler provides an automatic migration command for JSON files inside the migrations folder.
- **API Verification:** The ApiService can be enabled by setting API_VERIFICATION=on in the .env file. This verifies the APIs against predefined rules.
- **JWE Security:** Now transfer tokens with private encryption Keys. Refer documentation of token_util for more information. To generate keys use nexler cli tools.
- **Swagger Documented:** Automated documentation of APIs with Swagger UI, making it easier to interact with and test API endpoints directly from the browser. This feature improves developer productivity and ensures up-to-date API documentation.
- **Kafka Integrated:** Built-in support for Kafka enables seamless event-driven development, allowing developers to handle real-time data streams and execute actions with greater flexibility and scalability.
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

- `components/`: Stores all the components.
- `logic/`: Houses the logic modules associated with components.
- `routes/`: Contains route definitions for the application.
- `models/`: Contains all the data models used in the application.
- `config/`: Here you can save your app specific configurations to call later.

## Usage

Nexler provides CLI commands for various operations like creating components, logic, database migrations, etc.

 Detailed explanations of these commands along with examples can be found in `docs/cli_tools.md`.

Here is an example of creating a component and logic:

```shell
nexler create component MyComponent --url "/mycomponent" --variables=id,name(optional) --main=MyComponentFolder(optional)
nexler create logic MyLogic --component=MyComponent
```

In these examples, a new component named 'MyComponent' is created and mapped to the '/mycomponent' URL with `id` and `name` as parameters for its methods. Similarly, a new logic named 'MyLogic' is created for the component 'MyComponent'.

## Difference from Other Frameworks

Nexler stands out from other Python web frameworks like Flask, FastAPI, and Django with its approach to simplifying RESTful API development.

1. **Nexler vs Flask:** Flask is a micro-framework that leaves much of the decision-making to developers. Built on Flask framework, Nexler comes with more built-in tools like AuthService for user authentication and a `create` command for automating module generation. These tools make the development process smoother and remove the need for additional plugins.

2. **Nexler vs FastAPI:** FastAPI uses Pydantic for data validation and serialization, which can be verbose and cumbersome. Nexler, on the other hand, uses simpler decorators and intuitive Python syntax for these tasks. This makes Nexler easier to grasp for beginners and more convenient for experienced developers no need to relay on deep logic and complex thinking for basic functionalities.

3. **Nexler vs Django:** Django is a full-featured framework designed for creating complex web applications, whereas Nexler is primarily designed for building RESTful APIs. This makes Nexler more lightweight and efficient for API development along with faster processing and lower resource utilisation.

## AuthService

AuthService provides a way to manage user authentication and authorization. This service can be imported from `nexler.services.AuthService`. AuthService exposes a `userId` property to access the authenticated user's ID and a `protected` decorator to protect routes that require user authentication.

Example usage:

```python
from flask_restx import Resource
from nexler.services.AuthService import user, protected


class Test(Resource):
    # protect a route
    @protected
    def get(self):
        return "This route is protected!"
```

## CurrencyService

CurrencyService provides an in-built currency conversion tool that supports the currencies of 194 countries and updates daily. This service can be imported from `nexler.utils.money_util`.

## PasswordEncryption

Nexler implements Argon2, one of the most secure encryption mechanisms available today, for password management. This can be found in the `nexler.utils.pswd_util`.

## Documentation

For comprehensive and detailed information, please refer to the official Nexler documentation available in the `docs/` directory. This includes guides, tutorials, and detailed descriptions of Nexler features.

## Contributing

Nexler is an open-source project, and we welcome contributions of all kinds. Before contributing, please check the CONTRIBUTING.md document.

## License

This project is licensed under the [MIT License](LICENSE), granting permission to use, modify, distribute, and sublicense the software with minimal restrictions.

---

This README is just an overview of what Nexler can do. Please refer to the official documentation for more details. Enjoy using Nexler!

For more information about Nexler, feel free to contact klivolks or open an issue on GitHub.

**Disclaimer:** Nexler is a work in progress. There may be occasional updates, and we welcome any feedback or suggestions for improvement.