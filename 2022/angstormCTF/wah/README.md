# WAH - Pwn

## Challenge description
> Baby friendly!

Source code:
```C
#include <stdio.h>
#include <stdlib.h>

void flag(){
    char flag[128];
    
    FILE *file = fopen("flag.txt","r");
    if (!file) {
        puts("Error: missing flag.txt.");
        exit(1);
    }

    fgets(flag, 128, file);
    puts(flag);
}


int main(){
    setbuf(stdout, NULL);
    gid_t gid = getegid();
    setresgid(gid, gid, gid);
    
    char cry[24];

    printf("Cry: ");

    gets(cry);
    return 0;
}
```
## Solution
We need to find a way to call the flag function, so I opened the file in gdb and noted the address of the function
