#include <stdio.h>
#include <cs50.h>

int main(void)
{
    char block = '#';
    char space  = ' ';
    int intInput;
    while(true){
        printf("Please enter a number: \n");
        intInput = get_int();
        if (intInput >= 0 && intInput <= 23){
            break;
        }
        else{
            continue;
        }
    }

    for (int x = 0; x < intInput; x++){
        
        for (int t = 1; t < (intInput - x); t++){
            printf("%c", space);
        }
        for (int y = 0; y < x + 1; y++){
            printf("%c", block);
        }
        printf("  ");
        for (int r = 0; r < x + 1; r++){
            printf("%c", block);
        }
        printf("\n");
        
        
        
    }
    

    
    
}