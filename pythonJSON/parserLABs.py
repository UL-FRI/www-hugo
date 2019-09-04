import json
import frontmatter
import io
from os import path
from shutil import copyfile


def json_to_md(loaded_json):

    for p in loaded_json:
        fname = './content/sl/labs/' + p['abbreviation'].lower() + '.md'
        fname_en = './content/en/labs/' + p['abbreviation'].lower() + '.md'

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


with io.open('./sampleJSON/labs.json', 'r', encoding='utf8') as json_labs, open('./sampleJSON/labDescriptions.json', 'r', encoding='utf8') as desc_labs:
    data = json.load(json_labs)
    desc = json.load(desc_labs)
    json_to_md(data['labs'])
    json_to_md(desc)
