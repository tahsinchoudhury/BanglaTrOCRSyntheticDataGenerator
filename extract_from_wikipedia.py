from bs4 import BeautifulSoup
import requests
import re
import click

def text2chunks(text, n_words):
    words = text.split(" ")
    return [' '.join(chunk) for chunk in zip(*[iter(words)]*n_words)]

pattern = re.compile(r'\[\d+\]')
WIKIPEDIA_LINK = "https://bn.wikipedia.org/wiki/Special:Random"

@click.command()
@click.option('--nb_visited_pages', default=10, help='Number of wikipedia visited pages')
@click.option('--max_chunk_size', default=10, help='Max number of words in the extracted samples')
@click.option('--output_path', default="wikipedia_dataset.txt", help='Output path of the extracted dataset (.txt)')
def extract_from_wikipedia(nb_visited_pages, max_chunk_size, output_path):
    wikipedia_pages = []

    visited_count = 0
    for _ in range(nb_visited_pages):
        # page = requests.get(WIKIPEDIA_LINK)
        # soup = BeautifulSoup(page.content, 'html.parser')
        # p = soup.find_all('p')
        # text = p[1].get_text() if len(p) > 2 else "
        text = ""
        
        while len(text) < 50 or "\\" in text.replace("\n","").replace("\u200b",""):
            page = requests.get(WIKIPEDIA_LINK)
            soup = BeautifulSoup(page.content, 'html.parser')
            p = soup.find_all('p')
            text = p[1].get_text() if len(p) > 2 else ""

        text = re.sub(pattern, '', text.replace("\n","").replace("\u200b","").replace("\xa0","").replace("\ufeff",""))
        wikipedia_pages.extend( text2chunks(text, max_chunk_size) )

        visited_count += 1
        if visited_count % 10 == 0:
            print(f"Number of pages visited: {visited_count}")
        
    with open(output_path, 'w') as f:
        for item in wikipedia_pages:
            f.write("%s\n" % item)
    return 

if __name__ == '__main__':
    extract_from_wikipedia()