#include <stdio.h>
#include <stdbool.h>
#include <string.h>
#include <ctype.h>
#include "dictionary.h"
#include <stdlib.h>
#include <cs50.h>

typedef struct node
{
    int data;
    struct node *next;
}
node;

int main(void)
{
    int counter = 0;
    
    node *head = NULL;
    head = malloc(sizeof(node));
    node *current = head;
    
    printf("Please give me 5 numbers\n");
    while (counter < 5)
    {
        current->data = get_int();    
        current->next = malloc(sizeof(node));
        current = current->next;
        counter++;
    }
    current->next = NULL;
    current = head;
    
    while (current != NULL)
    {
        printf("%d\n", current->data);
        current = current->next;

    }
    
    
    
    
    
    
}