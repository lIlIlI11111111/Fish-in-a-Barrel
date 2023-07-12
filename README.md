# Fish in a Barrel
This is a raffle running program made by l|l|l| specifically for use with stream giveaways. It is an upgrade on the previous Raffler project, this time made with PyQt5 for an actual graphical user interface.

## Table of Contents
- [Installation](#installation)
- [Usage](#usage)
- [Features](#license)
- [Contributing](#contributing)
- [License](#license)
## Installation

### Detailed Windows Guide
1. **Python Installation**:
   - Download the latest version of Python from the official Python website (https://www.python.org/downloads/windows/).
   - Run the downloaded installer.
   - Select the option to "Add Python to PATH" during the installation process.
   - Click "Install Now" to begin the installation.
Once the installation is complete, open a new command prompt and type python --version to verify that Python is installed correctly.

2. **Repository Download**:
   - Go to this project's GitHub repository [here](https://github.com/lIlIlI11111111/Fish-in-a-Barrel)
   - Click on the green "Code" button and select "Download ZIP" to download the repository as a ZIP file.
   - Extract the ZIP file to a convenient location on your computer.

3. **Setup**:
   - Open a command prompt or PowerShell window.
   - Open a command prompt by pressing the Windows key, then typing "cmd" or "powershell" without the quotes and hitting Enter. Copy the path of the folder from the address bar at the top of the File Explorer window. For example, if the path is `C:\Users\YourName\repository`, copy that path.
   - Go back to the command prompt or PowerShell window and type cd followed by a space. For example, if the path you copied is `C:\Users\YourName\repository`, type: `cd C:\Users\YourName\repository`
Press Enter to execute the command.
   - Navigate to the extracted repository folder. First find where you placed it with File Explorer.
   - Run the setup batch file by typing `setup.bat` and pressing Enter.

### Linux

1. **Python Installation**:
   - Python usually comes pre-installed on most Linux distributions. You can check if Python is already installed by running `python --version` in a terminal.
   - If Python is not installed, you can install it using your package manager. For example, on Ubuntu, you can run `sudo apt-get install python3` to install Python 3.

2. **Repository Download**:
   - Open a terminal and navigate to the directory where you want to download the repository.
   - Clone the repository using the command `git clone https://github.com/your-username/your-repository`.

3. **Setup**:
   - Open a terminal and navigate to the cloned repository folder.
   - Run the setup script by typing `./setup.sh` and pressing Enter.



## Usage
When you want to run the program, double click the run.bat or run.sh file to launch the program. There are 4 main sections you will see: Loading, Functions, Rolling, and the viewing table.

For day-to-day usage, open the program, copy-paste your viewer list into the "Names go here" field, select "Default Procedure", Reject winners until one shows up, Accept the winner who shows up, and Save and Exit the program.


## Features

- ### Loading
	There are 3 main features of the Loading area. 
   First, there is the stream name. You can place the URL of your stream in the field. When you press the associated load button (to the right), it will load your name into the blacklist so you don't get entered into your own raffle.
   Then, there is the name field. Copy and paste the names of the viewers you would like to enter into the raffle here. Don't worry about if your own name is in the list, since any items in the blacklist will be ignored. Finally, you can hit the "Load" button below to load all of the attendees into the system, which you can see in the viewing table.

- ### Functions
	There are only 3 buttons that I would ever use here: Default Procedure, Save, and Exit. Everything besides Default Procedure is self-explanatory. Default procedure will first load the stream name into the blacklist field, load the names in the "Names go here" field into the table, perform a reset round only if necessary, give all people who are attending one more ticket, and initiate a roll. It is very useful, as it does everything one would want in the order they want it done in.

- ### Rolling
	Once a roll has started, you can choose one of three options: Accept, Reject, or Cancel. Accept will select the displayed user as the winner, taking all of their tickets and putting them on cooldown. Rejecting is useful if the person doesn't show up. They do not win, they keep their tickets, and they are not put on cooldown, and a new winner will be rolled again. Cancel is just like Reject, only it does not roll again.

- ### Viewing Table
	This doesn't have a practical use, but it can be a nice way to visualize who has how many tickets, who is on cooldown, or other data you may want.

## Contributing
If you would like to contribute, just ask me first. There's plenty of features yet to be implemented, and if you want to help, I'd be happy to share the list. If you have feature requests, you can submit an issue or contact me directly as well. Also, if you can translate or document code, that would also be helpful.

## License
See LICENSE.txt (Spoiler it's GNU)
