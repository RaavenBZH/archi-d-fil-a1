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
  
