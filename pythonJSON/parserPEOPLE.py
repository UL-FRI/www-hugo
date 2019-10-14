import json
import frontmatter
import re
import io
from os import path
from shutil import copyfile


def compare_names(name1, name2):
    split1 = name2.split()
    split2 = name1.split()
    fixed_name1 = ""
    fixed_name2 = ""

    for a in split2:
        if a[-1] != '.':
            fixed_name1 += ' ' + a
    for a in split1:
        if a[-1] != '.':
            fixed_name2 += ' ' + a

    if fixed_name1.replace(" ","").lower() == fixed_name2.replace(" ", "").lower():
        fname = re.sub(r'\s+', '_', fixed_name1.lstrip(' ').lower())
        fname_sl = './content/sl/osebje/' + fname + '.md'
        fname_en = './content/en/osebje/' + fname + '.md'

        if not path.isfile(fname_sl):
            copyfile('./structJSON/template_personal.md', fname_sl)
        if not path.isfile(fname_en):
            copyfile('./structJSON/template_personal.md', fname_en)

        return True
    else:
        return False


def json_to_md(persons, staff_desc, indexes, names):

    desc_ind = 0

    for (m, b) in zip(indexes, names):

        # persons[a] is same person as c
        if m != -1:
            fix_name = re.sub(r'\s+', '_', b.lstrip(' ').lower())
            fname_sl = './content/sl/osebje/' + fix_name + '.md'
            fname_en = './content/en/osebje/' + fix_name + '.md'

            with io.open(fname_sl, 'r', encoding='utf8') as f, io.open(fname_en, 'r', encoding='utf8') as f_en:
                person_json = persons[m]
                desc_json = staff_desc[desc_ind]

                # Open file's frontmatter
                post_md_sl = frontmatter.load(f, encoding='utf8')
                post_md_en = frontmatter.load(f_en, encoding='utf8')

                if post_md_sl.get('fixName') is '':
                    post_md_sl['fixName'] = fix_name
                if post_md_sl.get('profName') is '' and person_json['fullname_and_title'] is not None:
                    post_md_sl['profName'] = person_json['fullname_and_title']['sl']
                if post_md_sl.get('SICRIS') is '' and person_json['sicris_researcher_number'] is not None:
                    post_md_sl['SICRIS'] = person_json['sicris_researcher_number']
                if post_md_sl.get('profTitle') is '' and person_json['web_category'] is not None:
                    post_md_sl['profTitle'] = person_json['web_category']['sl']
                if post_md_sl.get('telephoneInfo') is '' and person_json['phone'] is not None:
                    post_md_sl['telephoneInfo'] = person_json['phone']
                if post_md_sl.get('mailInfo') is '' and person_json['email'] is not None:
                    post_md_sl['mailInfo'] = person_json['email']
                if post_md_sl.get('officeHours') is '' and person_json['office_hours'] is not None:
                    post_md_sl['officeHours'] = person_json['office_hours']['sl']
                if post_md_sl.get('location') is '' and person_json['location'] is not None:
                    post_md_sl['location'] = person_json['location']
                if post_md_sl.get('body') is '' and desc_json['descSl'] is not None:
                    post_md_sl.content = desc_json['descSl']

                if post_md_en.get('fixName') is '':
                    post_md_en['fixName'] = fix_name
                if post_md_en.get('profName') is '' and person_json['fullname_and_title'] is not None:
                    post_md_en['profName'] = person_json['fullname_and_title']['en']
                if post_md_en.get('SICRIS') is '' and person_json['sicris_researcher_number'] is not None:
                    post_md_en['SICRIS'] = person_json['sicris_researcher_number']
                if post_md_en.get('profTitle') is '' and person_json['web_category'] is not None:
                    post_md_en['profTitle'] = person_json['web_category']['en']
                if post_md_en.get('telephoneInfo') is '' and person_json['phone'] is not None:
                    post_md_en['telephoneInfo'] = person_json['phone']
                if post_md_en.get('mailInfo') is '' and person_json['email'] is not None:
                    post_md_en['mailInfo'] = person_json['email']
                if post_md_en.get('officeHours') is '' and person_json['office_hours'] is not None:
                    post_md_en['officeHours'] = person_json['office_hours']['en']
                if post_md_en.get('location') is '' and person_json['location'] is not None:
                    post_md_en['location'] = person_json['location']
                if post_md_en.get('body') is '' and desc_json['descEn'] is not None:
                    post_md_en.content = desc_json['descEn']

                if len(person_json['labs']) != 0:
                    for lab in person_json['labs']:
                        post_md_sl['lab'] = lab['title']['sl']
                        post_md_en['lab'] = lab['title']['en']
                        post_md_sl['labPos'] = lab['function_in_lab']['sl']
                        post_md_en['labPos'] = lab['function_in_lab']['en']

                if 'subjects' in person_json:
                    course_codes = []
                    for subject in person_json['subjects']:
                        if 'course_code' in subject:
                            course_codes.append(subject['course_code'])
                    sname = './data/osebje/subjects_and_img/' + fix_name + '_sub_img.json'

                    with io.open(sname, 'w+', encoding='utf8') as to:
                        from_insert = {
                            "subjects": course_codes,
                            "img": person_json['picture']
                        }
                        json.dump(from_insert, to)

            # Save the file
            new = io.open(fname_sl, 'wb')
            new_en = io.open(fname_en, 'wb')
            frontmatter.dump(post_md_en, new_en)
            frontmatter.dump(post_md_sl, new)
            new.close()
            new_en.close()
        desc_ind += 1


with io.open('./sampleJSON/persons.json', 'r', encoding='utf8') as json_persons, \
        io.open('./sampleJSON/staffDescriptions.json', 'r', encoding='utf8') as desc_persons:
    data = json.load(json_persons)
    desc = json.load(desc_persons)

    arrPersons = []
    arrDesc = []
    reference = {"Špela Arhar Holdt ", "Marko Bajec ", "Borut Batagelj ", "Katarina Bebar ", "Miha Bejek ",
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
    i = 0
    fixed_indexes = []
    for p in data['persons']:
        arrPersons.append(p['fullname_and_title']['sl'])
        i += 1
    k = 0
    for p in desc:
        split = str(p['name']).split()
        name = ""
        for a in split:
            if a[-1] != '.':
                name += ' ' + a
        arrDesc.append(name)
        k += 1

    print(str(len(arrPersons)) + ' ' + str(len(arrDesc)))
    for a in arrDesc:
        index = 0
        exist = 0
        for p in arrPersons:
            if compare_names(p, a):
                exist = 1
                fixed_indexes.append(index)
                break
            index += 1

        if exist == 0:
            fixed_indexes.append(-1)

    json_to_md(data['persons'], desc, fixed_indexes, arrDesc)


