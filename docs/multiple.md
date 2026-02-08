[↩ README](../README.md) | [◀ Parsing a DAT file](single.md) | [ Energy unit conversion ▶](units.md)

# Parsing multiple DAT files

When dealing with a lot of DAT results, calling the script for each DAT file you want to parse is a tedious work.

To solve this, the script allows you to chain as many DAT files as you want in the same script call:

Let `dat2csv` be the alias pointing to this script:

`$ dat2csv some/folder/some-band.dat another/folder/another-band.dat that/other/folder/that-doss.dat` <br>
Parses `some-band.dat` and generates the CSV files in the `some/folder/` directory. <br>
Parses `another-band.dat` and generates the CSV files in the `another/folder/` directory. <br>
Parses `that-doss.dat` and generates the CSV files in the `that/other/folder/` directory.

All that applies to a [single DAT file parsing](single.md) also applies to the multiple file parsing.

Files are added to a file processing queue and are parsed in the same order they are passed in the script call.