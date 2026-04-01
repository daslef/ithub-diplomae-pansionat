# Django Unfold Admin Demo <!-- omit from toc -->

Repository contains a sample project build upon the Unfold theme for Django. It includes the best practices when it comes to Unfold but keep in mind that it does not incorporate any more in-depth business logic. Everything is composed just for demonstration purposes.

- [Unfold](https://github.com/unfoldadmin/django-unfold) - Admin theme for Django
- [Turbo](https://github.com/unfoldadmin/turbo) - Django & Next.js starter kit including Unfold

## Table of contents <!-- omit from toc -->

- [Installation](#installation)
- [Loading sample data](#loading-sample-data)
- [Compiling Styles](#compiling-styles)

## Installation

First of all, it is required to create new `.env` file containing environment variables for the project. In this case, there are just two most important variables needed to be configured. If you are on local machine, set `DEBUG=1` to enable debug mode for further development. Second variable is `SECRET_KEY` which needs to be configured with some random long and secure string. Project is quite simple and it should be possible to run it without Docker at all. Make sure Python 3.13 is installed together with Poetry and follow the commands below to install all required dependencies and run migrations.

```bash
git clone git@github.com:unfoldadmin/formula.git
```

Run these commands inside `formula` directory, to install all dependencies and to run all migrations.

```bash
docker compose up
```

Create the admin user or you can't access to the instance.

```bash
docker compose exec web python manage.py createsuperuser
```

Run the command below to start the local development server.

## Loading sample data

After successful installation, database will be empty and there will be no data to observe through the admin area. Unfold provides some sample data available under `formula/fixtures`. These data can be loaded via commands below. It is important to run this command against empty database so primary keys will match.

```bash
docker compose exec web python manage.py loaddata formula/fixtures/*
```

## Compiling Styles

```python
# settings.py
from django.templatetags.static import static


UNFOLD = {
    "STYLES": [
        lambda request: static("css/styles.css"),
    ],
}
```

To compile new styles, run one of the commands below depending on your needs. To see what exactly the commands are doing and how the files are linked check `scripts` section inside `package.json`.

```bash
npm run tailwind:build  # one-time build
npm run tailwind:watch  # watch all files for changes
```

Before compiling the styles it is important to install all node dependencies as well which in our case contain just TailwindCSS and its typography plugin for styling formatted blocks of texts inside the WYSIWYG editor.

```bash
npm install
```
