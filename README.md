# UE-AD-A1-REST

Pour démarrer les différents services 
utiliser pour chaque tp : ```docker compose up --build``` 

TP1 REST sur la branch ```tp1``` -> ```git checkout tp1```

TP2 MIXTE sur la branche ```main``` -> ```git checkout main```

Utilisation des différents endpoints : 


**User (REST)** 

- [GET] ```localhost:3203``` -> Message de bienvenue
  
- [GET] ```localhost:3203/users``` -> Renvoie tous les users
  
- [GET] ```localhost:3203/usersbyid/<userid>``` -> Renvoie les réservations d'un utilisateur à partir de son id
  
- [GET] ```localhost:3203/usersbyname/<username>``` ->  Renvoie les réservations d'un utilisateur à partir de son nom

- [GET] ```localhost:3203/users/movies/<userid>``` -> Renvoie les détails des films de la réservation d'un utilisateur à partir de son id

  
**Booking (REST)** 

- [GET] ```http://localhost:3201/``` -> Message de bienvenue

- [GET] ```http://localhost:3201/bookings``` -> Renvoie toutes les réservations

- [GET] ```http://localhost:3201/bookings/<userid>``` -> Renvoie les réservations d'un utilisateur à partir de son id
 
- [GET] ```http://localhost:3201/bookings/<userid>``` -> Ajoute une réservation à un utilisateur à partir de son id POST DATA ```"date": STRING, "movieid": STRING```

**Showtime (REST)** 

- [GET] ```http://localhost:3202/``` -> Message de bienvenue 

- [GET] ```http://localhost:3202/showtimes``` -> Renvoie toutes les dates avec les films associés
 
- [GET] ```http://localhost:3202/showtimes/<date>``` -> Renvoie les films d'une date
- [POST] ```http://localhost:3202add_schedule``` -> Ajoute une programmation

  **Movie**
  - [GET] ```http://localhost:3200/json```
  - [GET] ```http://localhost:3200/```
  - [GET] ```http://localhost:3200/movies/`<movieid>` ```
  - [GET] ```http://localhost:3200/moviesbytitle?title=TITRE ```
  - [GET] ```http://localhost:3200/director=DIRECTOR ```
  - [GET] ```http://localhost:3200/moviesbyrate?rate=RATE```
  - [GET] ```http://localhost:3200/help```
  - [POST] ```http://localhost:3200/addmovie/`<movieid>` ```
  - [DEL] ```http://localhost:3200/movies/`<movieid>````
  - [PUT] ```http://localhost:3200/movies/`<movieid>`/`<rate>` ```
    
    
