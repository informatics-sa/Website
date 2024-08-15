# Public Data API
## `/data/members.json`
An array of people, each person has the following:
- `id`: which will be usually in `firstname_lastname` format
- `arname`: Name in Arabic
- `enname`: Name in English
- `graduation`: Integer, graduation year
- `codeforces`: Codeforces username

## `/data/participations.json`
An array of people, each person has the following:
- `id`: Eitehr `ioi`/`boi`/`apio`/`jboi`/`egoi`
- `year`: Integer, year
- `country`: Either a country name or `online`
- `start`: Start date
- `end`: End date
- `participants`: Dictionary of people IDs : Award name (`gold`/`silver`/`bronze`/`none`)
- `website`: Olympiad website of that year **(Optional)**