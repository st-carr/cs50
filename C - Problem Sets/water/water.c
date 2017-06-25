#include <stdio.h>
#include <cs50.h>

int main(void)
{
    printf("How long was your shower?");
    int minutes = get_int();
    int bottles = minutes * 12;
    printf("%d", bottles);
    
}