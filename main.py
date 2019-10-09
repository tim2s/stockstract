import codecs
import json
import urllib.request

from extractor import Extractor
from indexer import Indexer
from url_builder import company_details_url


def run_single():

  # 110067 Volkswagen
  # 6223347 Linde
  # 103050 Henkel

  notion = '103050'
  url = company_details_url(notion)
  with urllib.request.urlopen(url) as html_file:
    extractor = Extractor(html_file.read(), url)
    stock_main_data = extractor.content()

  with open('data/' + stock_main_data['head']['isin'] + '.json', 'w') as json_file:
    json.dump(stock_main_data, json_file)


def run_all():

  notions = []

  #with codecs.open("xamples/dax.html", "r", "utf-8") as html_file:
  # https://kurse.boerse.ard.de/ard/indizes_einzelkurs_uebersicht.htn?i=849976
  with urllib.request.urlopen("https://kurse.boerse.ard.de/ard/indizes_einzelkurs_uebersicht.htn?ascdesc=ASC&i=849976&sektion=portrait&sortierung=descriptionShort&offset=100") as html_file:
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
  run_all()
