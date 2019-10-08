import re


def get_currency(value):
  if '€' in value:
    return 'EUR'
  if '$' in value:
    return 'USD'
  return 'UNKNOWN: ' + value


def get_value(value):
  value_regex = re.compile('([0-9]|\\.)*,[0-9]{2}')
  return parse_german_float(value_regex.search(value)[0])


def extract_money(money_string):
  return {'value': get_value(money_string), 'currency': get_currency(money_string)}


def parse_german_float(value):
  if value == '-':
    return 0
  else:
    return float(value.replace('.', '').replace(',', '.'))


def extract_percent(value):
  return round(parse_german_float(value.replace('%', '')) / 100, 3)
