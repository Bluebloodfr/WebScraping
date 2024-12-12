#!/bin/bash

# Create the data directory if it doesn't exist
mkdir -p data

URL="https://github.com/DATAtourism/Application/raw/master"
#URL="https://github.com/DATAtourism/Application/blob/master/"   # fichier html
#URL="https://github.com/CarlaMorenoH/DATAtourisme/tree/eda56f7fc0b1396ee9bd54be06e4936b76bddf9d"    # fichier html

# Download the files
curl -L -o data/df_produit.zip $URL/df_produit.zip
curl -L -o data/df_fete.zip $URL/df_fete.zip
curl -L -o data/df_lieu.zip $URL/df_lieu.zip
curl -L -o data/df_it.zip $URL/df_it.zip

