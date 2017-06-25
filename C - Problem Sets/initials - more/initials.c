#include <stdio.h>
#include <cs50.h>
#include <string.h>
#include <ctype.h>

int main(void)
{
    string s = get_string();
    int nameLen = strlen(s);
    char outPut[10];
    int count = 0;
    bool onWord = false;
    
    for (int x = 0; x < nameLen; x++){
        if ((isalpha(s[x])) && (onWord == false)){
            outPut[count] = toupper(s[x]);
            count++;    
            onWord = true;
        }
        else if (s[x] == ' '){
            onWord = false;
        }

    }
    
    printf("%s\n", outPut);
    
    
    
    
    
    
    
}