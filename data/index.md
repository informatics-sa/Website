---
lang: en
title: Public Data API
---
# Public Data API

## [`/data/people.json`](/data/people.json)
An array of people, each person has the following:
- `id`: which will be usually in `firstname_lastname` format
- `arname`: Name in Arabic
- `enname`: Name in English 
- `graduation`: Integer, graduation year **(nullable)**
- `codeforces`: Codeforces username **(nullable)**
- `level`: Integer, current SIT Level ("`-2`" if graduated)

## [`/data/participations.json`](/data/participations.json)
An array of olympiads SIT participated in, each olympiad has the following:
- `id`: Either `ioi`/`boi`/`apio`/`jboi`/`egoi`
- `year`: Integer, year
- `country`: Either the 2-letters country code or "`online`"
- `start`: Start date
- `end`: End date
- `participants`: Dictionary of `<member ID>: <award name>`
    - `<award name>`: (`gold`/`silver`/`bronze`/`hounarablemention`) **(nullable)** (null in case of no award)
- `website`: Olympiad website of that year **(nullable)**

## [`/data/contact.json`](/data/contact.json)
A dictionary of (`developers`/`maintainers`/`admin`), each having an array of person ID

> *Note*:
> check the files for examples of formating.
