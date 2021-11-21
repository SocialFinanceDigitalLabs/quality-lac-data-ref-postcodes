# Quality LAC Data Reference - Postcodes

This is a redistribution of the **ONS Postcode Directory** shaped
to be used in the Quality Lac Data project.

This repository contains PyPI and npm distributions of
subsets of this dataset as well as the scripts to
generate them from source.

Source: Office for National Statistics licensed under the Open Government Licence v.3.0

Read more about this dataset here:

* https://geoportal.statistidcs.gov.uk/datasets/ons::ons-postcode-directory-august-2021/about

To keep distribution small, only pickled dataframes compatible 
with pandas 1.0.5 are included. This will hopefully change
once we figure out how to do different versions as extras.

As pickle is inherently unsafe, the SHA-512 checksum for each file
is included in [hashes.txt](qlacref_postcodes/hashes.txt). This
file is signed with [this key](./id_rsa.pub). 

When downloading from PyPI, specify the environment variable
`QLACREF_PC_KEY` to either be the public key itself, or a path
to where it can be loaded from. The checksums are then verified
and each file checked before unpickling. 
