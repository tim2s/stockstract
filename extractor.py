import datetime

from bs4 import BeautifulSoup

from value_extractor import extract_money, extract_percent, parse_german_float


def translate_row(row_name):
  values = {
    'Umsatz': 'revenue',
    'Umsatz je Aktie': 'revenuePerStock',
    'Cashflow je Aktie': 'cashFlowPerStock',
    'Eigenkapitalrendite': 'returnOnEquity',
    'Umsatzrendite': 'returnOnRevenue',
    'Gesamtrendite': 'totalReturn',
    'Return on Investment': 'returnOnInvest',
    'Anlageintensität': 'shareOfLongTermAssets',
    'Arbeitsintensität': 'shareOfCurrentAssets',
    'Eigenkapitalquote': 'shareOfEquity',
    'Verschuldungsgrad': 'debtToEquityRatio',
    'Liquidität 1. Grades': 'firstGradeLiquidity',
    'Liquidität 2. Grades': 'secondGradeLiquidity',
    'Liquidität 3. Grades': 'thirdGradeLiquidity',
    'Deckungsgrad 1': 'firstCoverageRatio',
    'Deckungsgrad 2': 'secondCoverageRatio',
    'Deckungsgrad 3': 'thirdCoverageRatio',
    'Fremdkapitalquote': 'gearingRatio',
    'Dividende': 'dividend',
    'Dividende je Aktie': 'dividendPerShare',
    'Gewinn je Aktie': 'earningsPerShare',
    'Operatives Ergebnis': 'operatingProfit',
    'Jahresüberschuss': 'earnings',
    'Forschungs- und Entwicklungskosten': 'researchAndDevelopment',
    'Ausstehende Aktien in Mio.': 'amountOfSharesOutstanding',
    'Cash flow': 'cashFlow',
    'Cashflow aus der Investitionstätigkeit': 'cashFlowFromInvestments',
    'Cashflow aus der Finanzierungstätigkeit': 'cashFlowFromFinance',
    'Veränderung der Finanzmittel': 'cashReserveDelta',
    'Finanzmittel am Ende der Periode': 'cashReserveEndOfPeriod',
    'Buchwert je Aktie': 'bookValuePerShare',
    'Anzahl der Mitarbeiter': 'amountOfEmployees',
    'Personalkosten': 'laborCost',
    'Umsatz pro Mitarbeiter': 'revenuePerEmployee'
  }
  if row_name in values:
    return values[row_name]
  else:
    return None


def extract_years_header(table, title):
  years = []
  for header_column in table.thead.tr("th"):
    if header_column.contents[0].string != title:
      years.append(int(header_column.contents[0].string))
  return years


class Extractor:

  def __init__(self, file_content, reference):

    self.soup = BeautifulSoup(file_content, 'html.parser')
    content_section = self.soup.find(id='vwd_content')
    self.content_section = content_section
    self.reference = reference

  @staticmethod
  def has_isin_content(span):
    return 'ISIN' in span.string

  def stock_info(self):
    return {'head': self.head(), }

  def head(self):

    stock_head_data = {}

    price_info_section = self.content_section.find_all("div", {"class": "einzelkurs_header"}, limit=2, recursive=False)
    stock_head_data['title'] = price_info_section[0].h1.string
    price_text = price_info_section[1].find(title="aktueller Wert").string.replace(u'\xa0', ' ')

    stock_head_data['current_price'] = extract_money(price_text)
    isin_and_wkn = price_info_section[1](string=self.has_isin_content)[0].string
    stock_head_data['isin'] = isin_and_wkn.split('|')[0].replace('ISIN', '').strip()
    stock_head_data['wkn'] = isin_and_wkn.split('|')[1].replace('WKN', '').strip()
    stock_head_data['timestamp'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    stock_head_data['url'] = self.reference

    return stock_head_data

  def content(self):

    tables = self.content_section("table")

    owner_structure = self.extract_owners(tables[0])

    balance_sheet = self.extract_balance_sheet(tables[2])

    income_statement = self.extract_kpi(tables[3], 'Gewinn- und Verlustrechnung')

    cash_flow = self.extract_kpi(tables[4], 'Jahrescashflow')

    stock_data = self.extract_kpi(tables[5], 'Wertpapierdaten')

    kpi_data = self.extract_kpi(tables[6], 'Bewertungszahlen')

    employees = self.extract_kpi(tables[7], 'Mitarbeiter')

    all_kpi = {**income_statement, **cash_flow, **stock_data, **kpi_data, **employees}

    return {'balance_sheet': balance_sheet, 'head': self.head(), 'owner_structure': owner_structure, 'kpi': all_kpi}

  def extract_owners(self, owner_table):

    owner_data = []
    all_rows = owner_table("tr")
    for row in all_rows:
      cells = row("td")
      if cells:
        owner_data.append({
          'owner': cells[0].string,
          'percent': extract_percent(cells[1].string)
        })
    return owner_data

  def extract_kpi(self, kpi_table, header_name):

    years = extract_years_header(kpi_table, header_name)

    kpi_data = {
      'years': years
    }

    for value_row in kpi_table.tbody("tr"):
      columns = value_row("td")
      row_name = columns[0].string

      kpi_field = translate_row(row_name)
      if kpi_field is None:
        print('unitentified row', row_name)
      else:
        row_values = []
        for column_index in range(1, len(columns)):
          value = parse_german_float(columns[column_index].string)
          year = years[column_index - 1]
          row_values.append({'year': year, 'value': value})
        kpi_data[kpi_field] = row_values

    return kpi_data

  def extract_balance_sheet(self, balance_sheet_table):

    years = extract_years_header(balance_sheet_table, 'Bilanz')

    balance_sheet = {
      'years': years,
      'assets': {},
      'liabilities_and_equity': {}
    }

    active_element = {}

    for value_row in balance_sheet_table.tbody("tr"):
      columns = value_row("td")
      row_name = columns[0].string

      if row_name == 'Aktiva':
        active_element = balance_sheet['assets']
        continue

      if row_name == 'Passiva':
        active_element = balance_sheet['liabilities_and_equity']
        continue

      if row_name.strip() == '':
        continue

      row_values = []
      for column_index in range(1, len(columns)):
        value = parse_german_float(columns[column_index].string)
        year = years[column_index - 1]
        row_values.append({'year': year, 'value': value})
      active_element[row_name] = row_values

    return balance_sheet
