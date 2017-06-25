/**
 * Copies a BMP piece by piece, just because.
 */
       
#include <stdio.h>
#include <stdlib.h>

#include "bmp.h"

int main(int argc, char *argv[])
{
    // ensure proper usage
    if (argc != 4)
    {
        fprintf(stderr, "Usage: ./copy size infile outfile\n");
        return 1;
    }
    //amount to increase or decrease
    int i = atoi(argv[1]);
    
    if (i > 100){
        fprintf(stderr, "Usage: size must be less than or equal to 100.\n");
        return 1;        
    }
    
    
    
    // remember filenames
    char *infile = argv[2];
    char *outfile = argv[3];

    // open input file 
    FILE *inptr = fopen(infile, "r");
    if (inptr == NULL)
    {
        fprintf(stderr, "Could not open %s.\n", infile);
        return 2;
    }

    // open output file
    FILE *outptr = fopen(outfile, "w");
    if (outptr == NULL)
    {
        fclose(inptr);
        fprintf(stderr, "Could not create %s.\n", outfile);
        return 3;
    }

    // read infile's BITMAPFILEHEADER
    BITMAPFILEHEADER bf;

    fread(&bf, sizeof(BITMAPFILEHEADER), 1, inptr);

    // read infile's BITMAPINFOHEADER
    BITMAPINFOHEADER bi;

    fread(&bi, sizeof(BITMAPINFOHEADER), 1, inptr);

    // ensure infile is (likely) a 24-bit uncompressed BMP 4.0
    if (bf.bfType != 0x4d42 || bf.bfOffBits != 54 || bi.biSize != 40 || 
        bi.biBitCount != 24 || bi.biCompression != 0)
    {
        fclose(outptr);
        fclose(inptr);
        fprintf(stderr, "Unsupported file format.\n");
        return 4;
    }
    
    int oldPadding = (4 - (bi.biWidth * sizeof(RGBTRIPLE)) % 4) % 4;
    int oldbiHeight = bi.biHeight;
    int oldbiWidth = bi.biWidth;
    
    
    bi.biWidth *= i;
    bi.biHeight *= i;

    
    // determine padding for scanlines
    int newPadding = (4 - (bi.biWidth * sizeof(RGBTRIPLE)) % 4) % 4;
    
    bi.biSizeImage = ((sizeof(RGBTRIPLE) * bi.biWidth) + newPadding) * abs(bi.biHeight);
    bf.bfSize = bi.biSizeImage + sizeof(BITMAPFILEHEADER) + sizeof(BITMAPINFOHEADER);
    
    
    

    // write outfile's BITMAPFILEHEADER
    fwrite(&bf, sizeof(BITMAPFILEHEADER), 1, outptr);

    // write outfile's BITMAPINFOHEADER
    fwrite(&bi, sizeof(BITMAPINFOHEADER), 1, outptr);

    int negWidth = ((oldbiWidth*3) * -1);
    
    // iterate over infile's scanlines
    for (int t = 0, biHeight = abs(oldbiHeight); t < biHeight; t++)
    {
        
        // for n-1 times - printing extra verticle rows
        for (int c = 0; c < i-1; c++)
        {
        
            // iterate over pixels in scanline
            for (int j = 0; j < oldbiWidth; j++)
            {
                // temporary storage
                RGBTRIPLE triple;
                // read RGB triple from infile
                fread(&triple, sizeof(RGBTRIPLE), 1, inptr);
    
                //write each pixel i times
                for (int m = 0; m < i; m++)
                {
                    // write RGB triple to outfile
                    fwrite(&triple, sizeof(RGBTRIPLE), 1, outptr);
                }    
                
            }
        
            // add outfile padding for each new row
            for (int k = 0; k < newPadding; k++)
            {
                fputc(0x00, outptr);
            } 
            
     
            // skip back to start of line by negative bi.biWidth
            fseek(inptr, negWidth, SEEK_CUR);       
 
        }    
        
        // iterate over pixels in scanline
        for (int r = 0; r < oldbiWidth; r++)
        {
            // temporary storage
            RGBTRIPLE triple;
            // read RGB triple from infile
            fread(&triple, sizeof(RGBTRIPLE), 1, inptr);
        
        
            //write each pixel i times
            for (int m = 0; m < i; m++){
                // write RGB triple to outfile
                fwrite(&triple, sizeof(RGBTRIPLE), 1, outptr);
            }    



        }
        // add outfile padding for each new row
        for (int w = 0; w < newPadding; w++)
        {
            fputc(0x00, outptr);
        } 
        
        // skip over infile padding, if any
        fseek(inptr, oldPadding, SEEK_CUR);
        
    }

    // close infile
    fclose(inptr);

    // close outfile
    fclose(outptr);

    // success
    return 0;
}
