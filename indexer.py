from bs4 import BeautifulSoup


class Indexer:

  def __init__(self, file_content):
    self.soup = BeautifulSoup(file_content, 'html.parser')
    self.stock_links = []
    all_linx = self.soup.find_all('a')
    for link in all_linx:
      if 'href' in link.attrs \
        and link.attrs['href'].startswith('https://kurse.boerse.ard.de/ard/kurse_einzelkurs_uebersicht.htn?i=') \
        and len(link("strong")) >= 1:
        notion = link.attrs['href'].replace('https://kurse.boerse.ard.de/ard/kurse_einzelkurs_uebersicht.htn?i=', '')
        self.stock_links.append(notion)

  def get_links(self):
    return self.stock_links
