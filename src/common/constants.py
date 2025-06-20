from typing import Dict

# Методы и операции, проходящие валидацию при использовании RegEx:
ALLOW_AGGREGATE_METHODS: str = r'avg|min|max'
ALLOW_FILTER_OPERATORS: str = r'=<>'

ERRORS_MAPPING: Dict[str, str] = {
    "argument --file/-f: expected one argument": "Флаг --file/-f не может принимать пустой аргумент",

    "argument --aggregate/-a: expected one argument": "Флаг --aggregate/-a не может принимать пустой аргумент",

    "argument --where/-w: expected one argument": "Флаг --where/-w не может принимать пустой аргумент",
}
