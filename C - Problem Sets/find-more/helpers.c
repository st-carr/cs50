/**
 * helpers.c
 *
 * Helper functions for Problem Set 3.
 */
 
#include <cs50.h>
#include <stdio.h>
#include <math.h>
#include "helpers.h"
const int xMAX = 65536;
int countArr[xMAX] = {0};
int tempArrIndex;
bool binSearch(int value, int values[], int start, int stop);
#define True true
#define False false
/**
 * Returns true if value is in array of n values, else false.
 */
//Variable used to escape out of recursive functions
int myTrue = 0;
bool binSearch(int value, int values[], int start, int stop){
    /*
    Gets length sub-array during each recursive loop
    finds mid-point of sub-array.
    if down to last index in subarray, check to see if target found
    checks to see if mid-point landed on target number
    if value is greater than midpoint, then make the new starting point the midpoint+1
    start function again using new start point
    if value is less than midpoint, then make the new endpoint the midpoint - 1
    start function using the new end point.
    */
    int length = stop - start;
    tempArrIndex = floor(length/2)+start;
    if (length == 1){
        if (value == values[start] || value == values[stop]){
            myTrue = 1;
        }
    }
    else if (value == values[tempArrIndex]){
        myTrue = 1;
    }
    else if (value > values[tempArrIndex]){
        start = tempArrIndex + 1;
        binSearch(value, values, start, stop);
    }
    else if (value < values[tempArrIndex]){
        stop = tempArrIndex - 1;
        binSearch(value, values, start, stop);
    }
    if (myTrue == 1){
        return true;
    }
    return false;
}

bool search(int value, int values[], int n)
{
    if (n <= 0){
        return false;
    }
    /*call resursive function*/
    return binSearch(value, values, 0, n);
}

/**
 * Counting Sorts array of n values.
 */
void sort(int values[], int n)
{
    /*
    iterate through list to sort, using a new array to tally each iteration of a value
    counts up to rewrite sorted array over old array
    */
    int tempIndex = 0;
    for (int x = 0; x < n; x++){
        tempIndex = values[x];
        countArr[tempIndex] += 1;
    }
    int tempCntUp = 0;

    /* 
    iterates over every possible value until it reaches the LIMIT
    more than one figure documented in this index
    rewrites array with the first index point that holds a number
    decreases the value in the index by one, since it has been inputted into old array
    iterates to next index in sorted array
    nullify the Y counter, since there is more than 1 value counted in the countArr
    */    
    for (int y = 0; y <= xMAX; y++){
        if (countArr[y] > 1){
            values[tempCntUp] = y;
            countArr[y]--;
            tempCntUp++;
            y--;
        }
        else if (countArr[y] > 0 && countArr[y] < 2){
            values[tempCntUp] = y; 
            countArr[y]--;
            tempCntUp++;
        }
    }
    return;
}
