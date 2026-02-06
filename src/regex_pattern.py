import re

NKPT = re.compile(r"#\s+NKPT\s+(\d+)\s+NBND\s+(\d+)\s+NSPIN\s+(\d+)")
NEPTS = re.compile(r"#\s+NEPTS\s+(\d+)\s+NPROJ\s+(\d+)\s+NSPIN\s+(\d+)")
EFERMI = re.compile(r"\s+([+-]?\d+.\d+)")
KPT_INDEX = re.compile(r"\s+(\d+)\s+\(([\d+,]+)\)\/(\d+)")
DATA = re.compile(r'-?\d+?\.\d+E[+-]\d+')  # matches "-9.9999E+99"