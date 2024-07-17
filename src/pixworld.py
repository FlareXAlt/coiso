import requests, re, websocket, time, json
from datetime import datetime, timezone
import ctypes
import random
from src.console import printPixel, printRefuse, printCaptcha

captcha = 0
def generateHash():
  	URL = 'https://pixworld.vercel.app/ptbr'
  	r = requests.get(URL, headers={
    	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0'
  	})

  	#"hash = re.findall(r'"wsHash":"(.+?)"', r.text)[0]"

  	return "hash"

def connect(hash, token=None):
	ws = websocket.WebSocket()
	ws.connect(f'wss://api.henrixounez.com/pixworld/pix/connect?hash={hash}', header={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0'},origin='https://pixworld.vercel.app')

	if token != None:
		time.sleep(2)
		ws.send('{"type":"loginUser","data":"%s"}' % (token))

	return ws


def getAccount(username, password):
	token = json.loads(requests.post('https://api.henrixounez.com/pixworld/user/login', json = {'username': f'{username}', 'password': f'{password}'}).content)['token']
	return token

def placePixel(ws, world, x, y, color):
	ws.send('{"type":"placePixel","data":{"x":%s,"y":%s,"color":"%s","canvas":"%s"}}' % (x,y,color,world))
	global captcha
	while True:
		data = json.loads(ws.recv())
		time.sleep(random.uniform(0.2,1))
		if data["type"] == 'confirmPixel':
			printPixel(x, y, color)
			cd = 30

			utc = datetime.now(timezone.utc)
			utc = utc.timestamp()

			now = int(utc)
			cooldown = cd - now
			return cooldown
			break
		elif data['type'] == "refusePixel":
			print(data)
			printRefuse(x, y, color)
			time.sleep(20)
			break
		elif data['type'] == "captchaNeeded":
			printCaptcha()
			#import requests
			#"https://api.henrixounez.com/pixworld/captcha.png"
			#response = requests.get("https://api.henrixounez.com/pixworld/captcha.png")
			#if response.status_code == 200:
			#	with open("captcha.png", "wb") as f:
			#		f.write(response.content)
			#text = input(">")
			#data = {"text": text}
			#requests.post("https://api.henrixounez.com/pixworld/captcha/verify", json=data)

			#ctypes.windll.kernel32.SetConsoleTitleW("DRACON BOT | CAPTCHA")
			return "captcha"
			break


