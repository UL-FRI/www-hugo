import json
import io
import os
import sys

import frontmatter
import requests
from datetime import datetime


def get_file_name(string):
    string = string.lstrip(' ').lower()
    split = string.split(' ')
    if len(split) == 2:
        filename = str(split[1]) + "_" + str(split[0])
    else:
        filename = str(split[2]) + "_" + str(split[1]) + "_" + str(split[0])

    c1 = 'č'.encode()
    c2 = 'ć'.encode()
    z = 'ž'.encode()
    s = 'š'.encode()
    dz = 'đ'.encode()
    umlaut = 'ü'.encode()

    string = filename.encode()
    string = string.replace(c1, b'c')
    string = string.replace(c2, b'c')
    string = string.replace(z, b'z')
    string = string.replace(s, b's')
    string = string.replace(dz, b'dz')
    string = string.replace(umlaut, b'u')
    string = string.decode('utf-8')

    return string


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
            if fullname.rstrip(" ") == ref.rstrip():
                fname = get_file_name(fullname.rstrip(' '))
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
        fname = './data/laboratorij/members/' + a + '.json'
        if os.path.isfile(fname):
            with io.open(fname, 'r', encoding='utf8') as labs:
                load = json.load(labs)
                for mem in load:
                    for person in ref_people:
                        mem_fname = get_file_name(mem['name']+' '+mem['surname'])
                        if mem_fname == person['fullname']:
                            complete_ref.append(
                                {
                                    "id": person['id'],
                                    "fullname": person['fullname'],
                                    "lab": a
                                }
                            )
                            person['fullname'] = 'blank'

    return complete_ref


def save_id_to_md_personal(id, filename):
    en = './content/en/osebje/' + filename + '/index.md'
    sl = './content/sl/osebje/' + filename + '/index.md'

    with io.open(en, 'r', encoding='utf8') as md_en, io.open(sl, 'r', encoding='utf8') as md_sl:

        post_en = frontmatter.load(md_en, encoding='utf8')
        post_sl = frontmatter.load(md_sl, encoding='utf8')

        if id not in post_en['projects']:
            post_en['projects'].append(id)
        if id not in post_sl['projects']:
            post_sl['projects'].append(id)


        # Save the file
        new = io.open(sl, 'wb')
        new_en = io.open(en, 'wb')
        frontmatter.dump(post_en, new_en)
        frontmatter.dump(post_sl, new)
        new.close()
        new_en.close()


def save_id_to_md_lab(id, filename):
    en = './content/en/laboratorij/' + filename + '/index.md'
    sl = './content/sl/laboratorij/' + filename + '/index.md'
    with io.open(en, 'r', encoding='utf8') as md_en, io.open(sl, 'r', encoding='utf8') as md_sl:

        post_en = frontmatter.load(md_en, encoding='utf8')
        post_sl = frontmatter.load(md_sl, encoding='utf8')

        if id not in post_en['projects']:
            post_en['projects'].append(id)

        if id not in post_sl['projects']:
            post_sl['projects'].append(id)


        # Save the file
        new = io.open(sl, 'wb')
        new_en = io.open(en, 'wb')
        frontmatter.dump(post_en, new_en)
        frontmatter.dump(post_sl, new)
        new.close()
        new_en.close()


def check_if_project_exist(proj_id, fname):
    if os.path.isfile(fname) and os.stat(fname).st_size != 0:
        with io.open(fname, 'r', encoding='utf8') as ref:
            ref_lab = json.load(ref)
            for i in ref_lab:
                if i['id'] == proj_id:
                    return True
            return False
    else:
        return False


def format_project(p):
    struct = {
        "id": p["id"],
        "title":
            {
                "si": p['si']['title'],
                "en": p['en']['title']
            },
        "ref_project_type": p['si']['ref_project_type'],
        "url": get_project_url(p),
        "start_date": p['si']['start_date'],
        "end_date": p['si']['end_date']
    }
    return struct


def get_project_url(p):
    with io.open('./sampleJSON/projects.json', 'r', encoding='utf8') as reference_projects:
        load = json.load(reference_projects)
        for i in load:
            if str(p['id']) == i['project_id']:
                return i['url']
    return ''


def get_folder_name(p):
    for name in os.listdir('./content/sl/osebje/'):
        if compare_names(name, p):
            return name


def compare_names(folderName, name):
    folderSplit = folderName.split('-')
    split = name.split('_')

    if set(split).issubset(set(folderSplit)):
        print(split)
        return True
    else:
        return False


def append_json(file, p):
    if os.path.isfile(file):
        with io.open(file, 'r', encoding='utf8') as to:
            project_json = json.load(to)
            temp_list = []
            for obj in project_json:
                temp_list.append(obj)
            temp_list.append(format_project(p))
            project_json = temp_list
            with io.open(file, 'w', encoding='utf8') as target:
                target.write(json.dumps(project_json, indent=4, sort_keys=True))
    else:
        with io.open(file, 'w', encoding='utf8') as to:
            arr = [format_project(p)]
            json.dump(arr, to)


def json_to_md(data_json, ref_ids):
    for p in data_json:
        for x in p['si']['persons']:
            for ref in ref_ids:
                if x['id'] == ref['id']:
                    datetime_str = p['si']['end_date']
                    fname = './data/osebje/projects/' + ref['fullname'] + '.json'
                    fname_lab = './data/laboratorij/projects/' + ref['lab'] + '.json'

                    if not check_if_project_exist(p['id'], fname_lab):
                        append_json(fname_lab, p)
                    save_id_to_md_lab(p['id'], ref['lab'])

                    personFolder = get_folder_name(ref['fullname'])
                    if personFolder is None:
                        print(ref['fullname'])

                    if os.path.isfile('./content/en/osebje/' + personFolder + '/index.md'):
                        append_json(fname, p)
                        save_id_to_md_personal(p['id'], personFolder)


def get_xml():
    url = 'http://projektiweb.fri.uni-lj.si/api/projekti'
    response = requests.get(url)
    with io.open('./sampleJSON/projekti.json', 'wb+') as file:
        file.write(response.content)
    url = 'http://projektiweb.fri.uni-lj.si/api/vrsteprojektov'
    response = requests.get(url)
    with io.open('./sampleJSON/vrste_projektov.json', 'wb+') as file:
        file.write(response.content)
    url = 'http://projektiweb.fri.uni-lj.si/api/partnerji'
    response = requests.get(url)
    with io.open('./sampleJSON/partnerji.json', 'wb+') as file:
        file.write(response.content)


# get_xml() # -- Uncomment to get xml files from projektiweb.fri.uni-lj.si

with io.open('./sampleJSON/projekti.json', 'r', encoding='utf8') as projekti:
    data = json.load(projekti)
    referencePeople = ["Špela Arhar Holdt", "Nina Arko Krmelj", "Marko Bajec", "Borut Batagelj", "Andrej Bauer",
     "Miha Bejek", "Aljoša Besednjak", "Jasna Bevk", "Marko Boben", "Ciril Bohak", "Alenka Bone", "Tadej Borovšak",
     "Zoran Bosnić", "Borja Bovcon", "Narvika Bovcon", "Tea Brašanac", "Ivan Bratko", "Janez Brežnik", "Andrej Brodnik",
     "Patricio Bulić", "Mojca Ciglarič", "Zala Cimperman", "Tomaž Curk", "Jernej Cvek", "Luka Čehovin Zajc",
     "Rok Češnovar",
     "Jaka Čibej", "Uroš Čibej", "Janez Demšar", "Jure Demšar", "Tomaž Dobravec", "Matej Dobrevski", "Rebeka Drnovšek",
     "Žiga Emeršič", "Aleš Erjavec", "Jana Faganeli Pucer", "Gašper Fele Žorž", "Gašper Fijavž", "Marko Firm",
     "Aleksandra Franc","Damir Franetič","Damjan Fujs","Luka Fürst","Niko Gamulin","Fatime Gashi","Anton Zvonko Gazvoda", "Sandi Gec",
     "Dejan Georgiev", "Martin Gjoreski", "Primož Godec", "Teja Goli", "Rok Gomišček", "Vesna Gračner",
     "Miha Grohar", "Vida Groznik", "Matej Guid", "Marjana Harcet", "Bojan Heric", "Ana Herzog", "Tomaž Hočevar",
     "Suzana Hostnik", "Tomaž Hovelja", "Aleks Huč", "Nejc Ilc", "Franc Jager", "Aleš Jaklič", "Miha Janež",
     "Marko Janković", "Amol Arjun Jawale", "David Jelenc", "Peter Jenko", "Gregor Jerše", "Matjaž Branko Jurič",
     "Aleksandar Jurišić", "Maher Kaddoura", "Benjamin Kastelic", "Alenka Kavčič", "Silvana Kavčič", "Maja Kerkez",
     "Borut Paul Kerševan", "Peter Marijan Kink", "Klemen Klanjšček", "Bojan Klemenc", "Jelena Klisara", "Vid Klopčič",
     "Petar Kochovski", "Enja Kokalj", "Igor Kononenko", "Miran Koprivec", "Domen Košir", "Simon Krek", "Matej Kristan",
     "Matjaž Kukar", "Leon Lampret", "Iztok Lapanja", "Dejan Lavbič", "Iztok Lebar Bajec", "Aleš Leonardis",
     "Žiga Lesar",
     "Jure Leskovec", "Nikola Ljubešić", "Sonja Lojk", "Jure Lokovšek", "Uroš Lotrič", "Alan Lukežič", "Nives Macerl",
     "Octavian-Mihai Machidon", "Lidija Magdevska", "Matija Marolt", "Teodora Matić", "Blaž Meden", "Jan Meznarič",
     "Jurij Mihelič", "Iztok Mihevc", "Kristian Miok", "David Modic", "Miha Moškon", "Martin Možina",
     "Nežka Mramor Kosta",
     "Miha Mraz", "Jon Muhovič", "Miha Nagelj", "Mimoza Naseka", "Jakob Novak", "Polona Oblak", "Amra Omanović",
     "Bojan Orel", "Matjaž Pančur", "Aleš Papič", "Uroš Paščinski", "Peter Peer", "Veljko Pejović", "Špela Perner",
     "Matevž Pesek", "Irena Pestotnik", "Andrej Petelin", "Mattia Petroni", "Matej Pičulin", "Ratko Pilipović",
     "Žiga Pirnar", "Gregor Pirš", "Marko Poženel", "Ajda Pretnar", "Žiga Pušnik", "Mateja Ravnik", "Andreja Retelj",
     "Matija Rezar", "Mitja Rizvič", "Borut Robič", "Marko Robnik Šikonja", "Peter Rot", "Igor Rožanc",
     "Ksenija Rozman",
     "Robert Rozman", "Taja Runovc", "Rok Rupnik", "Aleksander Sadikov", "Miha Schaffer", "Petra Simonič",
     "Arne Simonič",
     "Danijel Skočaj", "Boštjan Slivnik", "Davor Sluga", "Tim Smole", "Aleš Smonig Grnjak", "Aleš Smrdel",
     "Franc Solina",
     "Vlado Stankovski", "Luka Šajn", "Luka Šarc", "Andrej Šeruga", "Jaka Šircelj", "Blaž Škrlj", "Domen Šoberl",
     "Branko Šter", "Erik Štrumbelj", "Lovro Šubelj", "Domen Tabernik", "Vesna Tanko", "Marko Toplak", "Barbara Torkar",
     "Denis Trček", "Mira Trebar", "Jure Tuta", "Matej Ulčar", "Anita Valmarska", "Damjan Vavpotič", "Zdenka Velikonja",
     "Kristina Veljković", "Janoš Vidali", "Žiga Virk", "Matej Vitek", "Jaka Vodeb", "Petar Vračar", "Simon Vrhovec",
     "Martin Vuk", "Aleš Watzak", "Aljaž Zalar", "Vitjan Zavrtanik", "Nikolaj Zimic", "Aljaž Zrnec",
     "Helena Marija Zupan",
     "Blaž Zupan", "Jure Žabkar", "Aleš Žagar", "Lan Žagar", "Manca Žerovnik Mekuč", "Rok Žitko", "Slavko Žitnik",
     "Urška Žnidarič", "Bojan Žunkovič"]

    referenceLabs = {
        "biolab", "la", "laps", "laspp", "lbrso", "lem", "lgm", "li", "liis", "lkm", "lkrv", "lmmri", "lpt", "lrk",
        "lrss", "lrv", "ltpo", "lui", "lusy", "luvss"
    }
    idList = match_id(data['projects'], referencePeople)
    print(idList)
    reference = match_lab(referenceLabs, idList)
    print(reference)
    json_to_md(data['projects'], reference)



