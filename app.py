from flask import Flask, jsonify, abort, request
from redis import Redis
from flask import make_response
import os
import re

app = Flask(__name__)
redis = Redis(host='redis',port=6379)

football_teams = [
  {
    'ID': 1,
    'Name': 'FC Barcelona',
    'Country': 'Spain',
    'Stadium': 'Camp Nou',
    'Attendance': '99354',
    'Captain': 'Andres Iniesta'
  },
  {
    'ID': 2,
    'Name': 'Real Madrid CF',
    'Country': 'Spain',
    'Stadium': 'Estadio Santiago Bernabeu',
    'Attendance': '81044',
    'Captain': 'Sergio Ramos'
  },
  {
    'ID': 3,
    'Name': 'Club Atletico de Madrid',
    'Country': 'Spain',
    'Stadium': 'Wanda Metropolitano',
    'Attendance': '67703',
    'Captain': 'Gabi'
  },
  {
    'ID': 4,
    'Name': 'FC Bayern Muchen',
    'Country': 'Germany',
    'Stadium': 'Allianz Arena',
    'Attendance': '75000',
    'Captain': 'Manuel Neuer'
  },
  {
    'ID': 5,
    'Name': 'Juventus',
    'Country': 'Italy',
    'Stadium': 'Allianz Stadium',
    'Attendance': '41507',
    'Captain': 'Gianluigi Buffon'
  }
]

# Introduction
@app.route('/')
def hello():
	redis.incr('counter')
	return 'Hi! Here we provide info about football. You have been here %s time(s).' %redis.get('counter')

# Showing info about teams
@app.route('/football_teams', methods=['GET'])
def get_football_teams():
	if( request.args.get('name', '')):
		findTeams = []
		for i in football_teams:
			if( re.search(request.args.get('name', ''), i["Name"], re.IGNORECASE)):
				findTeams.append(i)
		return jsonify(findTeams)
	else:
		return jsonify(football_teams), 200

# Get method to show team by id
@app.route('/football_teams/<int:team_id>', methods=['GET'])
def get_team(team_id):
  team = [tm for tm in football_teams if (tm['ID'] == team_id) ]
  return jsonify(team)

# Create a new team
@app.route('/football_teams', methods=['POST'])
def create_team():
	if not request.json or not 'Name' in request.json:
	  abort(400)
	item = {
	  'ID': football_teams[-1]['ID'] + 1,
	  'Name': request.json['Name'],
	  'Country': request.json.get('Country', ""),
	  'Stadium': request.json.get('Stadium', "Unknown"),
	  'Attendance': request.json.get('Attendance', "10000"),
	  'Captain': request.json.get('Captain', "Player")

	}
	football_teams.append(item)
	return jsonify(item), 201, {'Location': '/football_teams/'+str(football_teams[-1]['ID'])}

# Change team attributes
@app.route('/football_teams/<int:team_id>', methods=['PUT'])
def change_info(team_id):
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

# Delete teams
@app.route('/football_teams/<int:team_id>', methods=['DELETE'])
def delete_team(team_id):
  item = [item for item in football_teams if item['ID'] == team_id]
  if len(item) == 0:
    abort(404)
  football_teams.remove(item[0])
  return jsonify(True), 200

@app.errorhandler(404)
def not_found(error):
	return make_response(jsonify({'error': 'Not Found'}), 404)

if __name__== "__main__":
	app.run(host="0.0.0.0",debug=True)
