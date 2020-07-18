import json
import frontmatter
import io
from os import path
import os
from shutil import copyfile


def get_slug(string):
    string = string.lstrip(' ').lower()
    string = string.replace(' ', '-')

    c1 = 'č'.encode()
    c2 = 'ć'.encode()
    z = 'ž'.encode()
    s = 'š'.encode()
    dz = 'đ'.encode()

    string = string.encode()
    string = string.replace(c1, b'c')
    string = string.replace(c2, b'c')
    string = string.replace(z, b'z')
    string = string.replace(s, b's')
    string = string.replace(dz, b'dz')
    string = string.decode('utf-8')

    return string

def json_to_md(loaded_json):

    for p in loaded_json:
        print(p)

        folderName = './content/sl/laboratorij/' + p['abbreviation'].lower()
        folderNameEn = './content/en/laboratorij/' + p['abbreviation'].lower()

        try:
            os.mkdir(folderName)
        except OSError:
            print("Creation of the directory %s failed" % folderName)
        else:
            print("Successfully created the directory %s " % folderName)

        try:
            os.mkdir(folderNameEn)
        except OSError:
            print("Creation of the directory %s failed" % folderNameEn)
        else:
            print("Successfully created the directory %s " % folderNameEn)

        fname = folderName + '/index.md'
        fname_en = folderNameEn + '/index.md'

        if not path.isfile(fname):
            copyfile('./structJSON/template_lab.md', fname)
        if not path.isfile(fname_en):
            copyfile('./structJSON/template_lab.md', fname_en)


        with io.open(fname, 'r', encoding='utf8') as md, io.open(fname_en, 'r', encoding='utf8') as md_en:

            # Parse file's front matter
            post_md = frontmatter.load(md, encoding='utf-8')
            post_md_en = frontmatter.load(md_en, encoding='utf-8')

            #Overwrite data
            overwrite = 1
            if (post_md.get('abbreviation') is '' or overwrite) and p['abbreviation'] is not None:
                post_md['abbreviation'] = p['abbreviation']
            if (post_md.get('title') is '' or overwrite) and p['title'] is not None:
                post_md['title'] = p['title']['sl']
            if (post_md.get('location') is '' or overwrite) and 'location' in p:
                if p['location'] != "Some Random Location":
                    post_md['location'] = p['location']
            if (post_md.get('body') is '' or overwrite) and p['description'] is not None:
                if p['description']['sl'] != "Nek random opis":
                    post_md.content = p['description']['sl']
            if (post_md.get('id') is '' or overwrite) and 'id' in p:
                post_md['id'] = p['id']

            if (post_md_en.get('abbreviation') is '' or overwrite) and p['abbreviation'] is not None:
                post_md_en['abbreviation'] = p['abbreviation']
            if (post_md_en.get('title') is '' or overwrite) and p['title'] is not None:
                post_md_en['title'] = p['title']['en']
            if (post_md_en.get('location') is '' or overwrite) and 'location' in p:
                if p['location'] != "Some Random Location":
                    post_md_en['location'] = p['location']
            if (post_md_en.get('body') is '' or overwrite) and p['description'] is not None:
                if p['description']['en'] != "Some Random Description":
                    post_md_en.content = p['description']['en']
            if (post_md_en.get('id') is '' or overwrite) and 'id' in p:
                post_md_en['id'] = p['id']

            # Save the file
            new = io.open(fname, 'wb')
            new_en = io.open(fname_en, 'wb')
            frontmatter.dump(post_md_en, new_en)
            frontmatter.dump(post_md, new)
            new.close()
            new_en.close()

        if 'members' in p:
            jname = './data/laboratorij/members/' + str(p['abbreviation']).lower() + '.json'
            members = p['members']

            for member in members:
                member['slug'] = get_slug(member['name']+'-'+member['surname'])
                print(member)


            with io.open(jname, 'w+', encoding='utf8') as to:
                from_insert = p['members']
                json.dump(from_insert, to)


with io.open('./sampleJSON/labs.json', 'r', encoding='utf8') as json_labs, open('./sampleJSON/labDescriptions.json', 'r', encoding='utf8') as desc_labs:
    data = json.load(json_labs)
    desc = json.load(desc_labs)
    json_to_md(data['labs'])
    json_to_md(desc)
