from src.common.constants import ALLOW_FILTER_OPERATORS, ALLOW_AGGREGATE_METHODS

FILTER_PATTERN: str = fr'^\s*([a-zA-Z_]\w*)\s*([{ALLOW_FILTER_OPERATORS}])(?![{ALLOW_FILTER_OPERATORS}])\s*(.+?)\s*$'
AGGREGATION_PATTER: str = fr'^\s*([a-zA-Z_]\w*)\s*=\s*({ALLOW_AGGREGATE_METHODS})\s*$'
