// Implements a dictionary's functionality

#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <ctype.h>
#include <string.h>

#include "dictionary.h"

// Represents number of children for each node in a trie
#define N 27

// Represents a node in a trie
typedef struct node
{
    bool is_word;
    struct node *children[N];
}
node;

// Represents a trie
node *root;

// initialise dictionary size to 0
int dictsize = 0;

// Loads dictionary into memory, returning true if successful else false
bool load(const char *dictionary)
{
    // open dictionary file
    FILE* Dict = fopen(dictionary,"r");

    if (!Dict)
    {
        return false;
    }

    // prepare to load Dict in memory as Trie
    int index;
    char c;
    char word[LENGTH];

    root = calloc(1, sizeof(node));

    // go through each word from Dict until EOF
    while((fscanf(Dict, "%s", word)) != EOF)
    {
        // a temp node pointer same as root for every word
        node *travptr = root;

        // go over each letter in word
        for(int i = 0, n = strlen(word); i < n; i++)
        {
            // store the current letter
            c = word[i];

            // find the index equivalent of current index
            if (c == '\'')
            {
                index = 26;
            }
            else
            {
                index = c - 97;
            }
            

            // if NULL, allocate memory
            if (travptr->children[index] == NULL)
            {
                travptr->children[index] = calloc(1, sizeof(node));
            }
            
            // move travptr to the next child
            travptr = travptr->children[index];
        }
            // at the end of the word, set is_word to true
            travptr->is_word = true;

        // increase dictionary size by 1
         dictsize++;
    }
    // Close dictionary
    fclose(Dict);
    // Indicate success
    return true;
}

// size
unsigned int size(void)
{
    return dictsize;
}

// Returns true if word is in dictionary else false
bool check(const char *word)
{
    char c;
    int index;

    // a temp node pointer same as root for every word
    node *travptr = root;

    // go over each letter in given word
    for(int i = 0, n = strlen(word); i < n; i++)
    {
        // store the current letter
        c = tolower(word[i]);

        // find index equivalent of c
        if(isalpha(c))
        {
            index = c - 97;
        }
        else if (c == '\'')
        {
            index = 26;
        }

        // move pointer if node is true, else return false
        if(travptr->children[index] != NULL)
            {
                travptr = travptr->children[index];
            }
        else
            return false;
    }

        if (travptr->is_word == true)
            return true;
        else
            return false;
}

// unload dictionary
void unloadMain (node* ptr)
{
    if (ptr == NULL)
        return;
    for(int i = 0; i < N; i++)
    {
        if (ptr->children[i] != NULL)
            unloadMain(ptr->children[i]);
    }
    // free memory
    free(ptr);
}

// Unloads dictionary from memory. Returns true if successful else false.
bool unload(void)
{
    unloadMain(root);
    return true;
}