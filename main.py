import requests
import regex as re
from flask import Flask , redirect , url_for, request,render_template
import json

def brute1(ahash):
	api1 = 'https://md5.gromweb.com/?md5='+ahash
	r = requests.get(api1,timeout=2,verify=False)
	if 'succesfully reversed' in r.text:
		dehash = re.findall('<em class="long-content string">(.*)<\/em>',r.text)[0]
		return dehash
	else:
		return False

def brute2(ahash):
	api2 = 'https://md5decrypt.net/en/'
	r = requests.session()
	a = r.get(api2,verify=False)
	captchaName = re.findall('<input id="captcha" type="text" name="([^"]*)',a.text)[0]
	temp = re.findall('<input type="hidden" name="(.*)"\svalue="(.*)"\/>',a.text)
	data = {'hash': ahash, captchaName: '', 
	temp[0][0] : temp[0][1],
	'decrypt': 'Decrypt',
	}
	b = r.post(api2,data=data,verify=False)
	if 'Sorry, this hash is not in our database' in b.text:
		return False
	else:
		return re.findall('<\/div><br\/>(.*)<br\/><br\/>',b.text)[0]



def brute3(ahash):
	r = requests.session()
	a = r.get('https://hashes.com/en/decrypt/hash',verify=False)	
	csrf_token = re.findall('<input type="hidden" name="csrf_token" value="([^"]*)',a.text)[0]
	postData = {
'csrf_token': csrf_token,
'hashes': ahash,
'knn': 64,
'submitted': 'true'
}
	b = r.post('https://hashes.com/en/decrypt/hash',data=postData,verify=False)
	if 'Left:' in b.text:
		return False
	else:
		return re.findall(ahash+':([^<]*)',b.text)[0]


def brute4(ahash):
	a = requests.get('https://hashtoolkit.com/decrypt-hash/?hash='+ahash,verify=False)
	if 'No hashes found for' in a.text:
		return False
	else:
		try:
			return re.findall('<span title="decrypted md5 hash"><a href="([^"])*">([^<]*)<\/a>',a.text)[1]
		except:
			return False

def Crack(ahash):
	m = brute1(ahash)
	if m!=False:
		return json.dumps({
        "hash": ahash,
        "hash type": "md5",
        "dehash": m,
        "success":"true",
        "author": "abhayGupta"
    })
	m = brute2(ahash)
	if m!=False:
		return json.dumps({
        "hash": ahash,
        "hash type": "md5",
        "dehash": m,
        "success":"true",
        "author": "abhayGupta"
    })
	m = brute3(ahash)
	if m!=False:
		return json.dumps({
        "hash": ahash,
        "hash type": "md5",
        "dehash": m,
        "success":"true",
        "author": "abhayGupta"
    })
	m = brute4(ahash)
	if m!=False:
		return json.dumps({
        "hash": ahash,
        "hash type": "md5",
        "dehash": m,
        "success":"true",
        "author": "abhayGupta"
    })
	return json.dumps({
        "hash": ahash,
        "hash type": "md5",
        "success":"false",
        "author": "abhayGupta"
    })

app = Flask(__name__)
@app.route('/')
def helloWorld():
	return "<title>MD5 DECRYPTER | ABHAY</title>"+render_template('index.html')


@app.route('/md5',methods=["GET","POST"])
def crackmd5():
	if request.method == "POST":
		ahash = request.form['ahash']
		open('ss.log','a').write('\n'+ahash)
		return Crack(ahash)
	if request.method=="GET":
		if "md5" in request.args:
			ahash = request.args.get('md5')
			ahash = ahash.strip()
			if ahash=='':
				return "Invalid Request"
			if len(ahash)!=32:
				return "Not a md5 HashType"

			open('ss.log','a').write('\n'+ahash)
			return Crack(ahash)

		else:
			return "Invalid Request"

app.run(0.0.0.0)