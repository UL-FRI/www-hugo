# www-hugo
The source code for Hugo version of certain websites at fri.uni-lj.si available at https://nejchirci.github.io/ with
laboratory page at https://nejchirci.github.io/lab/ and personal page at https://nejchirci.github.io/employees/ .


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
