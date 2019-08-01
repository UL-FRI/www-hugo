import json
import frontmatter
import io
from shutil import copyfile

with open('persons.json') as json_people:
    data = json.load(json_people)
    employeeID = 0
    for p in data['persons']:
        fname = './md/' + str(employeeID) + '.md'
        copyfile('template_employee.md', fname)

        with io.open(fname, 'r') as f:

            # Parse file's front matter
            post = frontmatter.load(f)
            if post.get('fullname_and_title') is None:
                post['fullname_and_title'] = str(p['fullname_and_title']['sl'])
            if post.get('web_category') is None:
                post['web_category'] = str(p['web_category']['sl'])
            if post.get('phone') is None:
                post['phone'] = str(p['phone'])
            if post.get('sicris_researcher_number') is None:
                post['sicris_num'] = str(p['sicris_researcher_number'])
            if post.get('picture') is None:
                post['picture'] = str(p['picture'])
            if post.get('description') is None:
                post.content = str(p['description']['sl'])



            # Save the file
            new = io.open(fname, 'wb')
            frontmatter.dump(post, new)
            new.close()

        fname = './data/' + str(employeeID) + '_employee.json'
        with io.open(fname, 'w+') as to:
            from_insert = p['subjects']
            json.dump(from_insert, to)
            from_insert = p['labs']
            json.dump(from_insert, to)

        employeeID += 1






