# Ghost

### About

An API endpoint built with Django for playing the word game *Ghost*.

### How to play

Select a letter. The computer will then select a letter and add it to the right of yours. You can then choose another letter and add it to the right side of the word. In this fashion, you take turns constructing a word.

The first player to create a full English word that is 4 characters or longer, or the first player to create a sequence of letters that *cannot* be continued into a proper English word loses.

### Demo

Available at: [http://www.danliberatori.com/projects/ghost](http://www.danliberatori.com/projects/ghost)

### Getting started

__Booting the server (Docker):__

The server can be started with the following Docker command:

```
$ docker-compose up
```

__Booting the server (Standalone):__

If you are not using Docker, you will need to make sure that you are using Python 3 or later and that all dependecies are installed.

*Check your Python version:*

```
$ python --version
```

If that shows an older version of Python, you can also check if Python 3 is installed under the command `python3`. If this is the case, you will need to substitute `python3` for `python`, and possibly `pip3` for `pip` in the commands below.

```
$ python3 --version
```

*Install dependencies:*

```
$ pip install -r requirements.txt
```

*Launch the server on port 8000:*

```
$ python manage.py runserver 0.0.0.0:8000
```


You can then use the sample front-end website to see the game in action. Open `/ui/index.html` in your browser to play.


__Changing dictionaries:__

New dictionaries can easily be imported if they are in JSON format. Simply modify the `/game/assets/build_wordlist.py` file to point to your new dictionary, and modify `/game/asset_loader.py` to match whatever you choose to name your output files. This can be done, for example, to quickly and easily port the game to a different language (Note: This implementation has been developed with ASCII characters in mind and likely will not work properly outside of the simple a-z ASCII characters).


### Winning plays

I have not taken the time to solve the game using the current dictionary. Here is a non-exhaustive list of potential winning sequences.

- J: "jairou", "juke"


### References

- [Ghost on Wikipedia](https://en.wikipedia.org/wiki/Ghost_(game))
- [The dictionary used in this implementation](https://github.com/matthewreagan/WebstersEnglishDictionary)