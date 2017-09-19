# Man in the middle

Python library implementing a network proxy with the ability to modify stream data.

This library was developed for the [poodle-challenge](https://github.com/alvarogzp/poodle-challenge) daemon. It was initially embedded into the daemon, and was later extracted due to its great potential to be used independently on other projects.

### Structure

The library is in the `mitm/` dir.

In `main.py` you can find a simple command-line tool that uses the library.
