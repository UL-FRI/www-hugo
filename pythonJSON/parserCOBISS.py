import time
import requests
from bs4 import BeautifulSoup
from os import listdir
from os.path import isfile, join
import io
import frontmatter


def get_sicris_numbers(_files):
    sicris_list = []
    ref_path = './content/sl/osebje/'
    for fname in _files:
        with io.open(ref_path + fname, 'r', encoding='utf8') as md:
            load = frontmatter.load(md)
            if load['SICRIS'] != '':
                sicris_list.append({
                    'fname': fname,
                    'sicris': load['SICRIS']
                })
    print(sicris_list)
    return sicris_list


def get_bibliography(sicris, lang):
    url = 'http://splet02.izum.si/cobiss/bibliography?code='+sicris+'&langbib='+lang+'&format=11&formatbib=1'
    req = requests.get(url)
    soup = BeautifulSoup(req.content, 'lxml')
    metas = soup.find_all('meta')
    url = (metas[1].attrs['content']).split('=')[1]
    response = requests.get(url)
    response = wait_for_resource_available(response, time.time(), url)
    return response.content


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


def format_bibilo(xml):
    soup = BeautifulSoup(xml, 'xml')
    soup = soup.find_all('BiblioEntry')
    print(soup)


# ('http://splet02.izum.si/cobiss/bibliography?code=18199&langbib=slv&format=11&formatbib=1', allow_redirects=True)
path = './content/sl/osebje'
files = [f for f in listdir(path) if f != '_index.md' and isfile(join(path, f))]
reference_people = get_sicris_numbers(files)
for person in reference_people:
    biblio = get_bibliography(person['sicris'], 'slv')
    format_bibilo(biblio)
    break


