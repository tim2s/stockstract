import json
import os
import urllib.request

from companyanalysis import CompanyAnalysis
from extractor import Extractor
from indexer import Indexer
from url_builder import company_details_url


index_pages = [
#sdax
  #"https://kurse.boerse.ard.de/ard/indizes_einzelkurs_uebersicht.htn?i=159191",
  #"https://kurse.boerse.ard.de/ard/indizes_einzelkurs_uebersicht.htn?ascdesc=ASC&i=159191&sektion=portrait&sortierung=descriptionShort&offset=50",
#mdax
  #"https://kurse.boerse.ard.de/ard/indizes_einzelkurs_uebersicht.htn?i=159090",
  #"https://kurse.boerse.ard.de/ard/indizes_einzelkurs_uebersicht.htn?ascdesc=ASC&i=159090&sektion=portrait&sortierung=descriptionShort&offset=50",
#dax
  #"https://kurse.boerse.ard.de/ard/indizes_einzelkurs_uebersicht.htn?i=159096",
#eurostoxx
  #"https://kurse.boerse.ard.de/ard/indizes_einzelkurs_uebersicht.htn?i=159194",
#stoxx europe
  #"https://kurse.boerse.ard.de/ard/indizes_einzelkurs_uebersicht.htn?i=159196",
#dow jones
  #"https://kurse.boerse.ard.de/ard/indizes_einzelkurs_uebersicht.htn?i=849973",
# s & p 500
  #"https://kurse.boerse.ard.de/ard/indizes_einzelkurs_uebersicht.htn?i=849976",
  #"https://kurse.boerse.ard.de/ard/indizes_einzelkurs_uebersicht.htn?ascdesc=ASC&i=849976&sektion=portrait&sortierung=descriptionShort&offset=50",
  #"https://kurse.boerse.ard.de/ard/indizes_einzelkurs_uebersicht.htn?ascdesc=ASC&i=849976&sektion=portrait&sortierung=descriptionShort&offset=100",
  #"https://kurse.boerse.ard.de/ard/indizes_einzelkurs_uebersicht.htn?ascdesc=ASC&i=849976&sektion=portrait&sortierung=descriptionShort&offset=150",
  #"https://kurse.boerse.ard.de/ard/indizes_einzelkurs_uebersicht.htn?ascdesc=ASC&i=849976&sektion=portrait&sortierung=descriptionShort&offset=200",
  #"https://kurse.boerse.ard.de/ard/indizes_einzelkurs_uebersicht.htn?ascdesc=ASC&i=849976&sektion=portrait&sortierung=descriptionShort&offset=250",
  #"https://kurse.boerse.ard.de/ard/indizes_einzelkurs_uebersicht.htn?ascdesc=ASC&i=849976&sektion=portrait&sortierung=descriptionShort&offset=300",
  #"https://kurse.boerse.ard.de/ard/indizes_einzelkurs_uebersicht.htn?ascdesc=ASC&i=849976&sektion=portrait&sortierung=descriptionShort&offset=350",
  #"https://kurse.boerse.ard.de/ard/indizes_einzelkurs_uebersicht.htn?ascdesc=ASC&i=849976&sektion=portrait&sortierung=descriptionShort&offset=400",
  #"https://kurse.boerse.ard.de/ard/indizes_einzelkurs_uebersicht.htn?ascdesc=ASC&i=849976&sektion=portrait&sortierung=descriptionShort&offset=450",
  #"https://kurse.boerse.ard.de/ard/indizes_einzelkurs_uebersicht.htn?ascdesc=ASC&i=849976&sektion=portrait&sortierung=descriptionShort&offset=500",

#nasdaq
  #"https://kurse.boerse.ard.de/ard/indizes_einzelkurs_uebersicht.htn?i=149002",
  #"https://kurse.boerse.ard.de/ard/indizes_einzelkurs_uebersicht.htn?ascdesc=ASC&i=149002&sektion=portrait&sortierung=descriptionShort&offset=50",
  #"https://kurse.boerse.ard.de/ard/indizes_einzelkurs_uebersicht.htn?ascdesc=ASC&i=149002&sektion=portrait&sortierung=descriptionShort&offset=100"

#Nikkei
  #"https://kurse.boerse.ard.de/ard/indizes_einzelkurs_uebersicht.htn?i=148429",
  #"https://kurse.boerse.ard.de/ard/indizes_einzelkurs_uebersicht.htn?ascdesc=ASC&i=148429&sektion=portrait&sortierung=descriptionShort&offset=50",
  #"https://kurse.boerse.ard.de/ard/indizes_einzelkurs_uebersicht.htn?ascdesc=ASC&i=148429&sektion=portrait&sortierung=descriptionShort&offset=100",
  #"https://kurse.boerse.ard.de/ard/indizes_einzelkurs_uebersicht.htn?ascdesc=ASC&i=148429&sektion=portrait&sortierung=descriptionShort&offset=150",
  #"https://kurse.boerse.ard.de/ard/indizes_einzelkurs_uebersicht.htn?ascdesc=ASC&i=148429&sektion=portrait&sortierung=descriptionShort&offset=200"
]


def analyze():
  company_candidates = []
  for company_json_file in os.listdir('data'):
    with open('data/' + company_json_file, 'r') as file:
      company_record = json.load(file)
      company_analysis = CompanyAnalysis(company_record)
      company_candidates.append(company_analysis)
      company_analysis.is_valid()
  company_candidates = list(filter(lambda company: company.is_valid(), company_candidates))
  company_candidates = list(filter(lambda company: 0 < company.pe() < 25, company_candidates))
  company_candidates = list(filter(lambda company: 0.04 < company.dividend_yield() < 0.10, company_candidates))
  company_candidates.sort(key=lambda company: company.gn_to_price())
  company_candidates = list(filter(lambda company: company.gn_to_price() < 1.2, company_candidates))
  for cp in company_candidates:
    print(cp)
    print(cp.dividend_values())


def run_single(notion):

  url = company_details_url(notion)
  with urllib.request.urlopen(url) as html_file:
    extractor = Extractor(html_file.read(), url)
    stock_main_data = extractor.content()

  with open('data/' + stock_main_data['head']['isin'] + '.json', 'w') as json_file:
    json.dump(stock_main_data, json_file)


def run_all(index_page):

  notions = []

  with urllib.request.urlopen(index_page) as html_file:
    indexer = Indexer(html_file)
    notions = indexer.get_links()

  for notion in notions:

    url = company_details_url(notion)
    with urllib.request.urlopen(url) as html_file:

      extractor = Extractor(html_file.read(), url)
      stock_main_data = extractor.content()

      if stock_main_data is not None:

        with open('data/' + stock_main_data['head']['isin'] + '.json', 'w') as json_file:
           json.dump(stock_main_data, json_file)


if __name__ == "__main__":
  #for index_page in index_pages:
    #run_all(index_page)
  analyze()
