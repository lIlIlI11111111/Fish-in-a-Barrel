# Fish in a Barrel
This is a raffle running program made by l|l|l| specifically for use with stream giveaways. It is an upgrade on the previous Raffler project, this time made with PyQt6 for an actual graphical user interface.

It also ships with an optional **browser extension** for [piczel.tv](https://piczel.tv) that loads your live viewer list directly into the app and neutralizes viewers who share an IP (i.e. are likely gaming the raffle). See [Browser Extension (piczel.tv)](#browser-extension-piczeltv).

## Table of Contents
- [Installation](#installation)
- [Usage](#usage)
- [Browser Extension (piczel.tv)](#browser-extension-piczeltv)
- [Features](#features)
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
   - Run the setup batch file by double-clicking the `setup.bat` file.
   - If it pops up that the an unknown program is running and Windows wants to stop it, click "more info" inside the text (it's kind of hidden), and then "run anyway." This message may appear once for `setup.bat` and `run.bat`, but then they will be recognized and stop giving these warnings.

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

There are two ways to get your viewer list into the app:

- **With the browser extension (piczel.tv):** put your stream URL in the "Your Stream URL" field, open your stream's watch page in your browser, and click **Load from site (extension)** (or just run the Default Procedure). The app pulls the current viewer list straight from the page, including shared-IP information. See [Browser Extension (piczel.tv)](#browser-extension-piczeltv).
- **Manually (any site):** copy-paste your viewer list into the "Names go here" field and click the **Load** button under it. This always works as a fallback and needs no extension.

For day-to-day usage with the extension: open the program, make sure your stream page is open in the browser, press **Ctrl+Shift+Enter** (Default Procedure), Reject winners until one shows up, Accept the winner who shows up, then Save and Exit.

For manual usage: open the program, copy-paste your viewer list into the "Names go here" field, run Default Procedure, and proceed the same way.

### Hotkeys
These work from anywhere in the app, regardless of which field is focused:

| Hotkey | Action |
| --- | --- |
| `Ctrl+Shift+Enter` | Default Procedure (load viewers + roll) |
| `Ctrl+S` | Save data to the data file |
| `Ctrl+L` | Load the names in the "Names go here" field |
| `Ctrl+W` / `Ctrl+Q` | Exit (prompts to save first) |

## Browser Extension (piczel.tv)

piczel.tv shows a per-viewer **shared-IP indicator** (a small 2-character badge) that is only visible to the logged-in streamer. Fish-in-a-Barrel can read this so that viewers sharing an IP can't multiply their raffle entries: when a group of viewers shares an IP, only **one** of them (chosen at random) is counted as active for the round. This grouping is kept internal — it is never shown in the table or written to disk, so viewers watching your screen can't tell detection is happening.

Because that indicator is behind your login and the page is rendered by JavaScript, the app can't read it on its own; a small paired browser extension scrapes it from your live page and hands it to the app over a local (localhost) connection. Everything stays on your machine.

### Installing the extension

The extension lives in the `extension/` folder of this repository. It works in both Chrome-family browsers and Firefox.

**Chrome / Edge / Brave**
1. Go to `chrome://extensions`.
2. Turn on **Developer mode** (top-right).
3. Click **Load unpacked** and select the `extension/` folder.

**Firefox**
1. Go to `about:debugging#/runtime/this-firefox`.
2. Click **Load Temporary Add-on…**.
3. Select `extension/manifest.json`. (Temporary add-ons are removed when Firefox restarts, so you'll re-add it next session.)

The app and the extension talk over port `8422` by default. If you need to change it, edit `[extension] port` in `config.ini` **and** the `BASE` port near the top of `extension/background.js` so they match.

### Using the extension

1. Start Fish-in-a-Barrel (`run.sh` / `run.bat`). It prints `Extension bridge listening on http://127.0.0.1:8422`.
2. Open your stream's watch page (e.g. `https://piczel.tv/watch/YourName`) in the browser where the extension is installed.
3. Put that same URL in the app's "Your Stream URL" field.
4. Click **Load from site (extension)** (or press **Ctrl+Shift+Enter** for the full Default Procedure).

The viewer list loads automatically. You may see the page's user-list panel briefly flicker open — that's the extension reading the current viewers. Banned users are skipped, your own name is blacklisted automatically, and one viewer per shared-IP group is entered.

If the extension doesn't respond within ~2 seconds (not installed, app not running, or the stream page isn't open), the app tells you to paste the list manually instead — nothing is loaded automatically. The manual copy-paste flow always remains available.

For troubleshooting tips, see `extension/README.md`.


## Features

- ### Loading
	The Loading area has three parts.
   First, there is the **stream URL** field. Put the URL of your stream here. The **Load from site (extension)** button next to it adds your own name to the blacklist (so you don't get entered into your own raffle) and, if the [browser extension](#browser-extension-piczeltv) is installed and your stream page is open, pulls the current viewer list — including shared-IP grouping — straight from the page.
   Then, there is the **name field** ("Names go here"). Copy and paste the names of the viewers you would like to enter into the raffle here, then hit the **Load** button below it. This is the manual fallback and works for any site. Don't worry if your own name is in the list — anything in the blacklist is ignored.
   Finally, there is the **blacklist** field for names that should always be excluded.

- ### Functions
	There are only 3 buttons that I would ever use here: Default Procedure, Save, and Exit. Everything besides Default Procedure is self-explanatory. Default Procedure will save the stream name and blacklist yourself, try to load the current viewers from the site via the extension (falling back to the "Names go here" field if the extension doesn't answer), perform a reset round only if necessary, give all attending people one more ticket, and initiate a roll. It is very useful, as it does everything one would want in the order they want it done in. It is also bound to `Ctrl+Shift+Enter`.

- ### Rolling
	Once a roll has started, you can choose one of three options: Accept, Reject, or Cancel. Accept will select the displayed user as the winner, taking all of their tickets and putting them on cooldown. Rejecting is useful if the person doesn't show up. They do not win, they keep their tickets, and they are not put on cooldown, and a new winner will be rolled again. Cancel is just like Reject, only it does not roll again.

- ### Viewing Table
	This doesn't have a practical use, but it can be a nice way to visualize who has how many tickets, who is on cooldown, or other data you may want.

## Contributing
If you would like to contribute, just ask me first. There's plenty of features yet to be implemented, and if you want to help, I'd be happy to share the list. If you have feature requests, you can submit an issue or contact me directly as well. Also, if you can translate or document code, that would also be helpful.

## License
See LICENSE.txt (Spoiler it's GNU)
