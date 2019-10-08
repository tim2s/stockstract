from bs4 import BeautifulSoup

# with codecs.open("xamples/kurse_einzelkurs_profil96056.html", "r", "utf-8") as html_file:


class Indexer:

  def __init__(self, file_content):
    self.soup = BeautifulSoup(file_content, 'html.parser')
    all_linx = self.soup.find_all('a')
    for link in all_linx:
      # continue here
      print(link)
