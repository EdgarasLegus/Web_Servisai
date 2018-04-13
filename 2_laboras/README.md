#Build
docker-compose build
docker-compose up -d
docker-compose ps

#########GET method for another web service

curl -i http://193.219.91.103:11361/dogs

########GET method: dog for every team

curl -i http://193.219.91.103:11361/football_teams/id/dogs

#######POST method: create new dog for the team

in postman: Connection-Type: application/json

http://193.219.91.103:11361/football_teams/dogs

{
    "Name": "Sevilla",
    "Country": "Spain",
    "breed": "Spanilel",
    "Spot": "7",
    "name": "Bruno",
    "temporary guardian ID": "Michael"
} 
