// All Credit for this hash function goes to D Bernstein

/**
 * Implements a dictionary's functionality.
 */
#include <stdio.h>
#include <stdbool.h>
#include <strings.h>
#include <string.h>
#include <ctype.h>
#include "dictionary.h"
#include <stdlib.h>
#include <math.h>

typedef struct node
{
    char *data;
    struct node *next;
}
node;
node *head = NULL;
struct node *listArray[500000] = {NULL};

/**
 * Returns true if word is in dictionary else false.
 */
bool check(const char *word)
{
    char lWord[LENGTH+1];
    int l = strlen(word);
    for (int i = 0; i < l; i++)
    {
        lWord[i] = tolower(word[i]);
        lWord[l] = '\0';
    }
    int hashNum = abs(hash_function(lWord) % 500000);
    node *cursor = listArray[hashNum];
    while (cursor != NULL)
    {
        if (cursor->data != NULL){
            if (strcasecmp(cursor->data, lWord) == 0)
            {
                return true;
            }
        }
        cursor = cursor->next;
    }
    
    return false;
}

/**
 * Loads dictionary into memory. Returns true if successful else false.
 */
bool load(const char *dictionary)
{

    int hashNum;
    node *newNode = NULL;
    //node *current = head;
   
    
    FILE *dp = fopen(dictionary, "r");
    if (dp == NULL)
    {
        printf("Could not open %s.\n", dictionary);
        return false;
    }
    
    int index = 0;
    char dWord[LENGTH+1];

    // spell-check each word in text
    for (int c = fgetc(dp); c != EOF; c = fgetc(dp))
    {
        // allow only alphabetical characters and apostrophes
        if (isalpha(c) || (c == '\'' && index > 0))
        {
            // append character to word
            dWord[index] = tolower(c);
            index++;
        }
        // we must have found a whole word, because word ended and wasn't entered.
        else if (index > 0)
        {
            // terminate current word
            dWord[index] = '\0';

            hashNum = abs(hash_function(dWord) % 500000);
      
            //Start new linked list, 
            if (head == NULL)
            {
                head = malloc(sizeof(node));
            }
            //Add onto exisiting linked list
            newNode = malloc(sizeof(node));
            newNode->data = malloc(sizeof(char)*LENGTH);
            strcpy(newNode->data, dWord);
            newNode->next = head;
            head = newNode;    
            
            if (listArray[hashNum] == NULL)
            {
                listArray[hashNum] = malloc(sizeof(node));
            }
            
            listArray[hashNum] = head;


            // prepare for next word
            index = 0;
        }
    }


    fclose(dp);
    return true;
}

/**
 * Returns number of words in dictionary if loaded else 0 if not yet loaded.
 */
unsigned int size(void)
{
    int n = 0;
    node *cursor = head;
    while (cursor != NULL)
    {
        if (cursor->data != NULL){
            n++;
        }
        cursor = cursor->next;
    }

    return n;
}

/**
 * Unloads dictionary from memory. Returns true if successful else false.
 */
bool unload(void)
{
    node *cursor = head;
    while (cursor != NULL)
    {
        node *temp = cursor;
        cursor = cursor -> next;
        free(temp);
    }
    return true;
}



int hash_function(const char* word)
{
    unsigned int hash = 0;
    for (int i = 0, n = strlen(word); i < n; i++)
        hash = (hash << 2) ^ word[i];
    return hash;
}