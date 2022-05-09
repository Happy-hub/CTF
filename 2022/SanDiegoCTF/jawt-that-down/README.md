# JaWT That Down

## Challenge Description
> The new ultra maximum security plugin I installed on my website is so good that even I can’t log in. Hackers don’t stand a chance.

## Solution
I saw that there was a login dashboard and that it required a username and a password.
So I tried to insert a "'" and a couple others to see if it breaks something - it did not.

After realizing it wasn't a SQLi, I tried to look at the script that is being loaded on the login screen /js/login.js.

