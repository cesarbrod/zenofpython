# zenofpython
This program translates the Zen of Python in multiple languages

## Instructions

Of course, you first need to have python3 installed on your system and I am assuming you are running on Linux.

Download the file zenofpython.py to the folder you wish, let's assume it is zenofpython. Move to the zenofpython folder.

Create a virtual environment and source it:

```
python3 -m venv venv
source ./venv/bin/activate
```

Install the dependencies

```pip install deep_translator```

**Run the program**

```python3 zenofpython [language]```

If you ommit [language], the program will prompt you with the name of the languages in a paginated format.

# How this program was created?

This program was created using Google's [Antigravity](https://antigravity.google/) IDE with the following prompt:

```
Please create a python3 program that prints the Zen of Python in a specified language,
or lists available languages for selection if none is specified at the program call.
```
