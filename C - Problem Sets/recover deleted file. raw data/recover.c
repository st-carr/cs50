#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <inttypes.h>
typedef uint8_t  BYTE;

int main(int argc, char *argv[])
{
    // ensure proper usage
    if (argc != 2)
    {
        fprintf(stderr, "Usage: ./copy infile\n");
        return 1;
    }
    
    char *infile = argv[1];

    // open input file 
    FILE *file = fopen(infile, "r");
    if (file == NULL)
    {
        fprintf(stderr, "Could not open %s.\n", infile);
        return 2;
    }
    

    BYTE buffer[512];

    int onJpeg = 0;
    char * output;
    output = malloc(10 * sizeof(char));
    int counter = 0;
    char * jpeg = ".jpg";
    int size, number;
    FILE *outptr;

    while (!feof(file))
    {

        //check to see if able to read a full 512 byte block 
        if (fread(&buffer, 512, 1, file) == 1)
        {
            //save size and number for output
            size = 512;
            number = 1;
        }
        //if can't read 512, then see if the number able to read is less than 512 (partial last block)
        else if (fread(&buffer, 512, 1, file) < 512)
        {
            //save size and number for output
            size = 1;
            number = fread(&buffer, 512, 1, file);
        }
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xf0) == 0xe0)
        {
            //is this the very first jpeg?
            if (counter > 0)
            {
                //close previous file then open new ones
                fclose(outptr);
                //gives correct three digit filename
                if (counter > 0 && counter < 10)
                {
                    sprintf(output, "00%d%s", counter, jpeg);
                }
                else if (counter >= 10)
                {
                    sprintf(output, "0%d%s", counter, jpeg);                    
                }
                
                
                outptr = fopen(output, "w");
                if (outptr == NULL)
                {
                    fprintf(stderr, "Could not create %s.\n", output);
                    return 3;
                }
                counter++;
            }
            else
            {
                //start first jpg
                sprintf(output, "00%d%s", counter, jpeg);
                outptr = fopen(output, "w");
                if (outptr == NULL)
                {
                    fprintf(stderr, "Could not create %s.\n", output);
                    return 3;
                }
                //jpeg found
                onJpeg = 1;
                //counts through each jpg found
                counter++;
            }
            
        }
        //are we currently reading a jpg? if yes then write the current block, if no, then continue searching for jpg start
        if (onJpeg == 1)
        {
            fwrite(&buffer, size, number, outptr);

        }
        else if (onJpeg == 0)
        {
            continue;
        }

    }
    fclose(file);

    free(output);
}