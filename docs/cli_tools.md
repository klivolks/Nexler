# Nexler CLI Tools

This document provides an overview of Nexler CLI (Command Line Interface) tools that assist in RESTful API development. 

## Table of Contents
1. [Creating a Component](#creating-a-component)
2. [Creating Logic](#creating-logic)
3. [Creating a Model](#creating-a-model)
4. [Database Migration](#database-migration)
5. [Upgrade](#upgrade)
6. [AI Integration](#ai-integration)
7. [Serve](#serve)
8. [Encryption](#encryption)


## Creating a Component

Nexler automates the creation of new components via a simple command that takes the component's name, URL, and optional URL variables.

Use the command:

```shell
nexler create component <ComponentName> [--url="/component_url"] [--variables=var1,var2,...] [--main="FolderName"]
```

Example usage:

```shell
nexler create component MyComponent --url "/mycomponent"
```

This example creates a new component 'MyComponent' and maps it to the '/mycomponent' URL.

### Additional Options

The `create component` command offers further customization:

- Specify optional URL variables:

    ```shell
    nexler create component MyComponent --url "/mycomponent" --variables=doc,id
    ```

- Create a protected component requiring user authentication:

    ```shell
    nexler create component MyProtectedComponent --url "/myprotectedcomponent" --protected
    ```

- Specify the HTTP methods for a component:

    ```shell
    nexler create component MyComponent --url "/myurlcomponent" --methods=get
    ```
- Creating Subcomponent for a main component

    ```shell
  nexler create component MyComponent --url "/myurlcomponent" --main=MainComponent
  ```
## Creating Logic

Logic modules are associated with components to encapsulate application's business rules. Nexler simplifies the creation of new logic modules.

Use the command:

```shell
nexler create logic <LogicName> --component=<ComponentName> [--subcomponent=<SubComponentName>]
```

Now supports optional subcomponent.

Example usage:

```shell
nexler create logic MyLogic --component=MyComponent
```

This example creates a new logic module 'MyLogic' for the component 'MyComponent'.

### Additional Options

The `create logic` command supports customization:

- Create an independent logic module, not associated with any component:

    ```shell
    nexler create logic MyIndependentLogic --independent
    ```
    
- Create a main logic module imported in `__init__.py` of the component:

    ```shell
    nexler create logic SubLogic --component=MyComponent --main=MainLogic
    ```
    
## Creating a Model

Nexler automates new model creation via a simple command. However, before running this command, ensure a `<ModelName>.json` file defining the fields for the model exists in the `app/models/variables/` directory.

Once set, use the following command to create a model:

```shell
nexler create model <ModelName> --logic=<LogicName> [--main=<MainLogicName>]
```

Example usage:

```shell
nexler create model User --logic=HelloWorldLogic --main=HelloWorld
```

This example creates a new model 'User' for the logic 'HelloWorldLogic' in the 'HelloWorld' directory.

### Additional Options

The `create model` command supports customization:

- Create a model associated with a logic module, which shares the parent directory's name:

    ```shell
    nexler create model UserModel --logic=MyLogic
    ```

- Create a standalone model, without linking it to any logic:

    ```shell
    nexler create model UserModel
    ```

Ensure `<ModelName>.json` exists in `app/models/variables/` and is correctly formatted.

## Database Migration

Nexler provides automatic migration for JSON files inside the migrations folder. Each JSON file should

 correspond to a collection name.

Migrate all JSON files using:

```shell
nexler migrate
```

## Upgrade

Upgrade Nexler to its latest version:

```shell
nexler upgrade
```

## AI Integration

Nexler has AI integration which allows you to generate or edit code, create components or insert lines of code using AI. Here's the basic syntax:

```shell
nexler ai <function> [--instruction="instruction here"] [--file="filename here"] [--start="start line number"] [--end="end line number"]
```

Where `<function>` can be `code`, `edit`, `create` or `insert`. If the function is `insert`, a placeholder `[insert]` should be present in the code where you want the insertion to occur.

## Serve

Run development server:

```shell
nexler serve
```
## Encryption

From Nexler 1.2.1, we have new feature of JSON Web Encryption for tokens. Refer token utility for how to use the encryption. This command creates private and public keys that can be shared among other services to decrypt and encrypt tokens. The folder is `./encryption`.

```shell
nexler encrypt generate
```

For detailed Nexler information, refer to the official `docs/` directory documentation. If you need further assistance, feel free to open an issue on GitHub or contact klivolks directly.

