from flask import Flask, redirect, url_for, render_template
from datetime import datetime
from dateutil.parser import parse
from lib import lib
import json
import requests
import os


#===SETTINGS===
username = input("Enter the username of the player you'd like to track: ")

playerGames = "gameData_" + username
resources_dir = os.path.expanduser('~\\Documents\\Dusk')
static_path = os.path.join(os.getcwd(), './black-dashboard-master/assets')
template_path = os.path.join(os.getcwd(), './black-dashboard-master')

#===TOKEN SETTING===
lib = lib({'token': '<insert_token_here>'})

#===STARTING DIR===
if (os.path.isdir(resources_dir)) != True:
	os.mkdir(resources_dir)

if (os.path.isdir(os.path.join(resources_dir, playerGames))) != True:
	os.mkdir(os.path.join(resources_dir, playerGames))

#===VERSION===
response = requests.get("https://api.github.com/repos/EternalDusk/Infinite-Analysis/releases/latest")

try:
	version = response.json()["tag_name"]
	if str(version) != "v1.0.0":
		print("Update Available! Go to https://github.com/EternalDusk/Infinite-Analysis/releases to update!")
except:
	print("Latest version grab failed (is there a release yet?)")

#===STARTING CALLS===
print("Grabbing player data...")

profile = lib.halo.infinite['@0.3.9'].appearance({
  'gamertag': username
})

games = lib.halo.infinite['@0.3.9'].stats.matches.list({
  'gamertag': username,
  'limit': {
	'count': 25,
	'offset': 0
  },
  'mode': 'matchmade'
});

csr_info = lib.halo.infinite['@0.3.9'].stats.csrs({
  'gamertag': username,
  'season': 1,
  'version': 2
});

#===PARSING DATA===

backgroundURL = profile["data"]["backdrop_image_url"]
emblemURL = profile["data"]["emblem_url"]
serviceTag = profile["data"]["service_tag"]

csr_tier_url = csr_info["data"][0]["response"]["current"]["tier_image_url"]

current_CSR = csr_info["data"][0]["response"]["current"]["value"]
tier_start = csr_info["data"][0]["response"]["current"]["tier_start"]
next_tier_start = csr_info["data"][0]["response"]["current"]["next_tier_start"]

for item in games["data"]:
	gameID = item["id"]
	path = os.path.join(resources_dir, playerGames, gameID + ".txt")
	if (os.path.exists(path)) != True:
		print("Saving game with id: " + str(gameID))
		with open(path, "w") as f:
			f.write(json.dumps(item))

matchInfo = []

for gameFile in os.listdir((os.path.join(resources_dir, playerGames))):
	with open(os.path.join(resources_dir, playerGames, gameFile)) as json_file:
		data = json.load(json_file)

		if (data["details"]["playlist"]["properties"]["ranked"] == True):

			accuracy = round(data["player"]["stats"]["core"]["shots"]["accuracy"], 2)
			rank = data["player"]["rank"]
			map = data["details"]["map"]["name"]
			gametype = data["details"]["category"]["name"]
			outcome = data["player"]["outcome"]
			csr = data["player"]["progression"]["csr"]["post_match"]["value"]
			CSR_change = data["player"]["progression"]["csr"]["post_match"]["value"] - data["player"]["progression"]["csr"]["pre_match"]["value"]
			score = data["player"]["stats"]["core"]["score"]

			date = data["played_at"][0:10]
			time = data["played_at"][11:19]
			dateTime = parse(date + " " + time).strftime("%m%d%Y, %H:%M:%S")

			matchInfo.append([accuracy, rank, map, gametype, outcome, CSR_change, score, dateTime, csr])

matchInfo.sort(key=lambda x: x[7])
matchSorted = matchInfo[::-1]

gameInfo = {}

saved_csr = current_CSR

for g in games["data"]:
	print(g["details"]["playlist"]["properties"]["ranked"])
	if (g["details"]["playlist"]["properties"]["ranked"] == True):
		current_mmr = round(g["player"]["team"]["skill"]["mmr"], 4)
		saved_mmr = current_mmr
		break

for i in range(0,10):
	nameAcc = "game" + str(i) + "acc"
	nameKDR = "game" + str(i) + "kdr"
	nameCSR = "game" + str(i) + "csr"
	nameMMR = "game" + str(i) + "mmr"

	gameInfo.update({nameAcc: games["data"][i]["player"]["stats"]["core"]["shots"]["accuracy"]})
	gameInfo.update({nameKDR: games["data"][i]["player"]["stats"]["core"]["kdr"]})

	if (games["data"][i]["details"]["playlist"]["properties"]["ranked"] == True):
		gameInfo.update({nameMMR: round(games["data"][i]["player"]["team"]["skill"]["mmr"], 4)})
		gameInfo.update({nameCSR: games["data"][i]["player"]["progression"]["csr"]["post_match"]["value"]})
		saved_csr = games["data"][i]["player"]["progression"]["csr"]["post_match"]["value"]
		saved_mmr = round(games["data"][i]["player"]["team"]["skill"]["mmr"], 4)
	else:
		gameInfo.update({nameCSR: saved_csr})
		gameInfo.update({nameMMR: saved_mmr})

	i += 1


#===STARTING FLASK APPLICATION===
app = Flask('Infinite Analysis', static_folder=static_path, template_folder=template_path)

@app.route('/')

def run():
	return render_template("index.html", username=username, serviceTag=serviceTag, userEmblemURL=emblemURL, gameData=gameInfo, matchData=matchSorted, currentCSR=current_CSR, csr_tier_url=csr_tier_url, current_mmr=current_mmr, tier_start=tier_start, next_tier_start=next_tier_start)

#run flask app
app.run(host = '0.0.0.0', port = 8080)