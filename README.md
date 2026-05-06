# Rockland P Reader

An unofficial way to read [Rockland Scientific](https://rocklandscientific.com/) .p files with python

Currently only testing with .p files off of a Microrider attached to a Slocum glider, [example file](/examples/raw/dat_1336.p) included in repo.
There is very little error checking and 0 quality control, still needs to be validated against a verified .p file reader.
This is a first draft, it's not very fast or efficient, mainly a proof of concept.


### Current Features:

* Reads config to determin matrix and channel layout
* Decodes P file into raw matrix of numeric values
* Inserts raw values into a Dataframe


### Planned Features:

* Convert the raw values to physical values with units.

