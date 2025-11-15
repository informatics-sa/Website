---
lang: en
title: Developer Documentation
layout: default
todo: "DEVELOPER FORMAT: Make the files compatibale to be used in SQL format"
---
# Developer documentation

## How does the website work?
- Any maintainer/developer commits some changes to Github
- Github workflow runs [`build.py`](https://github.com/informatics-sa/Website/blob/main/build.py) script
- `build.py` builds all HTML pages only by their [front-matter](http://jekyllrb.com/docs/front-matter/)
- Jekyll builds the pages based on `layout` field in the front matter, layouts are written in [`_layouts` folder](https://github.com/informatics-sa/Website/tree/main/root/_layouts)
- Github workflow finishes and Github pages hosts the static HTML website

## The library
The core library serves the core JSON files and takes care of some error handling and merging data togother.

Here is a **TODO list**:
- Error handling
- Add more data checking on the files with clear error messages

## Languages and Translation
Here is the main translations file: [`translations.json`](https://sainformatics.org/data/translations.json).

The list of languages exist in `utils.py`, it should be moved by devs to `build.py`. The first language in that list is the primary language.

The build script will copy every language to `_data/TWO_LETTER_CODE` directory as `.yml`.

For any file in `_data` folder in jeykll, you can access it by `site.data.FILE_NAME.ANY_FIELD`, and this is the way will be used for translations like this:

{% raw %}
```jekyll
{{site.data[page.lang].text_name}}
```
{% endraw %}

### URLs based on language
Here is an example:
{% raw %}
```jekyll
{% if page.lang != site.data.build.primary_lang %}/{{ page.lang }}/{% endif %}/olympaids/boi/2024
```
{% endraw %}

## Future projects
You might check the [original TODO list](https://github.com/informatics-sa/Website/blob/main/TODO.md), but it's up to your laziness if you will do them.

## Additional guides
- [`/debug`](https://sainformatics.org/debug): Website debugging URL
- [`/data`](https://sainformatics.org/data): Data guide for maintainers
- You might check the other private repos in the organization which has some assisting tools