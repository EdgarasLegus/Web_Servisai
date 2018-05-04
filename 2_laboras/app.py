from flask import Flask, jsonify, abort, request
#from redis import Redis
from flask import make_response
import os
import re
import json
import requests
import copy

app = Flask(__name__)
#redis = Redis(host='redis',port=6379)

football_teams = [
  {
    'ID': '1',
    'Name': 'FC Barcelona',
    'Country': 'Spain',
    'Stadium': 'Camp Nou',
    'Attendance': '99354',
    'Captain': 'Andres Iniesta',
    'Dog_ID': '1'
  },
  {
    'ID': '2',
    'Name': 'Real Madrid CF',
    'Country': 'Spain',
    'Stadium': 'Estadio Santiago Bernabeu',
    'Attendance': '81044',
    'Captain': 'Sergio Ramos',
    'Dog_ID': '1'
  },
  {
    'ID': '3',
    'Name': 'Club Atletico de Madrid',
    'Country': 'Spain',
    'Stadium': 'Wanda Metropolitano',
    'Attendance': '67703',
    'Captain': 'Gabi',
    'Dog_ID': '1'
  },
  {
    'ID': '4',
    'Name': 'FC Bayern Muchen',
    'Country': 'Germany',
    'Stadium': 'Allianz Arena',
    'Attendance': '75000',
    'Captain': 'Manuel Neuer',
    'Dog_ID': '1'
  },
  {
    'ID': '5',
    'Name': 'Juventus',
    'Country': 'Italy',
    'Stadium': 'Allianz Stadium',
    'Attendance': '41507',
    'Captain': 'Gianluigi Buffon',
    'Dog_ID': '1'
  },
  {
    'ID': '6',
    'Name': 'Roma',
    'Country': 'Italy',
    'Stadium': 'Stadio Olimpico',
    'Attendance': '51666',
    'Captain': 'Daniele De Rossi',
    'Dog_ID': '1'
  }
]

# Introduction
@app.route('/')
def hello():
#	redis.incr('counter')
	return 'Hi! Here we provide info about football. You have been here %s time(s).' #%redis.get('counter')

# Showing info about teams
@app.route('/football_teams', methods=['GET'])
def get_football_teams():
	if( request.args.get('name', '')):
		findTeams = []
		for i in football_teams:
			if( re.search(request.args.get('name', ''), i["Name"], re.IGNORECASE)):
				findTeams.append(i)
		return jsonify(findTeams), 200
	elif( request.args.get('embedded', '') == "dog"):
		embTeams=copy.deepcopy(football_teams)
		for i in range(0, len(football_teams)):
			try:
				req = requests.get('http://web2:81/dogs/'+embTeams[int(i)]['Dog_ID'])
				req = json.loads(req.text)
				embTeams[int(i)]['Dog_ID'] = req
			except requests.exceptions.RequestException as e:
				embTeams[int(i)]['Dog_ID'] = "null"
		return jsonify(embTeams), 200
	else:
		return jsonify(football_teams), 200

# Get method to show team by id
@app.route('/football_teams/<team_id>', methods=['GET'])
def get_team(team_id):
	if( request.args.get('embedded', '') == "dog"):
		embTeams=copy.deepcopy(football_teams)
		try:
			req = requests.get('http://web2:81/dogs/'+embTeams[int(team_id)]['Dog_ID'])
			req = json.loads(req.text)
			embTeams[int(team_id)]['Dog_ID'] = req
		except requests.exceptions.RequestException as e:
			embTeams[int(team_id)]['Dog_ID'] = "null"
		return jsonify(embTeams[int(team_id)]), 200
	else:
  		team = [tm for tm in football_teams if (tm['ID'] == team_id) ]
  		return jsonify(team), 200

# Create a new team
@app.route('/football_teams', methods=['POST'])
def create_team():
	if (request.args.get('embedded', '') == "dog"):
		dog = request.json['Dog']
		team_nr = len(football_teams)+1
		req = requests.post('http://web2:81/dogs', json = {"breed": dog['breed'], "name": dog['name'], "temporary guardian ID": dog['temporary guardian ID']})
		req = json.loads(req.text)
		item = {
	  		'ID': team_nr,
	  		'Name': request.json['Name'],
	  		'Country': request.json.get('Country', "Unknown"),
	  		'Stadium': request.json.get('Stadium', "Unknown"),
	  		'Attendance': request.json.get('Attendance', "10000"),
	  		'Captain': request.json.get('Captain', "Player"),
	  		'Dog_ID': req['id']
		}
		football_teams.append(item)
		return jsonify(item), 201
	else:
		team_nr = len(football_teams)+1
		req = requests.get('http://web2:81/dogs/'+request.json['Dog_ID'])
		if not request.json or not 'Name' in request.json:
			abort(404)
		else:
			item = {
				'ID': team_nr,
				'Name': request.json['Name'],
				'Country': request.json.get('Country', "Unknown"),
				'Stadium': request.json.get('Stadium', "Unknown"),
				'Attendance': request.json.get('Attendance', "10000"),
				'Captain': request.json.get('Captain', "Player"),
				'Dog_ID': request.json['Dog_ID']
			}
			football_teams.append(item)
			return jsonify(item), 201

# Change team attributes
@app.route('/football_teams/<team_id>', methods=['PUT'])
def change_team(team_id):
    item = [item for item in football_teams if item['ID'] == team_id]
    if len(item) == 0:
        abort(404)
    if not request.json:
        abort(400)
    if 'Name' in request.json and type(request.json['Name']) != unicode:
        abort(400)
    if 'Country' in request.json and type(request.json['Country']) != unicode:
        abort(400)
    if 'Stadium' in request.json and type(request.json['Stadium']) != unicode:
        abort(400)
    if 'Attendance' in request.json and type(request.json['Attendance']) != unicode:
        abort(400)
    if 'Captain' in request.json and type(request.json['Captain']) != unicode:
        abort(400)
    item[0]['Name'] = request.json.get('Name', item[0]['Name'])
    item[0]['Country'] = request.json.get('Country', item[0]['Country'])
    item[0]['Stadium'] = request.json.get('Stadium', item[0]['Stadium'])
    item[0]['Attendance'] = request.json.get('Attendance', item[0]['Attendance'])
    item[0]['Captain'] = request.json.get('Captain', item[0]['Captain'])
    return jsonify(item[0]), 200

# Change team attributes
@app.route('/football_teams/<team_id>/dog', methods=['PUT'])
def change_info(team_id):
	if(request.json ['name']):
		req = requests.put('http://web2:81/dogs/'+football_teams[int(team_id)]["Dog_ID"], json = {"id": request.json.get('id', "1"), "name": request.json['name'],  "breed": request.json['breed'], "temporary guardian ID": request.json['temporary guardian ID']})
		req = json.loads(req.text)
		return jsonify(req), 200
	else:
		ch  = [team for team in football_teams if (team['ID'] == team_id)]
		football_teams[int(team_id)]['Name'] = request.json['Name']
		football_teams[int(team_id)]['Country'] = request.json['Country']
		football_teams[int(team_id)]['Stadium'] = request.json['Stadium']
		football_teams[int(team_id)]['Attendance'] = request.json['Attendance']
		football_teams[int(team_id)]['Captain'] = request.json['Captain']
		return jsonify(football_teams[int(team_id)]), 200

# Delete teams
@app.route('/football_teams/<team_id>', methods=['DELETE'])
def delete_team(team_id):
  item = [item for item in football_teams if item['ID'] == team_id]
  if len(item) == 0:
  	abort(404)
  football_teams.remove(item[0])
  return jsonify(True), 200

@app.errorhandler(404)
def not_found(error):
	return make_response(jsonify({'error': 'Not Found'}), 404)

#@app.route('/football_teams/<team_id>/dog', methods=['DELETE'])
#def delete_dog(team_id):
#	item = [item for item in football_teams if item['ID'] == team_id]
#	if len(item) == 0:
#       		abort(404)
#	url = 'http://web2:81/dogs/'+item[0]['Dog_ID']
#   	req = requests.delete(url).text
#	football_teams.remove(item[0])
#	req = json.loads(req)
#	return jsonify(team_id), 200

if __name__== "__main__":
	app.run(host="0.0.0.0",debug=True, port=5000)
