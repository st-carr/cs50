#include <stdio.h>
#include <cs50.h>
#include <string.h>
#include <ctype.h>

int main(int argc, string argv[]){
    
    if (argc != 2){
        printf("Please enter ONE keyword\n");
        return 1;
    }
    for (int j = 0, n = strlen(argv[1]); j < n; j++){
        if (!isalpha(argv[1][j])){
            printf("Enter ONLY letters\n");
            return 1;
        }
     
    }
    
    printf("plaintext:");
    string p = get_string();
    int t = strlen(p);
    int tempAlpha, upperTemp, lowerTemp;
    string k = argv[1];
    int m = 0;
    char cipherText[t+1];
    
    for (int x = 0; x < t; x++){
        if (isalpha(p[x])){
            if (m == strlen(k)){
                m = 0;
            }
            int push = (int)tolower(k[m]) - 97;
            lowerTemp = (int)p[x] - 97;
            upperTemp = (int)p[x] - 65;
            if (islower(p[x])){
                tempAlpha = (lowerTemp + push) % 26;
                tempAlpha += 97;
            }
            else if (isupper(p[x])){
                tempAlpha = (upperTemp + push) % 26;
                tempAlpha += 65;
            }
            cipherText[x] = (char)tempAlpha;
            m++;
        }
        else{
            cipherText[x] = p[x];
        }
    
    }
        
    cipherText[t] = '\0';
    printf("ciphertext:%s\n", cipherText);
    return 0;
}