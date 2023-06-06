import re
import json
import base64
import string
import binascii
from xml.etree import ElementTree as ET
import yaml


def str_encode(s, encoding="utf-8", strType="base64"):
    if strType == "base64":
        return base64.b64encode(s.encode(encoding)).decode(encoding)
    elif strType == "hex":
        return binascii.hexlify(s.encode(encoding)).decode(encoding)
    else:
        raise ValueError(f"Unsupported encoding type: {strType}")


def str_decode(s, encoding="utf-8", strType="base64"):
    if strType == "base64":
        return base64.b64decode(s.encode(encoding)).decode(encoding)
    elif strType == "hex":
        return binascii.unhexlify(s.encode(encoding)).decode(encoding)
    else:
        raise ValueError(f"Unsupported decoding type: {strType}")


def parse(s, datatype="json"):
    if datatype.lower() == "json":
        return json.loads(s)
    elif datatype.lower() == "xml":
        return ET.fromstring(s)
    elif datatype.lower() == "yaml":
        return yaml.safe_load(s)
    else:
        raise ValueError(f"Unsupported datatype: {datatype}")


def remove_punctuation(s):
    return s.translate(str.maketrans('', '', string.punctuation))


def remove_whitespace(s):
    return "".join(s.split())


def capitalize(s):
    return s.title()


def snake_case(s):
    return re.sub(r'\W+', '_', s).strip('_').lower()


def camel_case(s):
    words = s.split('_')
    return words[0].lower() + ''.join(word.title() for word in words[1:])


def extract_numbers(s):
    return ''.join(re.findall(r'\d+', s))
