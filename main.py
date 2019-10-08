import codecs
import json
import urllib.request

from extractor import Extractor
from url_builder import company_details_url


def main():

  #kurse_einzelkurs_profil96056.html
  # url = "https://kurse.boerse.ard.de/ard/kurse_einzelkurs_profil.htn?i=98321"
  # url = "https://kurse.boerse.ard.de/ard/kurse_einzelkurs_profil.htn?i=7910800"
  # url = "https://kurse.boerse.ard.de/ard/kurse_einzelkurs_profil.htn?i=138312"
  # url = "https://kurse.boerse.ard.de/ard/kurse_einzelkurs_profil.htn?i=97458"

  notions = ['97458', '138312', '115424']

  for notion in notions:

    url = company_details_url(notion)
    with urllib.request.urlopen(url) as html_file:
    #with codecs.open("xamples/kurse_einzelkurs_profil96056.html", "r", "utf-8") as html_file:

      extractor = Extractor(html_file.read(), url)
      stock_main_data = extractor.content()

      print(stock_main_data)

      with open('data/' + stock_main_data['head']['isin'] + '.json', 'w') as json_file:
         json.dump(stock_main_data, json_file)


if __name__ == "__main__":
  main()
