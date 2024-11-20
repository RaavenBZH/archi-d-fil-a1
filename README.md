# UE-AD-A1-MIXTE

Pour démarrer les différents services 
Utiliser : ```docker compose up --build``` 

TP1 REST sur la branch 
tp1 -> git checkout tp1


TP2 MIXTE sur la branche 
main -> git checkout main


Utilisation des différents endpoints : 


User (REST) 

- [GET] localhost:3203 -> Message de bienvenue
  
- [GET] localhost:3203/users -> Renvoie tous les users
  
- [GET] localhost:3203/usersbyid/<userid> -> Renvoie les réservations d'un utilisateur à partir de son id
  
- [GET] localhost:3203/usersbyname/<username> ->  Renvoie les réservations d'un utilisateur à partir de son nom
  
- [GET] localhost:3203/users/movies/<userid> -> Renvoie les détails des films de la réservation d'un utilisateur à partir de son id


Movie (GraphQL)

http://localhost:3200/graphql 

Query : 
movie_with_rate(_rate: FLOAT)
  -> Renvoie les films ayant une note de plus ou moins _rate en note

Query : 
movies_info -> Renvoie toutes les routes liées à Movie

Mutation : 
delete_movie_with_id(_id: STRING) -> Supprime un film à partir de son ID

Query : 
movie_with_director(_director: STRING) -> Renvoie les films d'un directeur à partir depuis son nom

Query : 
movie_with_title(_title: STRING) -> Renvoie le film à partir du titre

Query : 
movie_with_id(_id: STRING -> Renvoie un film à partir de son ID

Mutation : 
update_movie_rating(_id: STRING,  _rate : FLOAT) -> Change la note d'un film à partir de son ID


Showtime (gRPC)

localhost:3202 Showtime / Home (Empty)

localhost:3202 Showtime / GetAllSchedules (Empty)

localhost:3202 Showtime / GetSchedule ("date" : String)

Booking (gRPC)

localhost:3201 BookingService / Home

localhost:3201 BookingService / GetAllBookings

localhost:3201 BookingService / GetBookingsForUser ("userid" : String)

localhost:3201 BookingService / AddBookingForUser ("userid":String, "date": String, "movieid": String)
