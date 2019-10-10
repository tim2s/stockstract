import string


def generate_all_links():
  links = []
  letters = list(string.ascii_uppercase)
  max_count = range(5)
  for letter in letters:
    for count in max_count:
      links.append(build_url(letter, count))
  return links


def build_url(letter, page):
  return f'https://kurse.boerse.ard.de/ard/aktien_profile.htn?letter={letter}&offset={page * 25}'
