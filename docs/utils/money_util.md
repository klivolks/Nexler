# `money_util.py` User Documentation

The `money_util.py` module provides a collection of functions to perform money related operations such as amount validation, conversion to text, applying and removing formatting, getting currency symbol and converting between different currencies. Here are the details of each function:

## Functions

- **validate_amount(amount)**: Validates if the provided amount can be converted to a float. Returns True if valid, otherwise False.

- **convert_to_text(amount, country, with_currency=False)**: Converts a given numerical amount into words. This function takes an optional parameter `with_currency`. If set to True, the returned string includes the name of the currency.

- **apply_formatting(amount, format, country)**: Applies regional formatting to the given amount according to the provided format (e.g., "IN" for Indian formatting, "INT" for International formatting). It returns the amount formatted as a currency string with the currency symbol obtained from the given country name.

- **remove_formatting(amount, country)**: Removes formatting from the given amount and returns the numerical value. The function requires the country name to identify the symbol to be stripped.

- **get_symbol(country)**: Returns the symbol of the currency used in the provided country.

- **convert_currency(amount, baseCurrency, targetCurrency)**: Converts a given amount from the base currency to the target currency using real-time exchange rates.

## Usage

To use these utility functions, simply import the required functions from the `app.utils.money_util` module and use them in your code where needed.

For example:

```python
from app.utils.money_util import validate_amount, convert_to_text, convert_currency

amount = '1234.56'
base_currency = 'USD'
target_currency = 'EUR'

if validate_amount(amount):
    print(convert_to_text(amount, base_currency, with_currency=True))  
    converted_amount = convert_currency(amount, base_currency, target_currency)
    print(f"The amount in {target_currency} is {converted_amount}")
else:
    print("Invalid amount")
```

In this example, the `validate_amount` function is used to validate if the amount is a valid numerical value. If it is valid, the `convert_to_text` function is used to convert it to words, and `convert_currency` is used to convert the amount from USD to EUR. If the amount is not valid, an error message is printed.