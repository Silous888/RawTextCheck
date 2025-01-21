trois mode :
    code aclios
    par word
    par languageTool
on peut choisir via des cases à cocher lesquelles méthodes on veut
ou avec chacun un bouton, et la date du dernier scan, et ça lancerait dans un thread

mettre les mots exclus dans un sheet avec une page par jeu
les résultats sont hors lignes, et on peut voir de quand ils datent
sur un mot compté comme faute, 
    on peut indiqué comme traité, pour le faire disparaitre, jusqu’à la prochaine vérif s’il n’a pas été traité
    on peut ajouter au dictionnaire

on doit pouvoir choisir les fichiers qu’on veut faire
soit en indiquant directement l’url, soit en proposant une liste

faut pouvoir indiqué les balises à ignorer

le tout avec une interface


peut-être proposer via clic droit pour accepter de modifier la faute automatiquement


pour l’api gooogle sheet, au lieu d’un décorateur, faire une fonction qui prend une fonction et un nombre infini de paramètres et qui fait un try catch en boucle jusqu’à que ça catch plus et qui alors renvoit le résultat de la fonction


pouvoir ajouter soit au dictionnaire des exceptions du jeu, soit au dictionnaire général de la méthode




ajouter un sort automatique de la liste des termes quand on la sauvegarde


le truc de sauvegarder la sheet en mémoire, faut gérer le cas de si on refait la même méthod, après avoir corrigé les fautes
donc charger à nouveau les fautes, et en fait peut-être ne pas sauvegarder du tout
parce que si on fait méthod 1, on corrige les fautes, puis on fait méthode 2, ça va pas prendre en compte les corrections


bug qui fait que je peux faire qu’une fois le check d’orthographe

ajouter un check de caractères qui passe pas dans le jeu, espace insécable, mauvais guillemets...

quand une méthode est fini d’être exécuté, faut mettre sur le tab des résultats automatiquement


faire en sorte de threader le worker si plusieurs signaux sont en même temps