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
- [GET] ```http://localhost:3200/json``` -> Retourne la liste des films
- [GET] ```http://localhost:3200/``` -> Message de bienvenue 
- [GET] ```http://localhost:3200/movies/`<movieid>` ``` -> Renvoie un film à partir de son ID
- [GET] ```http://localhost:3200/moviesbytitle?title=TITRE ``` Renvoie un film à partir de son titre
- [GET] ```http://localhost:3200/director=DIRECTOR ``` -> Renvoie les films à partir d'un directeur 
- [GET] ```http://localhost:3200/moviesbyrate?rate=RATE``` -> Renvoie les films à partir des notes
- [GET] ```http://localhost:3200/help``` -> Renvoie les routes de "movie"
- [POST] ```http://localhost:3200/addmovie/`<movieid>` ``` -> Ajoute un film 
- [DEL] ```http://localhost:3200/movies/`<movieid>` ``` -> Supprime un film 
- [PUT] ```http://localhost:3200/movies/`<movieid>`/`<rate>` ``` -> Modifie la note d'un film à partir de son id
    
    
