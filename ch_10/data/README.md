# About the data

| File | Description | Source |
| --- | --- | --- |
| `planets.csv` | Data on exoplanets. | The Open Exoplanet Catalogue database. |
| `stars.csv` | Data on individual stars. | The Open Exoplanet Catalogue database. |
| `winequality-red.csv` | Contains the chemical properties of red wines that were part of a blind-tasting, along with their scores. | The UCI Machine Learning Repository. |
| `winequality-white.csv` | Contains the chemical properties of white wines that were part of a blind-tasting, along with their scores. | The UCI Machine Learning Repository. |

### Sources
- The [Open Exoplanet Catalogue database](https://github.com/OpenExoplanetCatalogue/open_exoplanet_catalogue/) stores its data in a compressed XML. For the code used to extract the data needed to populate the `binaries.csv`, `planets.csv`, `stars.csv`, and `systems.csv` files, consult [planet_data_collection.ipynb](../../ch_09/planet_data_collection.ipynb). Data License:

  >Copyright (C) 2012 Hanno Rein<br><br>Permission is hereby granted, free of charge, to any person obtaining a copy of this database and associated scripts (the "Database"), to deal in the Database without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Database, and to permit persons to whom the Database is furnished to do so, subject to the following conditions:<br><br>The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Database. A reference to the Database shall be included in all scientific publications that make use of the Database.<br><br>THE DATABASE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE DATABASE OR THE USE OR OTHER DEALINGS IN THE DATABASE.

- The [UCI Machine Learning Repository](http://archive.ics.uci.edu) is a great source for finding datasets to practice ML. The wine datsets used in this chapter can be found [here](https://archive.ics.uci.edu/ml/datasets/wine+quality). Note that the data comes from this paper:

  > P. Cortez, A. Cerdeira, F. Almeida, T. Matos and J. Reis.<br>Modeling wine preferences by data mining from physicochemical properties. In Decision Support Systems, Elsevier, 47(4):547-553, 2009.
