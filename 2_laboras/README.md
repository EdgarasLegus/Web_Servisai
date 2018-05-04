# Build

- docker-compose build
- docker-compose up -d
- docker-compose ps

# 1-os užduoties užklausos

## GET - gauti informaciją apie visas komandas arba konkrečią komandą
- curl -i http://193.219.91.103:11361/football_teams
- curl -i http://193.219.91.103:11361/football_teams/1

## POST - sukurti nauja komanda
curl -i -X POST -H  "Content-Type: application/json" -d '{"Name":"Roma"}' http://193.219.91.103:11361/football_teams 

## PUT - pakeisti komandos atributus.
curl -i -H "Content-Type: application/json" -X PUT -d '{"Name":"Fiorentina", "Country":"Italy", "Stadium":"Fialco", "Attendance":"18000", "Captain":"Giacomo Saviola" }' http://193.219.91.103:11361/football_teams/1  

## DELETE - istrinti komanda
curl -i -X DELETE http://193.219.91.103:11361/football_teams/1

# 2-os uzduoties uzklausos

## GET - perziureti komandu suniukus arba vienos komandos suniuka
- curl -i http://193.219.91.103:11361/football_teams?embedded=dog
- curl -i http://193.219.91.103:11361/football_teams/1?embedded=dog

## POST - sukurti nauja komanda ir nauja suniuka
curl -i -X POST -H "Content-Type: application/json" -d '{"Name":"Nurnberg, "Dog": {"breed":"spaniel", "name":"Firmino", "temporary guardian ID":"Geronimo"}}' http://193.219.91.103:11361/football_teams?embedded=dog

## PUT - pakeisti info apie šuniuką.
curl -i -H "Content-Type: application/json" -X -PUT -d '{"name": "wilson", "breed": "captain",  "temporary guardian ID": "idaho"}' http://193.219.91.103:11361/football_teams/1/dog


