Virtual Learning Environment Web Application
=============

The VLE Web App is a Django project for a web application that provides a 
virtual learning environment for the Alúmnica Learners. It depends on the
alumnica_model repo.


#Django webapp development

Insert all django info here plz!!!
```
Django info
```

#Front End development environment
Front end development environment fro the VLE Alumnica Web App is made out of a custom NodeJS framework built with the following as a base:
#### Layout and Appearance
SASS utilizing Foundaiton 6 framweork and custom components with Autoprefixers for maximum browser compatibility.

#### JavaScript
JavaScript from NodeJS modules bundled with Webpack and Babel as well as custom scripts that control overall app behaviour
* All JS files inside `front-end/assets/js/pats` are for proof of concept only. Full functionality is  developed and applied in vle_webapp

#### HTML
HTML is composed utilizing Paninni and Handlebars for modular HTML static prototyping before implementing to Django templates.

#### Build in Browser Sync
Browser Sync for both Front end Static and Back end development

##Instalation
To use this template, your computer needs:

* NodeJS (0.12 or greater)
* Git

### Manual Setup

To manually set up the template, first download it with Git:

```bash
`git clone https://gitlab.com/code-ing/ti/fundacion-manuel-moreno/alumnica/vle_webapp.git`
```

Then open the folder in your command line, and install the needed dependencies:

```bash
cd vle_webapp
npm install
```

### Runninv Dev Environments

#### Front End  live environment

On your terminal run
```
npm run frontLive
```
This should start the build process and finish deploying a BrowserSync instance under:
```
http://localhost:8000
```
All changes to CSS and the JS bundle will automatically be updated and copied into the Django webapp location to always maintain both applications in sync

#### Back end Live environment
To make edits to CSS and the JS bundle directly inside the live Django application you must have the entire Django app installed and running with a database and all service workers.

Run your local Django server according to `Django Info`

In your terminal run
```
npm run backLive
```
This should start the build process and finish deploying a BrowserSync instance under:
```
http://localhost:8001
```
All changes to CSS and the JS bundle will automatically be updated and copied into the Django webapp location and Front-End dev env to always maintain both applications in sync

## Heroku

add Node JS buildpack to heroku to run before Django

`heroku buildpacks:add --index 1 heroku/nodejs`

Heroku will run `postinstall` script from `package.json` to run all SASS and JS scripts automatically.