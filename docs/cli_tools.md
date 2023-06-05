# Nexler CLI Tools

This document will help you understand how to utilize the Nexler CLI (Command Line Interface) tools to help simplify your RESTful API development. 

## Table of Contents
1. [Creating a Component](#creating-a-component)
2. [Creating Logic](#creating-logic)
3. [Creating a Model](#creating-a-model)
4. [Database Migration](#database-migration)
5. [Upgrade](#upgrade)


## Creating a Component

Nexler provides a simple command to automate the creation of new components. The command takes the component's name and its URL as arguments. You can also specify optional URL variables.

The basic syntax for the command is:

```shell
nexler create component <ComponentName> --url "/component_url" --variables=var1,var2,...
```

Example usage:

```shell
nexler create component MyComponent --url "/mycomponent"
```

In this example, a new component named 'MyComponent' is created and mapped to the '/mycomponent' URL.

### Additional Options

The `create component` command supports additional options for customization:

- To specify optional URL variables:
    ```shell
    nexler create component MyComponent --url "/mycomponent" --variables=doc,id
    ```

- To create a protected component that requires user authentication:
    ```shell
    nexler create component MyProtectedComponent --url "/myprotectedcomponent" --protected
    ```

- To specify the HTTP methods for a component:
    ```shell
    nexler create component MyComponent --url "/myurlcomponent" --methods=get
    ```

## Creating Logic

Logic modules can be associated with components to encapsulate the business rules of the application. Nexler simplifies the creation of new logic with a straightforward command.

The basic syntax for the command is:

```shell
nexler create logic <LogicName> --component=<ComponentName>
```

Example usage:

```shell
nexler create logic MyLogic --component=MyComponent
```

In this example, a new logic named 'MyLogic' is created for the component named 'MyComponent'.

### Additional Options

The `create logic` command supports additional options for customizing the behavior of the logic module:

- To create an independent logic module, not associated with any specific component:
    ```shell
    nexler create logic MyIndependentLogic --independent
    ```
    This command creates a new logic module named 'MyIndependentLogic' which is not tied to a specific component.

- To create a main logic module which will be imported in `__init__.py` of the component:
    ```shell
    nexler create logic SubLogic --component=MyComponent --main=MainLogic
    ```
    This command creates a new logic module named 'SubLogic' for the component 'MyComponent' inside 'MainLogic' folder and ensures it's imported in the `__init__.py` of the component.
## Creating a Model

With Nexler, you can automate the creation of new models by utilizing a straightforward command. However, before running this command, ensure a JSON file with the format `<ModelName>.json` is available in the `app/models/variables/` directory. This JSON file defines the fields for the model and must follow the structure as illustrated in the example below.

Here's the format for the JSON:

```json
[
    {"Variable": "_id", "Format": "str", "Required": false},
    {"Variable": "register_number", "Format": "str", "Required": false}
    // Additional variables
]
```

Once the JSON file is properly set up, you can use the following syntax to create a model:

```shell
nexler create model <ModelName> --logic=<LogicName> [--main=<MainLogicName>]
```

Example usage:

```shell
nexler create model User --logic=HelloWorldLogic --main=HelloWorld
```

In this example, a new model named 'User' is created for the logic named 'HelloWorldLogic' in 'HelloWorld' directory. The model fields will be based on `User.json` in the `app/models/variables/` directory.

### Additional Options

The `create model` command supports additional options for customizing the behavior of the model:

- To create a model associated with a logic module, which has the same name as its parent directory:
    ```shell
    nexler create model UserModel --logic=MyLogic
    ```
    This command creates a new model named 'UserModel' for the logic 'MyLogic' in 'MyLogic' directory.

- To create a standalone model, without linking it to any specific logic or main logic:
    ```shell
    nexler create model UserModel
    ```
    This command creates a standalone model named 'UserModel' without importing it to any specific logic.

Note: In both cases, make sure `<ModelName>.json` exists in `app/models/variables/` and is correctly formatted as per the requirements. if not it will create only _id and dummy data.


## Database Migration

Nexler provides an automatic migration command for JSON files inside the migrations folder. The name of each JSON file should correspond with the collection name, and the contents should follow the format `[{doc1},{doc2},...]`.

To migrate all JSON files, use the following command:

```shell
nexler migrate
```

## Upgrade

You can upgrade to the latest version of Nexler by running the following command:

```shell
nexler upgrade
```

---

For more detailed information on Nexler, refer to the official documentation in the `docs/` directory. Enjoy using Nexler!

If you have questions or need further assistance, feel free to open an issue on GitHub or contact klivolks directly.
