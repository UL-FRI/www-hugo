# www-hugo
The source code for Hugo version of selected website at fri.uni-lj.si that includes personal and lab pages.

## Important folders
Pages in Slovene language:

* [content/sl/osebje](https://github.com/UL-FRI/www-hugo/tree/master/content/sl/osebje) - headers for personal pages
* [data/osebje/project](https://github.com/UL-FRI/www-hugo/tree/master/content/sl/data/osebje/projects) - list of projects, updated automatically, IDs of projects displayed on the personal page are listed in [personal page headers](https://github.com/UL-FRI/www-hugo/tree/master/content/sl/osebje)

## Previews

[![Netlify Status](https://api.netlify.com/api/v1/badges/8e748765-0673-4633-a764-8a2ed70340f1/deploy-status)](https://app.netlify.com/sites/www-hugo/deploys)

Preview available at: [https://www-hugo.netlify.com](https://www-hugo.netlify.com).

## Development
### Dependencies
* [Hugo](https://gohugo.io/)
* [GNU Make](https://www.gnu.org/software/make/)

### Commands
#### Local development server
```bash
make
```

#### Builds
##### Development
```bash
make build-dev
```

##### Production
```bash
# Replace "http://example.com" with the base url of the site
make build-prod url=http://example.com 
```

#### Other
```bash
make clean  # run after "make build-dev" or "make build-prod"
```
