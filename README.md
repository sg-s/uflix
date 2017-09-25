# uflix


![image](images/header.png)

uflix is a set of tools to help you organise and view your home library of videos, movies and TV shows.

## Usage 

Make sure that every file is in a folder in your movies folder:

```
uflix put-in-folder
```

Clean up names, removing unnecesary cruft and rename folders to match this format: `Movie Name (Year)` 

```
uflix rename 
```

Use IMDB to figure out what the correct name for your horribly named folders are

```
uflix ask-imdb
```


Clean up your folder of movies, arranging them by name, putting "naked" video files into folders, and renaming folders in this format: `Movie Name (Year)`, and use IMDB to guess names:

```
uflix organise 
# This is equivalent to 
uflix put-in-folder
uflix rename
uflix ask-imdb
```


Don't actually do anything, but show what `uflix` would do:

```
uflix organise --dryrun
```

Clean up temporary files that `uflix` creates:

```
uflix cleanup
```

Download movie posters from IMDB and (macOS only) change the folder icon to be that of the movie poster. 

```
uflix get-posters
```
Check that your `config.txt` has reasonable values and looks good:

```
uflix check-config
```



## Dependencies 

1. python3 
2. 

## Installation 




## License 

## Roadmap

1. Test a script that coverts a .avi into a HTML5-supported .mp4 video
2. Build a script that finds and converts all video files in a folder
2. Build a script that builds webapges in each folder for each file
3. Build a script that builds the master webpage
4. Wrap up: setting up the server. 