#include <stdio.h>
#include <stdlib.h>
#include <limits.h>
#include <string.h>

const int maxTitleLen = 1024;
const int randomPrecision = 1000;


//The input file should go as such: name,tickets,onCooldown
//New people can show up from the user input. They should be handled by setting their tickets to 1 and isIn to 1
//If the current month%2 == 0 && day/7 == 0, change isIn for all users on the first round to 1

//Structure of the person. Languages is stored like: "lang1;lang2;lang3;...;langn"
struct person{
	char* name;
	int tickets;
	int onCooldown;
	int isIn;
};

//Tests if a) the next character is EOF or if b) the character after that is EOF
int areWeDoneYet(FILE* f){
	if(feof(f))
		return 1;
	int x;
	x = fgetc(f);
	ungetc(x, f);
	if(x == EOF)
		return 1;
	return 0;
}


struct person* parsePerson(FILE* f){
	char* buffer = malloc(maxTitleLen * sizeof(char));
	struct person* newMan = malloc(sizeof(struct person));
	if(newMan == NULL){
		//If this triggers, we will have an inevitable memory leak. Very bad.
		printf("Failed to allocate new person\n"); fflush(stdout);
	}
	//
	int maxLen = INT_MAX;
	newMan->name = NULL;
	fgets(buffer, maxTitleLen, f);
	const char comma[2] = ",";
	char* token = strtok(buffer, comma);
	
	//Setting name
	newMan->name = malloc(sizeof(char) * (1 + strlen(token)));
	strcpy(newMan->name, token);
	
	//Setting tickets
	newMan->tickets = atoi(strtok(NULL, comma));
	
	//Setting onCooldown
	newMan->onCooldown = atoi(strtok(NULL, comma));
	
	//Setting isIn
	newMan->isIn = 0;
	
	free(buffer);
	
	return newMan;
}

//Frees a person and all of its contents from memory
void freePerson(struct person* m){
		free(m->name);
		free(m);
}

//Frees a list by iteratively calling freeperson and then freeing the list itself
void freeList(struct person** personList, int* personCount){
	for(int i = 0; i < *personCount; i++){
		freePerson(personList[i]);
	}
	free(personList);
}

//Big bloated mess, but loops as many times as it needs to to gather every person in the
//list. realloc is like O(nlogn), or maybe even O(n^2) in this case, so don't make too big of a list.
struct person** getData(FILE* f, int* personCount){
	//printf("Inside of getData\n"); fflush(stdout);
	*personCount = 0;
	struct person** personList = (struct person**)malloc(sizeof(struct person*));
	//printf("Successfully allocated memory for first person\n"); fflush(stdout);
	while(!areWeDoneYet(f)){
		//printf("About to parse person\n"); fflush(stdout);
		struct person* m = parsePerson(f);
		//printf("Parsed person\n"); fflush(stdout);
		personList = (struct person**)realloc(personList, (*personCount + 1) * sizeof(struct person*));
		personList[*personCount] = m;
		(*personCount)++;
	}
	return personList;
}

//Displays persons by year.
void getUserInput(struct person*** personList, int* personCount){
	FILE* UIfile;
	//printf("Inside of getUserInput\n"); fflush(stdout);
	UIfile = fopen("nameInput.txt", "r");
	if(UIfile == NULL){
		printf("No suitable input file, exiting with error code 1\n");
		exit(1);
	}
	printf("Opened the input file successfully\n"); fflush(stdout);
	
	const char slashN[2] = "\n";
	
	while(!areWeDoneYet(UIfile)){
		char* buffer = malloc(maxTitleLen * sizeof(char));
		fgets(buffer, maxTitleLen, UIfile);
		char* token = strtok(buffer, slashN);
		//printf("Searching for user with name: %s\n", token); fflush(stdout);
		int foundMatch = 0;
		for(int i = 0; i < *personCount; i++){
			//printf("Testing person: %s against %s\n", *personList[i]->name, token); fflush(stdout);
			//printf("strcmp says: %d\n", strcmp(*personList[i]->name, token)); fflush(stdout);
			if(!strcmp((*personList)[i]->name, token)){
				foundMatch = 1;
				if((*personList)[i]->onCooldown)
					break;
				(*personList)[i]->isIn = 1;
			}
		}
		if(!foundMatch){
			printf("No match found, adding new user of name: %s\n", token); fflush(stdout);
			*personList = (struct person**)realloc(*personList, (*personCount + 1) * sizeof(struct person*));
			struct person* newMan = malloc(sizeof(struct person));
			newMan->name = malloc(sizeof(char) * (1 + strlen(token)));
			printf("Successfully realloc'd new memory\n"); fflush(stdout);
			strcpy(newMan->name, token);
			printf("Added username: %s\n", newMan->name); fflush(stdout);
			newMan->tickets = 0;
			newMan->onCooldown = 0;
			newMan->isIn = 1;
			(*personList)[*personCount] = newMan;
			printf("Set new member as final element in the array\n"); fflush(stdout);
			printf("Their name in the array is: %s\n", (*personList)[*personCount]->name); fflush(stdout);
			(*personCount)++;
		}
		free(buffer);
	}
	fclose(UIfile);
}

//Displays the top rated persons for each year.
void incrementAttendees(struct person** personList, const int personCount){
	for(int i = 0; i < personCount; i++){
		if(personList[i]->isIn && !(personList[i]->onCooldown)){
			(personList[i]->tickets)++;
		}
	}
	printf("Attendees not on cooldown have been incremented\n");
}

//Displays all persons in a given language. Compares the string exactly with strcmp, so be sure to not mess up typing
int roll(struct person** personList, const int personCount){
	int totalTickets = 0;
	for(int i = 0; i < personCount; i++){
		if(personList[i]->isIn && !(personList[i]->onCooldown)){
			totalTickets += personList[i]->tickets;
		}
	}
	if(totalTickets == 0){
		printf("Error, no contestants had any tickets. Error with dividing by 0.\n");
		return -1;
	}
	int r = (rand() % totalTickets) + 1;
	int sum = 0;
	for(int i = 0; i < personCount; i++){
		if(personList[i]->isIn && !personList[i]->onCooldown){
			sum += (personList[i]->tickets);
			if(sum >= r){
				printf("With %d tickets, the winner is %s\n", personList[i]->tickets, personList[i]->name);
				return i;
			}
		}
	}
	printf("A strange error occured in which no one won. Roll again, maybe, idk?\n");
	return -1;
}

void rollWrapper(struct person** personList, const int personCount){
	int hasWinner = 0;
	while(!hasWinner){
		int winNum = roll(personList, personCount);
		printf("Did %s claim their win? (0 for no, 1 for yes, 2 for cancel))\n", personList[winNum]->name);
		scanf("%d", &hasWinner);
		if(hasWinner == 1){
			personList[winNum]->isIn = 0;
			personList[winNum]->onCooldown = 1;
			personList[winNum]->tickets = 0;
		}
	}
}

void writeFile(struct person** personList, const int personCount){
	FILE* outFile;
	outFile = fopen("userDataList.txt", "w");
	for(int i = 0; i < personCount; i++){
		fprintf(outFile, "%s,%d,%d", personList[i]->name, personList[i]->tickets, personList[i]->onCooldown);
		if(i < personCount - 1)
			fprintf(outFile, "\n");
	}
	fclose(outFile);
}

void sortList(struct person** personList, const int personCount){
	int looping = 1;
	//printf("In sortList\n");
	while(looping){
		looping = 0;
		for(int i = 0; i < personCount - 1; i++){
			//printf("Testing %s's %d tickets against %s's %d tickets\n", personList[i]->name, personList[i]->tickets, personList[i+1]->name, personList[i+1]->tickets);
			if(personList[i]->tickets < personList[i + 1]->tickets){
				looping = 1;
				struct person* temp = personList[i];
				personList[i] = personList[i+1];
				personList[i+1] = temp;
			}
		}
	}
	printf("List sorted\n");
}

void listAll(struct person** personList, const int personCount){
	printf("Name: tickets, onCooldown, isIn\n");
	for(int i = 0; i < personCount; i++){
		printf("%s: %d, %d, %d\n", personList[i]->name, personList[i]->tickets, personList[i]->onCooldown, personList[i]->isIn);
	}
}

void resetRound(struct person** personList, const int personCount){
	for(int i = 0; i < personCount; i++){
		personList[i]->onCooldown = 0;
	}
}


int main(){
	//time_t t;
	//srand((unsigned) time(&t));
	FILE* inFile;
	inFile = fopen("userDataList.txt", "r");
	if(inFile == NULL){
		printf("File cannot be opened, returning with error code 1\n");
		fflush(stdout);
		return 1;
	}
	int personCount;
	//printf("Opened file userDataList.txt\n"); fflush(stdout);
	struct person** personList = getData(inFile, &personCount);
	printf("Processed file userDataList.txt and parsed data for %d persons\n", personCount); fflush(stdout);
	fclose(inFile);
	//Closing the file as soon as we don't need it, good practice I think :)
	//printf("Here is the name of the first person: %s\n", (personList[0])->name);
	
	int chooserNum = -1;
	int cont = 1;
	while(cont){
		printf("\n1. Default procedure\n");
		printf("2. Add new members from input file\n");
		printf("3. Increment active users\n");
		printf("4. Roll active users\n");
		printf("5. Save data to data file\n");
		printf("6. List all people\n");
		printf("7. Sort the list\n");
		printf("8. Reset Round\n");
		printf("9. Exit from the program\n\n");
		printf("Enter a choice from 1 to 9: ");
		scanf("%d", &chooserNum);
		//big switch statement for the different options, very standard stuff
		switch(chooserNum){
			case 1:
				getUserInput(&personList, &personCount);
				incrementAttendees(personList, personCount);
				listAll(personList, personCount);
				rollWrapper(personList, personCount);
				break;
			case 2:
				getUserInput(&personList, &personCount);
				listAll(personList, personCount);
				break;
			case 3:
				incrementAttendees(personList, personCount);
				listAll(personList, personCount);
				break;
			case 4:
				rollWrapper(personList, personCount);
				break;
			case 5:
				writeFile(personList, personCount);
				break;
			case 6:
				listAll(personList, personCount);
				break;
			case 7:
				sortList(personList, personCount);
				listAll(personList, personCount);
				break;
			case 8:
				resetRound(personList, personCount);
				break;
			case 9:
				cont = 0;
				break;
			default:
				printf("Wrong. Try again.\n");
		}
	}
	//Obligatory hello world
	//printf("hello world\n");
	//Also obligatory orca
	//orca
	
	
	freeList(personList, &personCount);
	return 0;
}