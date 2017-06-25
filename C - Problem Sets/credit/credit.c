#include <stdio.h>
#include <cs50.h>

int main(void)
{
    long long ccLong, tempLong0, tempLong1, tempLongAmex, tempLongVisa, tempLongMC;
    int intCalc = 0;
    int anotherTemp;
    bool algLuhn;
    long long amexCheck, visaCheck, mcCheck;
    printf("Enter your Credit Card number:\n");
    ccLong = get_long_long();
    tempLongMC = tempLongVisa = tempLongAmex = tempLong0 = tempLong1 = ccLong;
    
    while(tempLong0>10){
        tempLong0 /= 10;
        if(((tempLong0 % 10)*2) > 9){
            anotherTemp = (tempLong0 % 10)*2;
            while(anotherTemp){
                intCalc += anotherTemp % 10;
                anotherTemp /= 10;
            }
        }
        else{
            intCalc += (tempLong0 % 10)*2;        
        }
        tempLong0 /= 10;
    }

    while(tempLong1){    
        intCalc += (tempLong1 % 10);
        tempLong1 /= 10;
        tempLong1 /= 10;
    }

    //printf("%d\n", intCalc);        
    if(intCalc % 10 == 0){
        algLuhn = true;
    }
    else{
        algLuhn = false;
    }
    
    if(algLuhn == true){
        tempLongAmex /= 10;
        while(tempLongAmex){
            amexCheck = tempLongAmex % 100;
            tempLongAmex /= 100;
        }
        if(amexCheck == 34 || amexCheck == 37){
            printf("AMEX\n");
        }

        while(tempLongMC){
            mcCheck = tempLongMC % 100;
            tempLongMC /= 100;
        }
        if(mcCheck == 51 || mcCheck == 52|| mcCheck == 53|| mcCheck == 54|| mcCheck == 55){
            printf("MASTERCARD\n");
        }

        
        
        while(tempLongVisa){
            visaCheck = tempLongVisa % 10;
            tempLongVisa /= 10;
        }
        if(visaCheck == 4){
            printf("VISA\n");
        }
    }
    else{
        printf("INVALID\n");           
    }
}