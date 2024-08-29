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
- `graduation`: Integer, graduation year
- `codeforces`: Codeforces username
- `level`: Integer, current SIT Level ("`-2`" if graduated)

## [`/data/participations.json`](/data/participations.json)
An array of people, each person has the following:
- `id`: Either `ioi`/`boi`/`apio`/`jboi`/`egoi`
- `year`: Integer, year
- `country`: Either the 2-letters country code or "`online`"
- `start`: Start date
- `end`: End date
- `participants`: Dictionary of `<person ID> : Award name` (`gold`/`silver`/`bronze`/`hounarablemention`/`none`)
- `website`: Olympiad website of that year **(Optional)**

## [`/data/contact.json`](/data/contact.json)
An array of people, each person has the following:
- `id`: Member ID
- `email`: Contact email