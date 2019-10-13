# Ghost

### About

An API endpoint built with Django for playing the word game *Ghost*.

### How to play

Select a letter. The computer will then select a letter and add it to the right of yours. You can then choose another letter and add it to the right side of the word. In this fashion, you take turns constructing a word.

The first player to create a full English word that is 4 characters or longer, or the first player to create a sequence of letters that *cannot* be continued into a proper English word loses.

### Getting started

New dictionaries can easily be imported if they are in JSON format. Simply modify the `/game/assets/build_wordlist.py` file to point to your new dictionary, and modify `/game/asset_loader.py` to match whatever you choose to name your output files. This can be done, for example, to quickly and easily port the game to a different language (Note: This implementation has been developed with ASCII characters in mind and likely will not work properly outside of the simple a-z ASCII characters).

### References

- [Ghost on Wikipedia](https://en.wikipedia.org/wiki/Ghost_(game))
- [The dictionary used in this implementation](https://github.com/matthewreagan/WebstersEnglishDictionary)