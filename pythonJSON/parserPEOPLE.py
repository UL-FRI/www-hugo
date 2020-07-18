import json
import frontmatter
import os
from PIL import Image
import io
from os import path
from shutil import copyfile
import base64

lab_shorts = {
    "biolab":"bioinformatiko",
    "la":"algoritmiko",
    "laps":"arhitekturo in procesiranje signalov",
    "laspp":"adaptivne sisteme in paralelno procesiranje",
    "lbrso":"biomedicinske računalniške sisteme in oslikave",
    "lem":"e-medije",
    "lgm":"računalniško grafiko in multimedije",
    "li":"informatiko",
    "liis":"integracijo informacijskih sistemov",
    "lkm":"kognitivno modeliranje",
    "lkrv":"kriptografijo in računalniško varnost",
    "lmmri":"matematične metode v računalništvu in informatiki",
    "lpt":"podatkovne tehnologije",
    "lrk":"računalniške komunikacije",
    "lrss":"računalniške strukture in sisteme",
    "lrv":"računalniški vid",
    "ltpo":"tehnologijo programske opreme",
    "lui":"umetno inteligenco",
    "lusy":"vseprisotne sisteme",
    "luvss":"umetne vizualne spoznavne sisteme"
}

def compare_names(name1, name2):
    split1 = name2.split()
    split2 = name1.split()
    fixed_name1 = ""
    fixed_name2 = ""

    for a in split2:
        if a[-1] != '.':
            fixed_name1 += a
    for a in split1:
        if a[-1] != '.':
            fixed_name2 += a

    if fixed_name1.replace(" ","") == fixed_name2.replace(" ",""):
        return True
    else:
        return False


def createFolderAndMarkdown(fname):
    folderName_sl = './content/sl/osebje/' + fname
    folderName_en = './content/en/osebje/' + fname

    fname_sl = folderName_sl + '/index.md'
    fname_en = folderName_en + '/index.md'

    if not path.isfile(fname_sl):
        try:
            os.mkdir(folderName_sl)
        except OSError:
            print("Creation of the directory %s failed" % folderName_sl)
        else:
            print("Successfully created the directory %s " % folderName_sl)

        copyfile('./structJSON/template_personal.md', fname_sl)

    if not path.isfile(fname_en):
        try:
            os.mkdir(folderName_en)
        except OSError:
            print("Creation of the directory %s failed" % folderName_en)
        else:
            print("Successfully created the directory %s " % folderName_en)

        copyfile('./structJSON/template_personal.md', fname_en)


def get_lab_url(title):
    for key in lab_shorts:
        if lab_shorts[key].lower() in title.lower():
            return key

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

    string = filename.encode()
    string = string.replace(c1, b'c')
    string = string.replace(c2, b'c')
    string = string.replace(z, b'z')
    string = string.replace(s, b's')
    string = string.replace(dz, b'dz')
    string = string.decode('utf-8')

    print(string)
    return string


def save_image(dirName, fileName, imgsrc):
    imgsrc = str(imgsrc)
    imgnameSl = './content/sl/osebje/' + dirName + '/photos/'
    imgnameEn = './content/en/osebje/' + dirName + '/photos/'

    try:
        os.mkdir(imgnameSl)
    except OSError:
        print("Creation of the directory %s failed" % imgnameSl)
    else:
        print("Successfully created the directory %s " % imgnameSl)

    try:
        os.mkdir(imgnameEn)
    except OSError:
        print("Creation of the directory %s failed" % imgnameEn)
    else:
        print("Successfully created the directory %s " % imgnameEn)

    imgsrc = imgsrc.replace("data:image/png;base64,", "")

    im = Image.open(io.BytesIO(base64.b64decode(imgsrc)))
    im.save(imgnameSl + fileName + '.jpeg', 'JPEG')
    im.save(imgnameEn + fileName + '.jpeg', 'JPEG')


def json_to_md(persons, personlinks, persons_link_indexes, names):

    link_ind = 0
    brezSlike = []

    for (m, b) in zip(persons_link_indexes, names):
        if m != -1:
            person_json = persons[m]
            link_json = personlinks[link_ind]
            fix_name = str(link_json['url_sl']).split('/')[-1]

            createFolderAndMarkdown(fix_name)

            fname_sl = './content/sl/osebje/' + fix_name + '/index.md'
            fname_en = './content/en/osebje/' + fix_name + '/index.md'
            with io.open(fname_sl, 'r', encoding='utf8') as f, io.open(fname_en, 'r', encoding='utf8') as f_en:
                # Open file's frontmatter
                post_md_sl = frontmatter.load(f, encoding='utf8')
                post_md_en = frontmatter.load(f_en, encoding='utf8')

                #Overwrite current data
                overwrite = 1

                if post_md_sl.get('fileName') is '' or overwrite:
                    post_md_sl['fileName'] = get_file_name(b)
                if post_md_sl.get('pageTitle') is '' or overwrite:
                    post_md_sl['pageTitle'] = b.lstrip(' ')
                if (post_md_sl.get('profName') is '' or overwrite) and person_json['fullname_and_title'] is not None:
                    post_md_sl['profName'] = person_json['fullname_and_title']['sl']
                if (post_md_sl.get('SICRIS') is '' or overwrite) and person_json['sicris_researcher_number'] is not None:
                    post_md_sl['SICRIS'] = person_json['sicris_researcher_number']
                if (post_md_sl.get('profTitle') is '' or overwrite) and person_json['web_category'] is not None:
                    post_md_sl['profTitle'] = person_json['web_category']['sl']
                if (post_md_sl.get('telephoneInfo') is '' or overwrite) and person_json['phone'] is not None:
                    post_md_sl['telephoneInfo'] = person_json['phone']
                if (post_md_sl.get('mailInfo') is '' or overwrite) and person_json['email'] is not None:
                    post_md_sl['mailInfo'] = person_json['email']
                if (post_md_sl.get('officeHours') is '' or overwrite) and person_json['office_hours']['sl'] is not None:
                    post_md_sl['officeHours'] = person_json['office_hours']['sl']
                if (post_md_sl.get('location') is '' or overwrite) and person_json['location'] is not None:
                    post_md_sl['location'] = person_json['location']

                if post_md_en.get('fileName') is '' or overwrite:
                    post_md_en['fileName'] = get_file_name(b)
                if post_md_en.get('pageTitle') is '' or overwrite:
                    post_md_en['pageTitle'] = b.lstrip(' ')
                if (post_md_en.get('profName') is '' or overwrite) and person_json['fullname_and_title'] is not None:
                    post_md_en['profName'] = person_json['fullname_and_title']['en']
                if (post_md_en.get('SICRIS') is '' or overwrite) and person_json['sicris_researcher_number'] is not None:
                    post_md_en['SICRIS'] = person_json['sicris_researcher_number']
                if (post_md_en.get('profTitle') is '' or overwrite) and person_json['web_category'] is not None:
                    post_md_en['profTitle'] = person_json['web_category']['en']
                if (post_md_en.get('telephoneInfo') is '' or overwrite) and person_json['phone'] is not None:
                    post_md_en['telephoneInfo'] = person_json['phone']
                if (post_md_en.get('mailInfo') is '' or overwrite) and person_json['email'] is not None:
                    post_md_en['mailInfo'] = person_json['email']
                if (post_md_en.get('officeHours') is '' or overwrite) and person_json['office_hours']['en'] is not None:
                    post_md_en['officeHours'] = person_json['office_hours']['en']
                if (post_md_en.get('location') is '' or overwrite) and person_json['location'] is not None:
                    post_md_en['location'] = person_json['location']

                if len(person_json['labs']) != 0:
                    for lab in person_json['labs']:
                        post_md_sl['lab'] = lab['title']['sl']
                        post_md_en['lab'] = lab['title']['en']
                        post_md_sl['labPos'] = lab['function_in_lab']['sl']
                        post_md_en['labPos'] = lab['function_in_lab']['en']
                        post_md_sl['labURL'] = get_lab_url(lab['title']['sl'])
                        post_md_en['labURL'] = get_lab_url(lab['title']['sl'])

                if 'subjects' in person_json:
                    course_codes = []
                    for subject in person_json['subjects']:
                        if 'course_code' in subject:
                            course_codes.append(subject['course_code'])

                    post_md_en['courses'] = course_codes
                    post_md_sl['courses'] = course_codes

                if person_json['picture'] is not None:
                    save_image(fix_name, get_file_name(b), person_json['picture'])

                    post_md_en['resources'] = [
                        {
                            "src": "photos/" + get_file_name(b) + '.jpeg',
                            "name": "Personal photo"
                        }
                    ]

                    post_md_sl['resources'] = [
                        {
                            "src": "photos/" + fix_name + '.jpeg',
                            "name": "Osebna fotografija"
                        }
                    ]
                else:
                    brezSlike.append(fix_name)

                post_md_en['slug'] = fix_name
                post_md_sl['slug'] = fix_name

            # Save the file
            new = io.open(fname_sl, 'wb')
            new_en = io.open(fname_en, 'wb')
            frontmatter.dump(post_md_en, new_en)
            frontmatter.dump(post_md_sl, new)
            new.close()
            new_en.close()
        link_ind += 1
    print(brezSlike)
    print(len(brezSlike))


with io.open('./sampleJSON/employees.json', 'r', encoding='utf8') as json_persons, \
        io.open('./sampleJSON/employees-links.json', 'r', encoding='utf8') as link_persons:
    data = json.load(json_persons)
    links = json.load(link_persons)

    arrPersons = []
    arrLinks = []
    '''reference = ["Špela Arhar Holdt","Nina Arko Krmelj","Marko Bajec","Borut Batagelj","Andrej Bauer",
    "Miha Bejek","Aljoša Besednjak","Jasna Bevk","Marko Boben","Ciril Bohak","Alenka Bone","Tadej Borovšak",
    "Zoran Bosnić","Borja Bovcon","Narvika Bovcon","Tea Brašanac","Ivan Bratko","Janez Brežnik","Andrej Brodnik",
    "Patricio Bulić","Mojca Ciglarič","Zala Cimperman","Tomaž Curk","Jernej Cvek","Luka Čehovin Zajc","Rok Češnovar",
    "Jaka Čibej","Uroš Čibej","Janez Demšar","Jure Demšar","Tomaž Dobravec","Matej Dobrevski","Rebeka Drnovšek",
    "Žiga Emeršič","Aleš Erjavec","Jana Faganeli Pucer","Gašper Fele Žorž","Gašper Fijavž","Marko Firm","Aleksandra 
    Franc","Damir Franetič","Damjan Fujs","Luka Fürst","Niko Gamulin","Fatime Gashi","Anton Zvonko Gazvoda",
    "Sandi Gec","Dejan Georgiev","Martin Gjoreski","Primož Godec","Teja Goli","Rok Gomišček","Vesna Gračner",
    "Miha Grohar","Vida Groznik","Matej Guid","Marjana Harcet","Bojan Heric","Ana Herzog","Tomaž Hočevar",
    "Suzana Hostnik","Tomaž Hovelja","Aleks Huč","Nejc Ilc","Franc Jager","Aleš Jaklič","Miha Janež",
    "Marko Janković","Amol Arjun Jawale","David Jelenc","Peter Jenko","Gregor Jerše","Matjaž Branko Jurič",
    "Aleksandar Jurišić","Maher Kaddoura","Benjamin Kastelic","Alenka Kavčič","Silvana Kavčič","Maja Kerkez",
    "Borut Paul Kerševan","Peter Marijan Kink","Klemen Klanjšček","Bojan Klemenc","Jelena Klisara","Vid Klopčič",
    "Petar Kochovski","Enja Kokalj","Igor Kononenko","Miran Koprivec","Domen Košir","Simon Krek","Matej Kristan",
    "Matjaž Kukar","Leon Lampret","Iztok Lapanja","Dejan Lavbič","Iztok Lebar Bajec","Aleš Leonardis","Žiga Lesar",
    "Jure Leskovec","Nikola Ljubešić","Sonja Lojk","Jure Lokovšek","Uroš Lotrič","Alan Lukežič","Nives Macerl",
    "Octavian-Mihai Machidon","Lidija Magdevska","Matija Marolt","Teodora Matić","Blaž Meden","Jan Meznarič",
    "Jurij Mihelič","Iztok Mihevc","Kristian Miok","David Modic","Miha Moškon","Martin Možina","Nežka Mramor Kosta",
    "Miha Mraz","Jon Muhovič","Miha Nagelj","Mimoza Naseka","Jakob Novak","Polona Oblak","Amra Omanović",
    "Bojan Orel","Matjaž Pančur","Aleš Papič","Uroš Paščinski","Peter Peer","Veljko Pejović","Špela Perner",
    "Matevž Pesek","Irena Pestotnik","Andrej Petelin","Mattia Petroni","Matej Pičulin","Ratko Pilipović",
    "Žiga Pirnar","Gregor Pirš","Marko Poženel","Ajda Pretnar","Žiga Pušnik","Mateja Ravnik","Andreja Retelj",
    "Matija Rezar","Mitja Rizvič","Borut Robič","Marko Robnik Šikonja","Peter Rot","Igor Rožanc","Ksenija Rozman",
    "Robert Rozman","Taja Runovc","Rok Rupnik","Aleksander Sadikov","Miha Schaffer","Petra Simonič","Arne Simonič",
    "Danijel Skočaj","Boštjan Slivnik","Davor Sluga","Tim Smole","Aleš Smonig Grnjak","Aleš Smrdel","Franc Solina",
    "Vlado Stankovski","Luka Šajn","Luka Šarc","Andrej Šeruga","Jaka Šircelj","Blaž Škrlj","Domen Šoberl",
    "Branko Šter","Erik Štrumbelj","Lovro Šubelj","Domen Tabernik","Vesna Tanko","Marko Toplak","Barbara Torkar",
    "Denis Trček","Mira Trebar","Jure Tuta","Matej Ulčar","Anita Valmarska","Damjan Vavpotič","Zdenka Velikonja",
    "Kristina Veljković","Janoš Vidali","Žiga Virk","Matej Vitek","Jaka Vodeb","Petar Vračar","Simon Vrhovec",
    "Martin Vuk","Aleš Watzak","Aljaž Zalar","Vitjan Zavrtanik","Nikolaj Zimic","Aljaž Zrnec","Helena Marija Zupan",
    "Blaž Zupan","Jure Žabkar","Aleš Žagar","Lan Žagar","Manca Žerovnik Mekuč","Rok Žitko","Slavko Žitnik",
    "Urška Žnidarič","Bojan Žunkovič"] tocno 211 oseb'''
    i = 0
    link_indexes = []
    for p in data['persons']:
        arrPersons.append(p['fullname_and_title']['sl'])
        i += 1
    k = 0

    for p in links:
        split = str(p['ime']).split()
        split.extend(str(p['priimek']).split())
        name = " ".join(split)
        arrLinks.append(name)
        print(name)
        k += 1

    print(str(len(arrPersons)) + ' ' + str(len(arrLinks)))
    neObstaja = 0
    for a in arrLinks:
        index = 0
        exist = 0
        for p in arrPersons:
            if compare_names(p, a):
                exist = 1
                link_indexes.append(index)
                break
            index += 1
        if exist == 0:
            neObstaja += 1
            link_indexes.append(-1)

    print(neObstaja)
    json_to_md(data['persons'], links, link_indexes, arrLinks)


