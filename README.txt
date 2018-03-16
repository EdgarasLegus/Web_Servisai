#Build and run

docker-compose build

# Web Service pagrindinis
11361 forwardina i 80 porta

193.219.91.103:11361
193.219.91.103:11361/football_teams

#Pagrindinis puslapis - introduction

#INFORMACIJA APIE VISAS KOMANDAS
Postman:
GET http://193.219.91.103:11361/football_teams

#Informacija apie konkrecia komanda
Postman:
GET http://193.219.91.103:11361/football_teams/<id> , kur id musu atveju nuo 1 iki 5

#PRIDETI NAUJA KOMANDA
Postman:
POST - reikia nustatyti Headers - Connection-Type ir application/json.
Ieiti i raw ir ivesti:
{
  "Name": "New team"
}

#PAKEISTI KOMANDOS ATRIBUTUS
Postman:
PUT http://193.219.91.103:11361/football_teams/<id>, kur id nuo 1 iki 5.
reikia nustatyti Headers - Connection-Type ir application/json.
Ieiti i raw ir ivesti :
{
  "Captain": "Messi"
}

#ISTRINTI KOMANDA
Postman:
DELETE http://193.219.91.103:11361/football_teams/<id> , kur id nuo 1 iki 6
