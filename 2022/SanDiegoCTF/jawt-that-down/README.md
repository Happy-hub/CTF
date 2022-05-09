# JaWT That Down

## Challenge Description
> The new ultra maximum security plugin I installed on my website is so good that even I can’t log in. Hackers don’t stand a chance.

## Solution
I saw that there was a login dashboard and that it required a username and a password.
So I tried to insert a ```'``` and a couple others to see if it breaks something - it did not.

After realizing it wasn't a SQLi, I tried to look at the script that is being loaded on the login screen /js/login.js.
It was minified and most of it wasn't important, I searched for the keyword "username" to see where the credentials are being passed,
and I saw that the developer left the credentials in the script:

![image](https://user-images.githubusercontent.com/54234250/167389421-0869bd99-0435-499f-8f3d-7aab0d889eaf.png)

After I logged in, a new tab showed up called "Flag", I pressed it and got ```Invalid Token: Access Denied```,
my initial thought was to look at the cookie because it said ```Invalid Token``` which maybe referred to the token in the cookie:

![image](https://user-images.githubusercontent.com/54234250/167390289-2e296c73-1ce9-4bd1-b2f0-52fabd25f2f8.png)

It is base64 encoded, and I recognize that is it a ```JWT``` token - fits to the title of the challenge.

![image](https://user-images.githubusercontent.com/54234250/167390689-969da869-86d2-4e4e-b55a-36e603c5a58e.png)

We see that the token expires after 2 seconds because of the ```exp``` field.
So I figured that we need a script to access that directory in time
