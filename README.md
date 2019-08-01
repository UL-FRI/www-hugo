# www-hugo
The source code for Hugo version of certain websites at fri.uni-lj.si available at https://nejchirci.github.io/ with
laboratory page at https://nejchirci.github.io/lab/ and personal page at https://nejchirci.github.io/employees/ .

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
