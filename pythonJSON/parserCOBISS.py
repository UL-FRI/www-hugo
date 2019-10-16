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
                    'fname': load['fixName'],
                    'sicris': load['SICRIS']
                })
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


def format_bib(_bib):
    authors = _bib.find_all('Author')
    citation = ""
    i = 0
    for author in authors:
        if i != 0:
            citation += ', '
        citation += str(author.find('SurName').string).upper() + ", " + author.find('FirstName').string
        i += 1
    citation += '. '
    titles = _bib.find_all('Title')
    citation += titles[0].string + '. '
    if len(titles) > 1:
        citation += titles[1].string + ', '
    citation += _bib.find('PubDate').string
    print(citation)


def export_biblio(xml):
    soup = BeautifulSoup(xml, 'xml')
    entries = soup.find_all('BiblioEntry')
    for bio_entry in entries:
        format_bib(bio_entry)


'''
    BIBILOGRAPHY FORMAT EXAMPLE
    PRIIMEK, Ime. Naslov. Publikacija, letnik, številka, str. 100-200
'''
# ('http://splet02.izum.si/cobiss/bibliography?code=18199&langbib=slv&format=11&formatbib=1', allow_redirects=True)
path = './content/sl/osebje'
files = [f for f in listdir(path) if f != '_index.md' and isfile(join(path, f))]
reference_people = get_sicris_numbers(files)
ref = [
{'fname': 'aleksandar_jurišić', 'sicris': '08724'}, {'fname': 'aleksander_sadikov', 'sicris': '20389'},
{'fname': 'alenka_kavčič', 'sicris': '16131'}, {'fname': 'aleš_jaklič', 'sicris': '11161'},
{'fname': 'aleš_leonardis', 'sicris': '05896'},{'fname': 'aleš_smrdel', 'sicris': '18199'},
{'fname': 'aljaž_zrnec', 'sicris': '20334'},{'fname': 'andrej_brodnik', 'sicris': '04967'},
{'fname': 'blaž_zupan', 'sicris': '12536'},{'fname': 'bojan_klemenc', 'sicris': '32887'},
{'fname': 'bojan_orel', 'sicris': '09634'},{'fname': 'borut_batagelj', 'sicris': '22472'},
{'fname': 'borut_robič', 'sicris': '04646'},{'fname': 'boštjan_slivnik', 'sicris': '12766'},
{'fname': 'branko_šter', 'sicris': '14300'},{'fname': 'ciril_bohak', 'sicris': '30062'},
{'fname': 'damir_franetič', 'sicris': '34640'},{'fname': 'damjan_vavpotič', 'sicris': '21393'},
{'fname': 'danijel_skočaj', 'sicris': '18198'},{'fname': 'david_jelenc', 'sicris': '32040'},
{'fname': 'davor_sluga', 'sicris': '33385'},{'fname': 'dejan_lavbič', 'sicris': '25526'},
{'fname': 'denis_trček', 'sicris': '11077'},{'fname': 'domen_tabernik', 'sicris': '34398'},
{'fname': 'erik_štrumbelj', 'sicris': '29486'},{'fname': 'franc_jager', 'sicris': '03438'},
{'fname': 'franc_solina', 'sicris': '09581'},{'fname': 'gašper_fele_žorž', 'sicris': '26513'},
{'fname': 'gašper_fijavž', 'sicris': '16332'},{'fname': 'gregor_jerše', 'sicris': '25594'},
{'fname': 'igor_kononenko', 'sicris': '04242'},{'fname': 'igor_rožanc', 'sicris': '13564'},
{'fname': 'ivan_bratko', 'sicris': '02275'},{'fname': 'iztok_lebar_bajec', 'sicris': '21404'},
{'fname': 'janez_demšar', 'sicris': '16324'},{'fname': 'janoš_vidali', 'sicris': '30920'},
{'fname': 'jure_žabkar', 'sicris': '29020'},{'fname': 'jurij_mihelič', 'sicris': '22475'},
{'fname': 'ksenija_rozman', 'sicris': '28217'},{'fname': 'lan_žagar', 'sicris': '30921'},
{'fname': 'lovro_šubelj', 'sicris': '30918'},{'fname': 'luka_čehovin_zajc', 'sicris': '29381'},
{'fname': 'luka_šajn', 'sicris': '23401'},{'fname': 'marinka_žitnik', 'sicris': '35422'},
{'fname': 'marko_bajec', 'sicris': '16154'},{'fname': 'marko_boben', 'sicris': '19284'},
{'fname': 'marko_janković', 'sicris': '35425'},{'fname': 'marko_poženel', 'sicris': '23953'},
{'fname': 'marko_robnik_šikonja', 'sicris': '15295'},{'fname': 'marko_toplak', 'sicris': '30142'},
{'fname': 'martin_možina', 'sicris': '29021'},{'fname': 'martin_vuk', 'sicris': '23987'},
{'fname': 'matej_guid', 'sicris': '28365'},{'fname': 'matej_kristan', 'sicris': '30155'},
{'fname': 'matej_pičulin', 'sicris': '34600'},{'fname': 'matevž_pesek', 'sicris': '35071'},
{'fname': 'matija_marolt', 'sicris': '15677'},{'fname': 'matjaž_kukar', 'sicris': '14565'},
{'fname': 'matjaž_pančur', 'sicris': '19365'},{'fname': 'miha_janež', 'sicris': '28364'},
{'fname': 'miha_moškon', 'sicris': '29198'},{'fname': 'miha_mraz', 'sicris': '13442'},
{'fname': 'miha_nagelj', 'sicris': '35522'},{'fname': 'mira_trebar', 'sicris': '06795'},
{'fname': 'mojca_ciglarič', 'sicris': '13982'},{'fname': 'narvika_bovcon', 'sicris': '31252'},
{'fname': 'nejc_ilc', 'sicris': '31379'},{'fname': 'neli_blagus', 'sicris': '33188'},
{'fname': 'nikolaj_zimic', 'sicris': '05957'},{'fname': 'patricio_bulić', 'sicris': '19515'},
{'fname': 'petar_vračar', 'sicris': '31563'},{'fname': 'peter_marijan_kink', 'sicris': '24815'},
{'fname': 'peter_peer', 'sicris': '19226'},{'fname': 'polona_oblak', 'sicris': '22723'},
{'fname': 'robert_rozman', 'sicris': '14989'},{'fname': 'rok_rupnik', 'sicris': '15294'},
{'fname': 'rok_češnovar', 'sicris': '33795'},{'fname': 'saša_divjak', 'sicris': '02268'},
{'fname': 'simon_vrhovec', 'sicris': '33190'},{'fname': 'timotej_lazar', 'sicris': '35423'},
{'fname': 'tomaž_curk', 'sicris': '23399'},{'fname': 'tomaž_dobravec', 'sicris': '18188'},
{'fname': 'tomaž_hovelja', 'sicris': '31407'},{'fname': 'tomaž_hočevar', 'sicris': '35424'},
{'fname': 'uroš_lotrič', 'sicris': '16109'},{'fname': 'uroš_čibej', 'sicris': '23400'},
{'fname': 'vida_groznik', 'sicris': '33187'},{'fname': 'zoran_bosnić', 'sicris': '28779'}
]
'''
TO DOWNLOAD BIBLIOGRAPHY
for person in ref:
    print(person)
    biblio = get_bibliography(person['sicris'], 'slv')
    with io.open('./biblioXML/'+person['fname']+'.xml', 'wb') as file:
        file.write(biblio)
'''
for person in ref:
    with io.open('./biblioXML/'+person['fname']+'.xml', 'r', encoding='utf8') as f:
        export_biblio(f.read())
        break
