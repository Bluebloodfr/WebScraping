#!/bin/bash

# Create the data directory if it doesn't exist
mkdir -p data

# Download the files
curl -L -o data/df_produit.zip https://github.com/DATAtourism/Application/raw/master/df_produit.zip
curl -L -o data/df_fete.zip https://github.com/DATAtourism/Application/raw/master/df_fete.zip
curl -L -o data/df_lieu.zip https://github.com/DATAtourism/Application/raw/master/df_lieu.zip
curl -L -o data/df_it.zip https://github.com/DATAtourism/Application/raw/master/df_it.zip

