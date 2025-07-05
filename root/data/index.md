---
lang: en
title: Public Data API
layout: default
todo: "DEVELOPER FORMAT: Make the files compatibale to be used in SQL format"
---
# Public Data API
Always check the files for examples of the formatting.

## How is the docs written?
### Data types
#### JSON datatypes
- String
- Integer
- Boolean
- Float
- Array: JSON array `[...]`
- Dictionary/Object: JSON object `{...}`
#### Custom defined
- Date: String, gregorian date in format `YYYY/M/D`
- URL: String, starts with prefix `https://` and without suffix `/`
- Email: String, an email

### Properties
By default each property is required, here are the additional properties:
- **unique**: It should be distinct through the whole file
- **optional**: It's not required, the default value is `null` except if mentioned otherwise
- **deprecated**: It was used previously and not removed because of development issues
- **future**: The field isn't used in any current data, but could be useful in the future development

## [`/data/people.json`](/data/people.json)
An array of people, each person has the following:
- `iid`: Integer, informatics ID of the student, currently fetched from IDs assigned by Marko **(unique)**
- `id`: String, lowercase with no spaces ID usually in format `firstname_lastname`, not used anymore and shouldn't be written, it will be removed by devleopers when not needed anymore **(deprecated)**
- `arname`: String, Name in Arabic
- `enname`: String, Name in English 
- `level`: Integer, current SIT Level ("`-1`" if he/she graduated, "`-2`" if he/she disqualified/left before graduating, "`-3`" if he/she was never a student)
- `graduation`: Integer, graduation year **(optional)**
- `codeforces`: String, Codeforces username **(optional)**
- `email`: Email, most official email, usually `...@sainformatics.org`, used in case of [contact page](https://sainformatics.org/contact) **(optional)**
- `female`: Boolean, used in girls competitions, default is `false` **(optional)**

## [`/data/participations.json`](/data/participations.json)
An array of olympiads SIT participated in, each olympiad has the following:
- `id`: String, An id of an olympiad that exists in `olympiads.json`
- `year`: Integer, year
- `country`: String, the 2-letters country code of the host country of the olympiad.
- `start`: Date, The start day of the olympiad
- `end`: Date, the end day of the olympiad
- `participants`: Dictionary of `<member ID>: <award name>`
    - `<award name>`: (`gold`/`silver`/`bronze`/`hounarablemention`) (null in case of no award)
- `website`: URL, Olympiad website of that specific year **(nullable)**
- `online`: Boolean, indicates if Saudi participated online or not, default is False **(optional)**

## [`/data/olympiads.json`](/data/olympiads.json)
An array of olympiads SIT participated in, each olympiad has the following:
- `id`: String, Should be lowercase, 3/4-letters short olympiad name (i.e. `ioi`, `imo`, `egoi`) **(unique)**
- `arname`: String, Full name in Arabic
- `enname`: String, Full name in English 
- `official`: Boolean, is Saudi Arabia an official country or not
- `participations_count`: Integer, How many students participate per year (optional, needed when it's used in `tsts.json`)
- `website`: URL, General Olympiad website, shouldn't be a specific year website except if it was the first version of the olympiad **(nullable)**

## [`/data/images.json`](/data/images.json)
These images would be shown in [Image libary](https://sainformatics.org/images), shouldn't have a strict rules about the title/description.

You might check and share [image proposals form](https://forms.gle/oxJKdEX78kA8fYzQ6), which is maintained by the website developers.

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
- `name`: String, Name of exam in English
- `date`: Date, The day of the exam
- `problems`: Array of problem ID
- `participants`: Dictionary of student ID and an array of floats which is score per task

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
- `execluded`: Array, of strings student ID
- `min_graduation`: Integer, minimum graduation year to be eligable
- `female_only`: Boolean, true if the competition is female only
- `min_birthdate`: Date, the minimum birthdate for eligibility **(future)**


# Constant files
These files are needed, but they aren't database kind.
## [`/data/countries.json`](/data/countries.json)
## [`/data/translations.json`](/data/translations.json)
