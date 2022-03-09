from flask import Flask, redirect, url_for, render_template
from datetime import datetime
from dateutil.parser import parse
from lib import lib
import webbrowser
import json
import requests
import os



#===VERSION===
response = requests.get("https://api.github.com/repos/EternalDusk/Infinite-Analysis/releases/latest")

try:
	version = response.json()["tag_name"]
	if str(version) != "v1.1.0":
		print("Update Available! Go to https://github.com/EternalDusk/Infinite-Analysis/releases to update!")
except:
	print("Latest version grab failed (is there a release yet?)")


#===SETTINGS===
username = input("Enter the username of the player you'd like to track: ").replace(" ", "_")

playerGames = "gameData_" + username
resources_dir = os.path.expanduser('~\\Documents\\Dusk')
static_path = os.path.join('black-dashboard-master\\assets')
template_path = os.path.join('black-dashboard-master')

#===TOKEN SETTING===
lib = lib({'token': '<insert_token_here>'})

#===STARTING DIR===
if (os.path.isdir(resources_dir)) != True:
	os.mkdir(resources_dir)

if (os.path.isdir(os.path.join(resources_dir, playerGames))) != True:
	os.mkdir(os.path.join(resources_dir, playerGames))

if (os.path.isdir(os.path.join(resources_dir, playerGames, "teamData"))) != True:
	os.mkdir(os.path.join(resources_dir, playerGames, "teamData"))

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


message_once = False
for file in os.listdir(os.path.join(resources_dir, playerGames)):
	if (message_once == False):
		if (len(os.listdir(os.path.join(resources_dir, playerGames))) > 1):
			print("Updating previous game file versions, this might take a minute...")
			message_once = True
	if (os.path.isfile(os.path.join(resources_dir, playerGames, file))):
		with open(os.path.join(resources_dir, playerGames, file)) as update_file:
			data = json.load(update_file)
			print("Updating game file with id: " + data["id"])

			team_data = lib.halo.infinite['@0.3.9'].stats.matches.retrieve({
			'id': data["id"]
			});

			players_grabbed = False
			while players_grabbed == False:
				for i in range(0, len(team_data["data"]["players"])):
					if (team_data["data"]["players"][i]["gamertag"] == "???"):
						team_data = lib.halo.infinite['@0.3.9'].stats.matches.retrieve({
						'id': data["id"]
						});
						break
					else:
						players_grabbed = True

			path = os.path.join(resources_dir, playerGames, "teamData", data["id"] + ".txt")
			if (os.path.exists(path)) != True:
				with open(path, "w") as f:
					f.write(json.dumps(team_data))

		update_file.close()

		os.remove(os.path.join(resources_dir, playerGames, file))


for item in games["data"]:
	gameID = item["id"]

	path = os.path.join(resources_dir, playerGames, "teamData", gameID + ".txt")
	if (os.path.exists(path)) != True:

		team_data = lib.halo.infinite['@0.3.9'].stats.matches.retrieve({
		'id': gameID
		});

		players_grabbed = False
		while players_grabbed == False:
			for i in range(0, len(team_data["data"]["players"])):
				if (team_data["data"]["players"][i]["gamertag"] == "???"):
					team_data = lib.halo.infinite['@0.3.9'].stats.matches.retrieve({
					'id': data["id"]
					});
					break
				else:
					players_grabbed = True

		print("Saving game with id: " + str(gameID))
		with open(path, "w") as f:
			f.write(json.dumps(team_data))


matchInfo = []

for gameFile in os.listdir((os.path.join(resources_dir, playerGames, "teamData"))):
	with open(os.path.join(resources_dir, playerGames, "teamData", gameFile)) as json_file:
		data = json.load(json_file)

		cobraInfo = []
		eagleInfo = []

		if (data["data"]["details"]["playlist"]["properties"]["ranked"] == True):
			for player in data["data"]["players"]:
				playerGamertag = player["gamertag"]
				playerTeam = player["team"]["name"]
				playerRank = player["rank"]
				playerMMR = round(player["team"]["skill"]["mmr"], 2)
				playerCSR = player["progression"]["csr"]["post_match"]["value"]
				playerKills = player["stats"]["core"]["summary"]["kills"]
				playerDeaths = player["stats"]["core"]["summary"]["deaths"]
				playerAssists = player["stats"]["core"]["summary"]["assists"]
				playerAccuracy = round(player["stats"]["core"]["shots"]["accuracy"], 2)

				if (playerTeam == "Cobra"):
					cobraInfo.append([playerGamertag, playerTeam, playerRank, playerMMR, playerCSR, playerKills, playerDeaths, playerAssists, playerAccuracy])
				else:
					eagleInfo.append([playerGamertag, playerTeam, playerRank, playerMMR, playerCSR, playerKills, playerDeaths, playerAssists, playerAccuracy])
		else:
			for player in data["data"]["players"]:
				playerGamertag = player["gamertag"]
				playerTeam = player["team"]["name"]
				playerRank = player["rank"]
				playerMMR = "N/A"
				playerCSR = "N/A"
				playerKills = player["stats"]["core"]["summary"]["kills"]
				playerDeaths = player["stats"]["core"]["summary"]["deaths"]
				playerAssists = player["stats"]["core"]["summary"]["assists"]
				playerAccuracy = round(player["stats"]["core"]["shots"]["accuracy"], 2)


				if (playerTeam == "Cobra"):
					cobraInfo.append([playerGamertag, playerTeam, playerRank, playerMMR, playerCSR, playerKills, playerDeaths, playerAssists, playerAccuracy])
				else:
					eagleInfo.append([playerGamertag, playerTeam, playerRank, playerMMR, playerCSR, playerKills, playerDeaths, playerAssists, playerAccuracy])

		for p in range(0, len(data["data"]["players"])):
			if data["data"]["players"][p]["gamertag"] == username:
				accuracy = round(data["data"]["players"][p]["stats"]["core"]["shots"]["accuracy"], 2)
				rank = data["data"]["players"][p]["rank"]
				map = data["data"]["details"]["map"]["name"]
				gametype = data["data"]["details"]["category"]["name"]
				outcome = data["data"]["players"][p]["outcome"]
				score = data["data"]["players"][p]["stats"]["core"]["score"]

				cobraOutcome = data["data"]["teams"]["details"][1]["outcome"]
				eagleOutcome = data["data"]["teams"]["details"][0]["outcome"]

				date = data["data"]["played_at"][0:10]
				time = data["data"]["played_at"][11:19]
				dateTime = parse(date + " " + time).strftime("%m%d%Y, %H:%M:%S")

				id = data["data"]["id"].replace("-", "")

				for ele in id:
				    if ele.isdigit():
				        id = id.replace(ele, "")
				id += time.replace(":", "")

				if (data["data"]["details"]["playlist"]["properties"]["ranked"] == True):
					csr = data["data"]["players"][p]["progression"]["csr"]["post_match"]["value"]
					CSR_change = data["data"]["players"][p]["progression"]["csr"]["post_match"]["value"] - data["data"]["players"][p]["progression"]["csr"]["pre_match"]["value"]

					matchInfo.append([[dateTime, id, "Ranked"], [map, gametype, outcome, cobraOutcome, eagleOutcome], [rank, accuracy, score, csr, CSR_change], cobraInfo, eagleInfo])
				else:
					csr = -1
					CSR_change = 0

					matchInfo.append([[dateTime, id, "Unranked"], [map, gametype, outcome, cobraOutcome, eagleOutcome], [rank, accuracy, score, csr, CSR_change], cobraInfo, eagleInfo])


matchInfo.sort(key=lambda x: x[0])
matchSorted = matchInfo[::-1]

gameInfo = {}

saved_csr = current_CSR

saved_mmr = 0
mmr_set = False

for g in games["data"]:
	if (g["details"]["playlist"]["properties"]["ranked"] == True):
		current_mmr = round(g["player"]["team"]["skill"]["mmr"], 4)
		saved_mmr = current_mmr
		mmr_set = True
		break

if (len(games["data"]) < 10):
	gameLength = len(games["data"])
else:
	gameLength = 10

for i in range(0,gameLength):
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

if (mmr_set == False):
	current_mmr = 0

webbrowser.open_new_tab("http://localhost:8080")

#===STARTING FLASK APPLICATION===
app = Flask('Infinite Analysis', static_folder=static_path, template_folder=template_path)

@app.route('/')
def show_index():
	return render_template("index.html", username=username, serviceTag=serviceTag, userEmblemURL=emblemURL, gameData=gameInfo,currentCSR=current_CSR, csr_tier_url=csr_tier_url, current_mmr=current_mmr, tier_start=tier_start, next_tier_start=next_tier_start)

@app.route('/games.html')
def show_games():
	return render_template("games.html", username=username, serviceTag=serviceTag, userEmblemURL=emblemURL, matchData=matchSorted)


#run flask app
app.run(host = '0.0.0.0', port = 8080)