# Ghost

### About

An implementation of the word game *Ghost* as a Django app.

### How to play

Select a letter. The computer will then select a letter and add it to the right of yours. You can then choose another letter and add it to the right side of the word. In this fashion, you take turns constructing a word.

The first player to create a full English word that is 4 characters or longer, or the first player to create a sequence of letters that *cannot* be continued into a proper English word loses.

### Demo

Available at: [https://www.danliberatori.com/projects/ghost](https://www.danliberatori.com/projects/ghost)

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

__Playing the game:__

Once the server has been booted up, you can use the sample front-end website to see the game in action. Open `http://localhost:8000/` in your browser to play.


### References

- [Ghost on Wikipedia](https://en.wikipedia.org/wiki/Ghost_(game))
- [Word list reference](https://en.wiktionary.org/wiki/Wiktionary:Frequency_lists/PG/2006/04/1-10000)
- [Word list definitions](https://github.com/matthewreagan/WebstersEnglishDictionary)