import json
import frontmatter
import io
from shutil import copyfile


with open('labs.json') as json_labs:
    data = json.load(json_labs)
    for p in data['labs']:
        fname = './markdown/' + str(p['abbreviation']).lower() + '.md'
        copyfile('template_lab.md', fname)
        
        with io.open(fname, 'r') as f:

            # Parse file's front matter
            post = frontmatter.load(f)
            if post.get('abbreviation') is None:
                post['abbreviation'] = str(p['abbreviation'])
            if post.get('title') is None:
                post['title'] = str(p['title']['sl'])
            if post.get('location') is None:
                post['location'] = str(p['location'])
            if post.get('body') is None:
                post.content = str(p['description']['sl'])

            # Save the file
            new = io.open(fname, 'wb')
            frontmatter.dump(post, new)
            new.close()

        fname = './data/' + str(p['abbreviation']) + '_mem.json'
        with io.open(fname, 'w+') as to:
            from_insert = p['members']
            json.dump(from_insert, to)






