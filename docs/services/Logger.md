# **Logger Documentation**

## **Overview**
The `Logger` utility is designed to save error logs to the database for efficient debugging and troubleshooting. It ensures that all errors are captured automatically unless explicitly handled by the user.

You can use the `Logger` by importing it into your code as follows:

```python
from nexler.services import Logger
```

### **Key Features**
- Automatically logs unhandled exceptions.
- Provides a simple method to log custom error messages.
- Stores error details in a centralized database for analysis.

---

## **Usage**

### **Logging Custom Messages**
To log a custom message, use the `Logger.log()` method:

```python
Logger.log("Your custom error message here")
```

#### Example:
```python
try:
    # Some code that might raise an exception
    risky_operation()
except Exception as e:
    Logger.log(f"Error occurred: {str(e)}")
    raise  # Re-raise the exception if needed
```

---

## **Automatic Error Logging**
All unhandled exceptions are automatically logged by the `Logger`. This ensures that critical errors are not missed.

For example:
```python
def perform_task():
    result = 10 / 0  # This will raise a ZeroDivisionError
```
Even if you don't explicitly log the exception, the `Logger` will capture and store it.

---

## **Best Practices**
1. **Use for Custom Debugging**: While the `Logger` automatically captures errors, it's recommended to log specific events or exceptions critical to your application flow.
   
2. **Avoid Overuse**: Log only meaningful errors or information to avoid cluttering the logs.

3. **Review Logs Regularly**: Use the stored logs to analyze recurring issues or unexpected behaviors.
