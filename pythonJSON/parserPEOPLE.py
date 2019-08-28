import json
import frontmatter
import io
from os import path
from shutil import copyfile


def compare_names(name1, name2):
    split1 = name2.split()
    split = name1.split()
    fixed_name1 = ""
    fixed_name2 = ""
    for a in split:
        if a[-1] != '.':
            fixed_name1 += ' ' + a
    for a in split1:
        if a[-1] != '.':
            fixed_name2 += ' ' + a
    return fixed_name1.replace(" ", "").lower() == fixed_name2.replace(" ", "").lower()


''' def json_to_md(loaded_json):

    for p in loaded_json:
        fname = './content/sl/osebje/' + p['abbreviation'].lower() + '.md'
        fname_en = './content/en/osebje/' + p['abbreviation'].lower() + '.md'

        if not path.isfile(fname):
            copyfile('./sampleJSON/template_lab.md', fname)
        if not path.isfile(fname_en):
            copyfile('./sampleJSON/template_lab.md', fname_en)

        with io.open(fname, 'r', encoding='utf8') as f, io.open(fname_en, 'r', encoding='utf8') as f_en:

            # Parse file's front matter
            post = frontmatter.load(f, encoding='utf-8')
            post_en = frontmatter.load(f_en, encoding='utf-8')

            if post.get('abbreviation') is None and p['abbreviation'] is not None:
                post['abbreviation'] = p['abbreviation']
                post_en['abbreviation'] = post['abbreviation']

            if post.get('title') is None and p['title'] is not None:
                post['title'] = p['title']['sl']
                post_en['title'] = p['title']['en']

            if post.get('location') is None and p['location'] is not None:
                post['location'] = p['location']
                post_en['location'] = post['location']

            if post.get('body') is None and p['description'] is not None:
                post.content = p['description']['sl']
                post_en.content = p['description']['en']

            if post.get('id') is None and 'id' in p:
                post['id'] = p['id']
                post_en['id'] = p['id']

            # Save the file
            new = io.open(fname, 'wb')
            new_en = io.open(fname_en, 'wb')
            frontmatter.dump(post_en, new_en)
            frontmatter.dump(post, new)
            new.close()
            new_en.close()

        if 'members' in p:
            jname = './data/' + str(p['abbreviation']).lower() + '_mem.json'

            with io.open(jname, 'w+', encoding='utf8') as to:
                from_insert = p['members']
                json.dump(from_insert, to)
'''

with io.open('./sampleJSON/persons.json', 'r', encoding='utf8') as json_persons, \
        io.open('./sampleJSON/staffDescriptions.json', 'r', encoding='utf8') as desc_persons:
    data = json.load(json_persons)
    desc = json.load(desc_persons)

    arrPersons = []
    arrDesc = []
    reference = {"Špela Arhar Holdt ","Marko Bajec ","Borut Batagelj ","Katarina Bebar ","Miha Bejek ","Aljoša Besednjak ","Jasna Bevk ","Janez Bindas ","Neli Blagus ","Marko Boben ","Ciril Bohak ","Alenka Bone ","Zoran Bosnić ","Narvika Bovcon ","Borja Bovcon ","Ivan Bratko ","Andrej Brodnik ","Patricio Bulić ","Mojca Ciglarič ","Jaka Cijan ","Zala Cimperman ","Tomaž Curk ","Jernej Cvek ","Luka Čehovin Zajc ","Rok Češnovar ","Jaka Čibej ","Uroš Čibej ","Andrej Čopar ","Janez Demšar ","Saša Divjak ","Andrej Dobnikar ","Tomaž Dobravec ","Matej Dobrevski ","Roman Dorn ","Miha Drole ","Žiga Emeršič ","Aleš Erjavec ","Jana Faganeli Pucer ","Gašper Fele Žorž ","Gašper Fijavž ","Aleksandra Franc ","Damir Franetič ","Luka Fürst ","Peter Gabrovšek ","Anton Zvonko Gazvoda ","Sandi Gec ","Dejan Georgiev ","Primož Godec ","Teja Goli ","Rok Gomišček ","Vesna Gračner ","Miha Grohar ","Vida Groznik ","Matej Guid ","Veselko Guštin ","dr. Marjana Harcet ","Bojan Heric ","Ana Herzog ","Tomaž Hočevar ","Alen Horvat ","Tomaž Hovelja ","Aleks Huč ","Nejc Ilc ","Franc Jager ","Aleš Jaklič ","Martin Jakomin ","Miha Janež ","Marko Janković ","David Jelenc ","Peter Jenko ","Gregor Jerše ","Matjaž Branko Jurič ","Aleksandar Jurišić ","Maher Kaddoura ","Benjamin Kastelic ","Alenka Kavčič ","Silvana Kavčič ","Maja Kerkez ","Peter Marijan Kink ","Bojan Klemenc ","Jelena Klisara ","Vid Klopčič ","Petar Kochovski ","Dušan Kodek ","Igor Kononenko ","Miran Koprivec ","Domen Košir ","Jan Kralj ","Marjan Krisper ","Matej Kristan ","Matjaž Kukar ","Dejan Lavbič ","Timotej Lazar ","Iztok Lebar Bajec ","Aleš Leonardis ","Žiga Lesar ","Jure Leskovec ","Matjaž Ličen ","Jaka Lindič ","Nikola Ljubešić ","Sonja Lojk ","Jure Lokovšek ","Uroš Lotrič ","Alan Lukežič ","Nives Macerl ","Viljan Mahnič ","Ivan Majhen ","Matija Marolt ","Teodora Matić ","Blaž Meden ","Jan Meznarič ","Miran Mihelčič ","Jurij Mihelič ","Iztok Mihevc ","David Modic ","Miha Moškon ","Martin Možina ","Nežka Mramor Kosta ","Miha Mraz ","Jon Natanael Muhovič ","Miha Nagelj ","Polona Oblak ","Tanja Oblak Črnič ","Amra Omanović ","Bojan Orel ","Radko Osredkar ","Matjaž Pančur ","Jan Pavlin ","Peter Peer ","Veljko Pejović ","Darja Peljhan ","Matevž Pesek ","Irena Pestotnik ","Zvonimir Petkovšek ","Matej Pičulin ","Ratko Pilipović ","Ljubo Pipan ","Žiga Pirnar ","Gregor Pirš ","Matevž Pogačnik ","Rok Povšič ","Marko Poženel ","Ajda Pretnar ","Matej Prijatelj ","Žiga Pušnik ","Martin Raič ","Vladislav Rajkovič ","Jan Ravnik ","Mateja Ravnik ","Andreja Retelj ","Matija Rezar ","Anže Rezelj ","Borut Robič ","Marko Robnik Šikonja ","Igor Rožanc ","Robert Rozman ","Ksenija Rozman ","Taja Runovc ","Rok Rupnik ","Aleksander Sadikov ","Miha Schaffer ","Petra Simonič ","Danijel Skočaj ","Boštjan Slivnik ","Davor Sluga ","Tim Smole ","Aleš Smonig Grnjak ","Aleš Smrdel ","Franc Solina ","Blaž Sovdat ","Martin Stražar ","Luka Šajn ","Luka Šarc ","Gregor Šega ","Andrej Šeruga ","Igor Škraba ","Aleš Špetič ","Branko Šter ","Marina Štros-Bračko ","Erik Štrumbelj ","Lovro Šubelj ","Domen Tabernik ","Vesna Tanko ","Marko Toplak ","Barbara Torkar ","Denis Trček ","Mira Trebar ","Jure Tuta ","Matej Ulčar ","Damjan Vavpotič ","Luka Vavtar ","Zdenka Velikonja ","Dejan Velušček ","Dejan Verčič ","Janoš Vidali ","Tone Vidmar ","Boštjan Vilfan ","Mojca Vilfan ","Zvonko Virant ","Žiga Virk ","Matej Vitek ","Petar Vračar ","Simon Vrhovec ","Martin Vuk ","Aleš Watzak ","Aljaž Zalar ","Nikolaj Zimic ","Aljaž Zrnec ","Helena Marija Zupan ","Blaž Zupan ","Jure Žabkar ","Lan Žagar ","Manca Žerovnik Mekuč ","Rok Žitko ","Marinka Žitnik ","Slavko Žitnik ","Urška Žnidarič"}
    i = 0
    fixed_indexes = []
    for p in data['persons']:
        arrPersons.append(p['fullname_and_title']['sl'])
        i += 1
    k = 0
    for p in desc:
        arrDesc.append(p['name'])
        k += 1

    print(str(len(arrPersons))+' '+str(len(arrDesc)))

    same = 0
    for a in arrDesc:
        exist = 0
        index = 0
        for p in arrPersons:
            if compare_names(p, a):
                same += 1
                exist = 1
                fixed_indexes.append(index)
                break
            index += 1
        if exist == 0:
            print(a)
    print(str(len(fixed_indexes)))

