This is a mini-project called "Raffler" by l|l|l|

Description:
The raffling algorithm was based off of a design used by a streamer called Veiled616, but I unfortunately do not know the true origins of it. It is a continuously increasing weighted raffle, so the more times a person loses, the more likely they are to win, in general.

Setup:
Just compile main.c with your favorite C compiler. For example, I use `$ gcc main.c`, but if you like the executable to me named something other than a.out, or you'd like to use a different compiler, your command will change thusly. Make sure to manually prepopulate userDataList.txt before running, since it has proof-of-concept contestant names/values.

Usage:
First, replace all the text in nameInput.txt with the names of people currently attending. They MUST be in the form name1'\n'name2'\n'name3... Since this was designed specifically for easy use with Piczel viewer lists, it is very fragile to small changes in the user input.
Next, run a.out or whatever your executable name is. Technically, the nameInput.txt file isn't read until either the "Default Procedue" or "Add new members from the input file" are activated, but it is in general not recommened to have any of the files open while the program is running.
There are a number of options, which at time of writing is 9. Default procedure combines adding new members, incrementing all present members once, sorting the list, listing all the people and their statuses, and rolling the raffle, but each of these steps can be done individually. Sorting sorts by decreasing ticket number: if you'd like it to be any other way, you're welcome to do it yourself. Saving data to the data file completely overwrites the old userDataList.txt file, and it will include any new members that joined. It writes the list as presented in the command line, so do note that all changes, including sorting the list, will be saved as-is. Finally, the last option exits the program. It does not automatically save the results - IF YOU WANT TO HAVE YOUR CHANGES SAVED, YOU MUST USE THE SAVE OPTION. There is no warning for exiting without saving, so do so at your own peril.
