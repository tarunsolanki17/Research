#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void printstr(char* str)
{
    printf("%s\n", str);
}
int main()
{
    char str[] = "hello";
    char* ptr = (char*) malloc(10);
    strcpy(ptr, str);
    printstr(ptr);
    printf("stack: %p\n", str);
    printf("heap : %p\n", ptr);
    printf("text : %p\n", printstr);
    printf("text : %p\n", main);
    return 0;
}
