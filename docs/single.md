<p align="center">
  <a href="../README.md">
    <img src="https://img.shields.io/badge/↩-README-white?style=for-the-badge">
  </a>
  <a href="restraints.md">
    <img src="https://img.shields.io/badge/◀ - File name restraints-blue?style=for-the-badge">
  </a>
  <a href="multiple.md">
    <img src="https://img.shields.io/badge/▶ - Parsing multiple DAT files-blue?style=for-the-badge">
  </a>
</p>

# Parsing a DAT file

The script expects at least one argument when called. If there is only one argument passed, this argument **MUST** point to a valid DAT file.

Let `dat2csv` be the alias pointing to this script:

`$ dat2csv path/to/file.dat`

That's it. Just point to a valid file (see [file name restraints](restraints.md) for valid file names) and the script will do its job.

## CSV files and overwritting problems

All CSV files are generated in the same folder where the inputted DAT is located.

The CSV file names follows a fixed pattern, and do not inherit nothing from the name of the inputted DAT file. This can lead to the following problem: 

> There are two different band result files in the same folder: `band1.dat` and `band2.dat`. <br> You parse `band1.dat`, then parse `band2.dat`. <br>
If you have not moved the DAT files to separate folders, the results from `band1.dat` will be overwritten by the results of `band2.dat`.

**Be careful to not overwrite results from two different DAT files located in the same folder.**

## Spin-polarized solutions
For the user convenience, the script automatically separates the alpha and beta spin results into different CSV files. It also includes the information of the spin in the comment section of the CSV header, so users can easily identify the spin inside OriginLab worksheets.

For systems without spin-polarization, where the alpha and beta spin are equivalent, the script generates a single CSV file for the alpha spin.