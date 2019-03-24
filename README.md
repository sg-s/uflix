# uflix


![image](images/header.png)

A tiny python toolbox to help you organize your movies. 


# Usage

## Make a CLI-version from the python script

```bash
python uflix.py make-cli
```

This generates a version of the script that can be run from the command line. This version will be used in the rest of this readme. 

## Clean up a directory containing movies 

```bash
uflix clean
```

This command does the following things:

* makes sure every movie is in its own folder
* formats the name of the folder so that it is `Movie Name (Year)`

To do this, `uflix` relies on a two-step approach:

1. First, folder names are cleaned up using the fantastic `guessit` library
2. Then, `uflix` uses fuzzy text searching to search the entire IMDB database for the correct movie name. Searching is powered by the `fuzzywuzzy` package. 

## Search for movies in movies folder

```bash
uflix search "Movie Name"
```

## Mark a movie as something you would like to add

```bash
uflix add "Movie Name (Year)"
```

This creates an empty folder in your `movies_path` ready for your movie once you get it. 

## List all missing movies

```bash
uflix list
```

# Installation

# Configuration

# License

`uflix` is free software. 