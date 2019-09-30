import json
import frontmatter
import io
from os import path
from shutil import copyfile


def json_to_md(loaded_json):

    for p in loaded_json:
        fname = './content/sl/laboratorij/' + p['abbreviation'].lower() + '.md'
        fname_en = './content/en/laboratorij/' + p['abbreviation'].lower() + '.md'

        if not path.isfile(fname):
            copyfile('./sampleJSON/template_lab.md', fname)
        if not path.isfile(fname_en):
            copyfile('./sampleJSON/template_lab.md', fname_en)

        with io.open(fname, 'r', encoding='utf8') as md, io.open(fname_en, 'r', encoding='utf8') as md_en:

            # Parse file's front matter
            post_md = frontmatter.load(md, encoding='utf-8')
            post_md_en = frontmatter.load(md_en, encoding='utf-8')

            if post_md.get('abbreviation') is None and p['abbreviation'] is not None:
                post_md['abbreviation'] = p['abbreviation']
            if post_md.get('title') is None and p['title'] is not None:
                post_md['title'] = p['title']['sl']
            if post_md.get('location') is None and p['location'] is not None:
                post_md['location'] = p['location']
            if post_md.get('body') is None and p['description'] is not None:
                post_md.content = p['description']['sl']
            if post_md.get('id') is None and 'id' in p:
                post_md['id'] = p['id']

            if post_md_en.get('abbreviation') is None and p['abbreviation'] is not None:
                post_md_en['abbreviation'] = p['abbreviation']
            if post_md_en.get('title') is None and p['title'] is not None:
                post_md_en['title'] = p['title']['en']
            if post_md_en.get('location') is None and p['location'] is not None:
                post_md_en['location'] = p['location']
            if post_md_en.get('body') is None and p['description'] is not None:
                post_md_en.content = p['description']['en']
            if post_md_en.get('id') is None and 'id' in p:
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

            with io.open(jname, 'w+', encoding='utf8') as to:
                from_insert = p['members']
                json.dump(from_insert, to)


with io.open('./sampleJSON/labs.json', 'r', encoding='utf8') as json_labs, open('./sampleJSON/labDescriptions.json', 'r', encoding='utf8') as desc_labs:
    data = json.load(json_labs)
    desc = json.load(desc_labs)
    json_to_md(data['labs'])
    json_to_md(desc)
