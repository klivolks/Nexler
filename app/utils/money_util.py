from forex_python.converter import CurrencyRates
import locale
import inflect
from app.utils import mongo_util, str_util
from daba.Mongo import collection

engine = inflect.engine()


def validate_amount(amount):
    try:
        float(amount)
        return True
    except ValueError:
        return False


def convert_to_text(amount, country, with_currency=False):
    whole, fraction = str(float(amount)).split('.')
    fraction = fraction[:2]  # Limit fractional part to two digits

    whole = int(whole)
    fraction = int(fraction)

    whole_part = engine.number_to_words(whole)
    fraction_part = engine.number_to_words(fraction) if fraction != 0 else ''
    col = collection('currencies')
    q = mongo_util.Query()
    q.Name = country
    result = col.getOne(q.build())
    currency_unit = result.get('CurrencyUnit').lower() if whole == 1 else f"{result.get('CurrencyUnit').lower()}s"

    fractional_unit = result.get('FractionUnit').lower() if fraction == 1 else f"{result.get('FractionUnit').lower()}s"

    if with_currency:
        if fraction != 0:
            return f"{whole_part} {currency_unit}, {fraction_part} {fractional_unit}"
        else:
            return f"{whole_part} {currency_unit}"
    else:
        if fraction != 0:
            return f"{whole_part}, {fraction_part}"
        else:
            return whole_part


def apply_formatting(amount, cur_format, country):
    if cur_format == "IN":
        locale.setlocale(locale.LC_ALL, 'en_IN.UTF-8')
    elif cur_format == "INT":
        locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
    return locale.currency(amount, grouping=True, symbol=get_symbol(country))


def remove_formatting(amount, country):
    return locale.atof(amount.strip(get_symbol(country)))


def get_symbol(country):
    col = collection('currencies')
    q = mongo_util.Query()
    q.Name = country
    result = col.getOne(q.build())
    return result.get('Symbol')


def convert_currency(amount, baseCurrency, targetCurrency):
    return CurrencyRates().convert(baseCurrency, targetCurrency, amount if validate_amount(amount) else 0)
