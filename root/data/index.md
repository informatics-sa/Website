---
lang: en
title: Public Data API
---
# Public Data API

Always check the files for examples of the formatting.

## [`/data/people.json`](/data/people.json)
An array of people, each person has the following:
- `id`: which will be usually in `firstname_lastname` format
- `arname`: Name in Arabic
- `enname`: Name in English 
- `graduation`: Integer; graduation year **(nullable)**
- `codeforces`: Codeforces username **(nullable)**
- `level`: Integer; current SIT Level ("`-1`" if he/she graduated, "`-2`" if he/she disqualified/left before graduating, "`-3`" if he/she was never a student)

## [`/data/participations.json`](/data/participations.json)
An array of olympiads SIT participated in, each olympiad has the following:
- `id`: An id of an olympiad that exists in `olympiads.json`
- `year`: Integer, year
- `country`: Either the 2-letters country code or "`online`"
- `start`: Start date
- `end`: End date
- `participants`: Dictionary of `<member ID>: <award name>`
    - `<award name>`: (`gold`/`silver`/`bronze`/`hounarablemention`) **(nullable)** (null in case of no award)
- `website`: Olympiad website of that year, with `https://` in prefix without `/` in the end **(nullable)**

## [`/data/olympiads.json`](/data/olympiads.json)
An array of olympiads SIT participated in, each olympiad has the following:
- `id`: Should be lowercase, 3/4-letters name (i.e. `ioi`, `imo`)
- `arname`: Full name in Arabic
- `enname`: Full name in English 
- `official`: Boolean, is Saudi Arabia an official country or not
- `website`: Olympiad website of that year, with `https://` in prefix without `/` in the end **(nullable)**

## [`/data/images.json`](/data/images.json)
An array of images, each image consist of these labels:
- `src`: Filename of the image in `/img` directory
- `artitle`: Arabic title
- `entitle`: English title
- `ardescription`: Arabic description
- `endescription`: English description
- `date`: String, usually Gregorian date in format `YYYY/MM/DD` or `YYYY/M/D`

## [`/data/contact.json`](/data/contact.json)
A dictionary of (`developers`/`maintainers`/`admin`), each having an array of person ID
