#include <stdio.h>
#include <stdlib.h>
#include <cs50.h>

int main(int argc, char *argv[])
{
    //accepting only one command line argument
    if (argc != 2)
    {
        fprintf(stderr, "Usage: ./recover filename\n");
        return 1;
    }
    //opening card.raw programmatically
    FILE *file = fopen(argv[1], "r");
    
    //if forensic image cannot be opened for reading
    if (file == NULL)
    {
        fprintf(stderr, "Could not open file %s , file name should be card.raw.\n", argv[1]);
        return 2;
    }
    
    //creating buffer of size 512
    unsigned char buffer[512];
    
    //filename array
    char filename[8];
    
    //file count
    int counter = 0;
    
    FILE *pic = NULL;
    //whether a picture is detected (default to no aka false)
    int pic_detected = false;
    
    //reading 512 bytes into a buffer
    while (fread(buffer, 512, 1, file) == 1)
    {
        //checking for jpeg headers
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xf0) == 0xe0)
        {
            //close previous image 
            if (pic_detected == true)
            {
                fclose(pic);
            }
            else
            {
                pic_detected = true;
            }
            sprintf(filename, "%03i.jpg", counter);
            
            //writing picture into file
            pic = fopen(filename, "w");
            counter++;
        }
        
        if (pic_detected == true)
        {
            fwrite(&buffer, 512, 1, pic);
        }
    }
    //Close all opened files
    fclose(file);
    fclose(pic);
    
    return 0;
}
