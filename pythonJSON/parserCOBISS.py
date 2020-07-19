import time
import requests
from bs4 import BeautifulSoup
from os import listdir
from os.path import isfile, join
import io
import frontmatter
import json
import re

def get_sicris_numbers(_files):
    sicris_list = []
    for fname in _files:
        with io.open(fname, 'r', encoding='utf8') as md:
            load = frontmatter.load(md)
            if load['SICRIS'] != '':
                sicris_list.append({
                    'fname': load['fileName'],
                    'sicris': load['SICRIS']
                })
    return sicris_list


def get_bibliography(sicris, lang):
    url = 'http://splet02.izum.si/cobiss/bibliography?code='+sicris+'&langbib='+lang+'&format=11&formatbib=1'
    req = requests.get(url)
    soup = BeautifulSoup(req.content, 'lxml')
    metas = soup.find_all('meta')
    print(metas)
    if len(metas) > 1:
        url = (metas[1].attrs['content']).split('=')[1]
        response = requests.get(url)
        response = wait_for_resource_available(response, time.time(), url)
        return response.content
    return str.encode("")


def wait_for_resource_available(_response, _time, _url):
    timer = 10
    time_wait = 0.5
    while _response.status_code == 200:
        time.sleep(time_wait)
        timer += time_wait
        elapsed_time = int(time.time() - _time)
        _response = requests.get(_url)
        if timer < elapsed_time:
            return None
        if not "Prosimo" in str(_response.content):
            return _response


def format_bib(_bib):
    authors = _bib.find_all('Author')

    entry = {
        'authors': "",
        'title': "",
        'publication': "",
        'links': {
            'doi': '',
            'bioRxiv': '',
            'pubmed': ''
        }
    }

    i = 0
    for author in authors:
        if author.find('FirstName') is not None and author.find('SurName') is not None:
            newAuthor = author.find('SurName').string + " " + author.find('FirstName').string[0]
            if i == len(authors)-1:
                entry['authors'] += newAuthor + "."
            else:
                entry['authors'] += newAuthor + ", "
        i += 1


    titles = _bib.find_all('Title')
    entry['title'] = titles[0].string

    if len(titles) > 1:
        entry['publication'] = titles[1].string
        if _bib.find('Numbering') is not None:
            numbering = _bib.find('Numbering')
            pubNum = ""

            print(entry['publication'])
            print(numbering)
            if numbering.find('VolumeNum') is not None and numbering.find('IssueNum') is not None:
                vol = numbering.find('VolumeNum').string
                vol = re.search(r"\b[\d]+\b", vol)
                issue = numbering.find('IssueNum').string
                issue = re.search(r"\b[\d]+\b", issue)
                if vol is not None and issue is not None:
                    pubNum += str.format(", {}({})", vol.group(), issue.group())
            elif numbering.find('VolumeNum') is not None:
                vol = numbering.find('VolumeNum').string
                vol = re.search(r"\b[\d]+\b", vol)
                if vol is not None:
                    pubNum += ", " + vol.group()
            elif numbering.find('IssueNum') is not None:
                issue = numbering.find('IssueNum').string
                issue = re.search(r"\b[\d]+\b", issue)
                if issue is not None:
                    pubNum += str.format(", {}", issue.group())

            if numbering.find('ArtPageNums') is not None:
                pages = numbering.find('ArtPageNums').string
                pages = pages.split(' ')[-1]
                pubNum += ":" + pages

            if numbering.find('Year') is not None:
                year = numbering.find('Year').string
                year = re.search(r"\b[\d]+\b", year)
                if year is not None:
                    pubNum += ", " + year.group()

            print(entry['publication'] + pubNum)
            entry['publication'] += pubNum

    if _bib.find('DOI') is not None:
        entry['links']['doi'] = 'https://dx.doi.org/' + _bib.find('DOI').string

    print(entry)
    return entry


def export_biblio(xml):
    soup = BeautifulSoup(xml, 'xml')
    entries = soup.find_all('BiblioEntry')
    exported_bio = {
        "entries": []
    }
    for bio_entry in entries:
        exported_bio['entries'].append(format_bib(bio_entry))
    return exported_bio


'''
    BIBILOGRAPHY FORMAT EXAMPLE
    PRIIMEK, Ime. Naslov. Publikacija, letnik, številka, str. 100-200
'''
# ('http://splet02.izum.si/cobiss/bibliography?code=18199&langbib=slv&format=11&formatbib=1', allow_redirects=True)
path = './content/sl/osebje'
files = [f for f in listdir(path) if f != '_index.md' and isfile(join(join(path, f), "/index.md"))]
for f in listdir(path):
    if f != '_index.md' and isfile(path + '/' + f + "/index.md"):
        files.append(path + '/' + f + "/index.md")
print(files)
reference_people = get_sicris_numbers(files)
ref = reference_people
'''
#TO DOWNLOAD BIBLIOGRAPHY
for person in ref:
    print(person)
    biblio = get_bibliography(person['sicris'], 'slv')
    with io.open('./biblioXML/'+person['fname']+'.xml', 'wb') as file:
        file.write(biblio)
'''
for person in ref:
    with io.open('./biblioXML/'+person['fname']+'.xml', 'r', encoding='utf8') as f:
        print(person['fname'])
        file_data = f.read()
        if len(file_data) > 1:
            toWrite = export_biblio(file_data)
            fname = './data/osebje/publ/' + person['fname'] + '.json'

            with io.open(fname, 'w+', encoding='utf8') as to:
                json.dump(toWrite, to)