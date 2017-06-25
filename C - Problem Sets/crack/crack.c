#include <stdio.h>
#include <cs50.h>
#include <string.h>
#include <ctype.h>
#include <unistd.h>


#define _XOPEN_SOURCE       /* See feature_test_macros(7) */
char *crypt(const char *key, const char *salt);


int main(int argc, string argv[]){
    char myPassword[5];
    if (argc != 2){
        printf("Please enter ONE keyword\n");
        return 1;
    }
    string hash = argv[1];
    for (int counter = 0; counter < 4; counter ++){
    for (int a1 = 65; a1 < 123; a1++){
        for (int b1 = 65; b1 < 123; b1++){    
            for (int c1 = 65; c1 < 123; c1++){
                for (int d1 = 65; d1 < 123; d1++){   
                    myPassword[0] = (char) a1;
                    if (counter == 0) {
                        myPassword[1] = '\0';            
                    }
                    else if (counter == 1){
                        myPassword[1] = b1;
                        myPassword[2] = '\0';
                    }
                    else if (counter == 2){
                        myPassword[1] = b1;
                        myPassword[2] = c1;                
                        myPassword[3] = '\0';
                    }
                    else if (counter == 3){
                        myPassword[1] = b1;
                        myPassword[2] = c1;                
                        myPassword[3] = d1;
                        myPassword[4] = '\0';
                    }
                    if (strcmp((crypt(myPassword, "50")), hash) == 0){
                        printf("MATCH: %s\n", myPassword);
                        return 0;        
                    }
                }
            }    
        }
    }
    }  
return 0;
}