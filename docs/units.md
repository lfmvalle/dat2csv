<p align="center">
  <a href="../README.md">
    <img src="https://img.shields.io/badge/↩-README-white?style=for-the-badge">
  </a>
  <a href="multiple.md">
    <img src="https://img.shields.io/badge/◀ - Parsing multiple DAT files-blue?style=for-the-badge">
  </a>
  <a href="precision.md">
    <img src="https://img.shields.io/badge/▶ - Numerical precision-blue?style=for-the-badge">
  </a>
</p>

# Energy unit conversion

It is somewhat rare to address results directly in Hartree units. The vast majority of works in the literature deal with *electron-Volt* units, eV.

By default, this script automatically converts all energy units to eV. If you intend to keep Hartree units, use the ***-h*** parameter when calling the script. The position where this parameter must be doesn't matter:

All these have the same behavior: <br>
`$ dat2csv -h some-band-file.dat some-doss-file.dat` <br>
`$ dat2csv some-band-file.dat -h some-doss-file.dat` <br>
`$ dat2csv some-band-file.dat some-doss-file.dat -h`

Have in mind that the energy unit will be applied to **ALL FILES** in a [multiple file parsing](multiple.md).

The Hartree to eV conversion factor used in the script is `27.211386` (from: [NIST / 2022 CODATA recommended values](https://physics.nist.gov/cgi-bin/cuu/Value?hrev)).

For a more descriptive view about the unit conversion, see the table below:

| Applied for | Result | Variable | Converted units <br> (script default) | Forced default <br> (using -h) |
| :- | :- | :-: | :-: | :-: |
| BAND | Path of k-points | k | - | - |1
| BAND | Band energy | E(k) | eV | Hartree |
| DOS / COOP / COHP | Energy | E | eV | Hartree |
| DOS / COOP / COHP | Density of States | D(E) | (states/eV)/cell | (states/Hartree)/cell |