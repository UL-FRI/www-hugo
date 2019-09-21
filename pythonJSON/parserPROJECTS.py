import json
import re
import io
import os
import requests
from datetime import datetime, date


def match_id(data_json, refrence_json):
    persons = []
    for p in data_json:
        p = p['si']
        for m in p['persons']:
            persons.append(m)

    ids = []
    for ref in refrence_json:
        for a in persons:
            fullname = a['ime']+' '+a['priimek']+' '
            if fullname == ref:
                fname = re.sub(r'\s+', '_', ref.lstrip(' ').rstrip(' ').lower())
                ids.append(
                    {
                        "id": a['id'],
                        "fullname": fname
                    }
                )
                ref = 'blank'
    return ids


def match_lab(ref_lab, ref_people):
    complete_ref = []
    for a in ref_lab:
        fname = './data/laboratorij/' + a + '_mem.json'
        if os.path.isfile(fname):
            with io.open(fname, 'r', encoding='utf8') as labs:
                load = json.load(labs)
                for mem in load:
                    for person in ref_people:
                        mem_fname = re.sub(r'\s+', '_', (mem['name']+' '+mem['surname']).lower())
                        if mem_fname == person['fullname']:
                            complete_ref.append(
                                {
                                    "id": person['id'],
                                    "fullname": person['fullname'] + '_projects',
                                    "lab": a
                                }
                            )
                            person['fullname'] = 'blank'

    return complete_ref


def check_if_project_exist(proj_id, fname):
    if os.path.isfile(fname):
        with io.open(fname, 'r', encoding='utf8') as ref:
            ref_lab = json.load(ref)
            for i in ref_lab:
                if i['id'] == proj_id:
                    return True
            return False
    else:
        return False


def append_json(file, p):
    if os.path.isfile(file):
        with io.open(file, 'r', encoding='utf8') as to:
            project_json = json.load(to)
            temp_list = []
            for obj in project_json:
                temp_list.append(obj)
            temp_list.append(p)
            project_json = temp_list
            with io.open(file, 'w', encoding='utf8') as target:
                target.write(json.dumps(project_json, indent=4, sort_keys=True))
    else:
        with io.open(file, 'w', encoding='utf8') as to:
            arr = [p]
            json.dump(arr, to)


def json_to_md(data_json, ref_ids):
    for p in data_json:
        for x in p['si']['persons']:
            for ref in ref_ids:
                if x['id'] == ref['id']:

                    datetime_str = p['si']['end_date']
                    fname = './data/osebje/projekti/' + ref['fullname'] + '.json'
                    fname_lab = './data/laboratorij/projekti/' + ref['lab'] + '.json'

                    if datetime_str is not None:
                        datetime_obj = datetime.strptime(datetime_str, '%Y-%m-%d %H:%M:%S')
                        current_date_time = datetime.today()
                        if current_date_time > datetime_obj:
                            fname = './data/osebje/projekti/' + ref['fullname'] + '_end.json'
                            fname_lab = './data/laboratorij/projekti/' + ref['lab'] + '_end.json'

                    if not check_if_project_exist(p['id'], fname_lab):
                        append_json(fname_lab, p)
                    append_json(fname, p)


def get_xml():
    url = 'http://projektiweb.fri.uni-lj.si/api/projekti'
    response = requests.get(url)
    with io.open('projekti.json', 'wb+') as file:
        file.write(response.content)
    url = 'http://projektiweb.fri.uni-lj.si/api/vrsteprojektov'
    response = requests.get(url)
    with io.open('vrste_projektov.json', 'wb+') as file:
        file.write(response.content)
    url = 'http://projektiweb.fri.uni-lj.si/api/partnerji'
    response = requests.get(url)
    with io.open('partnerji.json', 'wb+') as file:
        file.write(response.content)


with io.open('projekti.json', 'r', encoding='utf8') as projekti:
    data = json.load(projekti)
    referencePeople = {"Špela Arhar Holdt ", "Marko Bajec ", "Borut Batagelj ", "Katarina Bebar ", "Miha Bejek ",
                 "Aljoša Besednjak ", "Jasna Bevk ", "Janez Bindas ", "Neli Blagus ", "Marko Boben ", "Ciril Bohak ",
                 "Alenka Bone ", "Zoran Bosnić ", "Narvika Bovcon ", "Borja Bovcon ", "Ivan Bratko ", "Andrej Brodnik ",
                 "Patricio Bulić ", "Mojca Ciglarič ", "Jaka Cijan ", "Zala Cimperman ", "Tomaž Curk ", "Jernej Cvek ",
                 "Luka Čehovin Zajc ", "Rok Češnovar ", "Jaka Čibej ", "Uroš Čibej ", "Andrej Čopar ", "Janez Demšar ",
                 "Saša Divjak ", "Andrej Dobnikar ", "Tomaž Dobravec ", "Matej Dobrevski ", "Roman Dorn ",
                 "Miha Drole ", "Žiga Emeršič ", "Aleš Erjavec ", "Jana Faganeli Pucer ", "Gašper Fele Žorž ",
                 "Gašper Fijavž ", "Aleksandra Franc ", "Damir Franetič ", "Luka Fürst ", "Peter Gabrovšek ",
                 "Anton Zvonko Gazvoda ", "Sandi Gec ", "Dejan Georgiev ", "Primož Godec ", "Teja Goli ",
                 "Rok Gomišček ", "Vesna Gračner ", "Miha Grohar ", "Vida Groznik ", "Matej Guid ", "Veselko Guštin ",
                 "dr. Marjana Harcet ", "Bojan Heric ", "Ana Herzog ", "Tomaž Hočevar ", "Alen Horvat ",
                 "Tomaž Hovelja ", "Aleks Huč ", "Nejc Ilc ", "Franc Jager ", "Aleš Jaklič ", "Martin Jakomin ",
                 "Miha Janež ", "Marko Janković ", "David Jelenc ", "Peter Jenko ", "Gregor Jerše ",
                 "Matjaž Branko Jurič ", "Aleksandar Jurišić ", "Maher Kaddoura ", "Benjamin Kastelic ",
                 "Alenka Kavčič ", "Silvana Kavčič ", "Maja Kerkez ", "Peter Marijan Kink ", "Bojan Klemenc ",
                 "Jelena Klisara ", "Vid Klopčič ", "Petar Kochovski ", "Dušan Kodek ", "Igor Kononenko ",
                 "Miran Koprivec ", "Domen Košir ", "Jan Kralj ", "Marjan Krisper ", "Matej Kristan ", "Matjaž Kukar ",
                 "Dejan Lavbič ", "Timotej Lazar ", "Iztok Lebar Bajec ", "Aleš Leonardis ", "Žiga Lesar ",
                 "Jure Leskovec ", "Matjaž Ličen ", "Jaka Lindič ", "Nikola Ljubešić ", "Sonja Lojk ", "Jure Lokovšek ",
                 "Uroš Lotrič ", "Alan Lukežič ", "Nives Macerl ", "Viljan Mahnič ", "Ivan Majhen ", "Matija Marolt ",
                 "Teodora Matić ", "Blaž Meden ", "Jan Meznarič ", "Miran Mihelčič ", "Jurij Mihelič ", "Iztok Mihevc ",
                 "David Modic ", "Miha Moškon ", "Martin Možina ", "Nežka Mramor Kosta ", "Miha Mraz ",
                 "Jon Natanael Muhovič ", "Miha Nagelj ", "Polona Oblak ", "Tanja Oblak Črnič ", "Amra Omanović ",
                 "Bojan Orel ", "Radko Osredkar ", "Matjaž Pančur ", "Jan Pavlin ", "Peter Peer ", "Veljko Pejović ",
                 "Darja Peljhan ", "Matevž Pesek ", "Irena Pestotnik ", "Zvonimir Petkovšek ", "Matej Pičulin ",
                 "Ratko Pilipović ", "Ljubo Pipan ", "Žiga Pirnar ", "Gregor Pirš ", "Matevž Pogačnik ", "Rok Povšič ",
                 "Marko Poženel ", "Ajda Pretnar ", "Matej Prijatelj ", "Žiga Pušnik ", "Martin Raič ",
                 "Vladislav Rajkovič ", "Jan Ravnik ", "Mateja Ravnik ", "Andreja Retelj ", "Matija Rezar ",
                 "Anže Rezelj ", "Borut Robič ", "Marko Robnik Šikonja ", "Igor Rožanc ", "Robert Rozman ",
                 "Ksenija Rozman ", "Taja Runovc ", "Rok Rupnik ", "Aleksander Sadikov ", "Miha Schaffer ",
                 "Petra Simonič ", "Danijel Skočaj ", "Boštjan Slivnik ", "Davor Sluga ", "Tim Smole ",
                 "Aleš Smonig Grnjak ", "Aleš Smrdel ", "Franc Solina ", "Blaž Sovdat ", "Martin Stražar ",
                 "Luka Šajn ", "Luka Šarc ", "Gregor Šega ", "Andrej Šeruga ", "Igor Škraba ", "Aleš Špetič ",
                 "Branko Šter ", "Marina Štros-Bračko ", "Erik Štrumbelj ", "Lovro Šubelj ", "Domen Tabernik ",
                 "Vesna Tanko ", "Marko Toplak ", "Barbara Torkar ", "Denis Trček ", "Mira Trebar ", "Jure Tuta ",
                 "Matej Ulčar ", "Damjan Vavpotič ", "Luka Vavtar ", "Zdenka Velikonja ", "Dejan Velušček ",
                 "Dejan Verčič ", "Janoš Vidali ", "Tone Vidmar ", "Boštjan Vilfan ", "Mojca Vilfan ", "Zvonko Virant ",
                 "Žiga Virk ", "Matej Vitek ", "Petar Vračar ", "Simon Vrhovec ", "Martin Vuk ", "Aleš Watzak ",
                 "Aljaž Zalar ", "Nikolaj Zimic ", "Aljaž Zrnec ", "Helena Marija Zupan ", "Blaž Zupan ",
                 "Jure Žabkar ", "Lan Žagar ", "Manca Žerovnik Mekuč ", "Rok Žitko ", "Marinka Žitnik ",
                 "Slavko Žitnik ", "Urška Žnidarič"}

    referenceLabs = {
        "biolab", "lalg", "laps", "laspp", "lbrso", "lem", "lgm", "li", "liis", "lkm", "lkrv", "lmmri", "lpt", "lrk",
        "lrss", "lrv", "ltpo", "lui", "lusy", "luvss"
    }

    idList = match_id(data['projects'], referencePeople)
    reference = match_lab(referenceLabs, idList)
    json_to_md(data['projects'], reference)





