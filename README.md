# Welcome to Escape Game!

## Goal
The goal of this game is to collect all the keys, which are represented by lowercase letters ('a' to 'z'). To progress through the game, you may encounter locks represented by uppercase letters ('A' to 'Z'). For example, 'a' can open 'A'.

## Getting Started
To run the game, follow these steps:

1. **Clone the repository:**
```
git clone <repository_url>
cd <repository_directory>
```

2. **Setup Virtual Environment (optional but recommended):**
If you prefer to use a virtual environment (recommended):

To create a virtual environment using pipenv, you can follow these steps:

* Install pipenv:
  If you haven't already installed pipenv, you can do so using pip (Python's package installer):

* Navigate to Your Project Directory:
  Open a terminal or command prompt and change to the directory where your project is located:
  ```
  cd /path/to/your/project
  ```
* Create a Virtual Environment:
  Use pipenv to create a new virtual environment for your project:
  ```
  pipenv --python 3.8   # Replace 3.8 with your preferred Python version if necessary
  ```
  This command will create a new virtual environment inside your project directory. It will also create a Pipfile which will manage your dependencies.

* Activate the Virtual Environment:
  Once the virtual environment is created, you need to activate it:
  ```
  pipenv shell
  ```
  After running this command, your command prompt should change to indicate that you are now working within the virtual environment.

* Install Dependencies:
  While inside the virtual environment, install the dependencies specified in your Pipfile:
  ```
  pipenv install
  ```
  This command will install all the necessary packages listed in Pipfile.

3. **Run Your Game:**
Now you can run your game as usual. Your project has a main.py file, you can execute it:
```
python main.py
```

4. **Enjoy the Game!**
Have fun exploring and solving puzzles in the escape game!

Good luck and happy escaping!

Note: **Exit the Virtual Environment:**
When you're done playing and want to exit the virtual environment, you can use the exit command:
```
exit
```
This will deactivate the virtual environment and return you to your normal command prompt.
