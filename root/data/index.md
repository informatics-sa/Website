---
lang: en
title: Public Data API
layout: default
todo: "DEVELOPER FORMAT: Make the files compatibale to be used in SQL format"
---
# Public Data API
Always check the files for examples of the formatting.

## How is the docs written?
Description of the JSON type of the file itself, then the fields of it by indicating one of the types below:
- String
- Integer
- Date: String in gregorian date in format `YYYY/M/D`

## [`/data/people.json`](/data/people.json)
An array of people, each person has the following:
- `id`: Integer, informatics ID of the student, currently fetched from IDs assigned by Marko **(unique)**
- `arname`: String, Name in Arabic
- `enname`: String, Name in English 
- `graduation`: Integer; graduation year **(nullable)**
- `codeforces`: String, Codeforces username **(nullable)**
- `level`: Integer, current SIT Level ("`-1`" if he/she graduated, "`-2`" if he/she disqualified/left before graduating, "`-3`" if he/she was never a student)

## [`/data/participations.json`](/data/participations.json)
An array of olympiads SIT participated in, each olympiad has the following:
- `id`: String, An id of an olympiad that exists in `olympiads.json`
- `year`: Integer, year
- `country`: String, the 2-letters country code of the host country of the olympiad.
- `start`: Date, The start day of the olympiad
- `end`: Date, the end day of the olympiad
- `participants`: Dictionary of `<member ID>: <award name>`
    - `<award name>`: (`gold`/`silver`/`bronze`/`hounarablemention`) **(nullable)** (null in case of no award)
- `website`: Olympiad website of that year, with `https://` in prefix without `/` in the end **(nullable)**
- `online`: Boolean indicates if Saudi participated online or not, default is False **(optional)**

## [`/data/olympiads.json`](/data/olympiads.json)
An array of olympiads SIT participated in, each olympiad has the following:
- `id`: String, Should be lowercase, 3/4-letters short olympiad name (i.e. `ioi`, `imo`, `egoi`)
- `arname`: String, Full name in Arabic
- `enname`: String, Full name in English 
- `official`: Boolean, is Saudi Arabia an official country or not
- `participations_count`: How many students participate per year (optional, needed when it's used in `tsts.json`)
- `website`: Olympiad website of that year, with `https://` in prefix without `/` in the end **(nullable)**

## [`/data/images.json`](/data/images.json)
These images would be shown in [Image libary](https://sainformatics.org/images), shouldn't have a strict rules about the title/description.

An array of images, each image consist of these labels:
- `src`: String, Filename of the image in [`/img` directory in the repository](https://github.com/informatics-sa/Website/tree/main/root/img) 
- `artitle`: String, Arabic title
- `entitle`: String, English title
- `ardescription`: String, Arabic description
- `endescription`: String, English description
- `date`: Date, the date of this image

## [`/data/contact.json`](/data/contact.json)
A dictionary of (`developers`/`maintainers`/`admin`), each having an array of person ID

## [`/data/exams.json`](/data/exams.json)
A dictionary of exam IDs, where every exam has:
- `name`: Name of exam in English
- `date`: Date of exam in format `YYYY/M/D`
- `problems`: An array of problem ID
- `participants`: A dictionary of student ID and an array of integers which is score per task

## [`/data/tsts.json`](/data/tsts.json)
A dictionary of year and olympiad IDs, and every olympiad ID contains a set of exams, and set of execluded students, for example:
```json
{
    "2025": {
        "_general_execluded": ["sultan_alaiban"],
        "ioi": {
            "exams": ["exam1", "exam2"],
            "min_birthdate": "2009/6/30",
            "female_only": false,
            "execluded": ["muaath_alqarni", "ali_alsalman"]
        }
    }
}
```

Additional rules (Optional):
- `execluded`: An array of student ID (strings)
- `min_graduation`: An integer, minimum graduation year to be eligable.
- `female_only`: Boolean, true if the competition is female only.
- `min_birthdate`: A date, **not working currently**, but will be used in the future.


# Constant files
These files are needed, but they aren't database kind.
## [`/data/countries.json`](/data/countries.json)
## [`/data/translations.json`](/data/translations.json)
