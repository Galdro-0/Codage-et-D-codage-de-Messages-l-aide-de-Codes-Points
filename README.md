Rapport de Projet : Codage et Décodage de Messages à l'aide de Codes à Points

1. Introduction
Le projet consiste à concevoir et développer une application en Python pour encoder et décoder des messages texte en utilisant des codes à points. Les codes à points sont des matrices de points colorés qui représentent chaque caractère d'un alphabet. Ce rapport présente la conception, l'implémentation et les fonctionnalités de l'application développée.
2. Objectifs
Encoder des messages texte en utilisant des codes à points.
Décoder des messages encodés en codes à points pour retrouver le texte original.
Fournir une interface utilisateur intuitive pour encoder, décoder et visualiser les messages.
Générer, charger et sauvegarder des dictionnaires de codage personnalisés.
Sauvegarder les images encodées et analyser les images pour les décoder.
3. Conception de l'Application
3.1 Architecture
L'application est développée en utilisant la bibliothèque Tkinter pour l'interface utilisateur et Matplotlib pour la visualisation des codes à points. Elle est structurée en deux parties principales :
Interface Utilisateur : Une fenêtre principale avec des panneaux de contrôle et d'affichage.
Logique de Codage/Décodage : Les fonctions pour encoder et décoder les messages, gérer les dictionnaires de codage, et sauvegarder les images.
3.2 Interface Utilisateur
L'interface utilisateur est divisée en deux sections :
Panneau de Contrôle : Permet à l'utilisateur d'encoder et de décoder des messages, de gérer les dictionnaires de codage, et de sauvegarder les images.
Panneau d'Affichage : Affiche les matrices de points encodées et les résultats du décodage.
 
3.3 Fonctionnalités Clés
Génération de Dictionnaire : Génère un dictionnaire de codage aléatoire pour l'alphabet spécifié.
Chargement et Sauvegarde de Dictionnaire : Permet de charger et de sauvegarder des dictionnaires de codage en format JSON.
Encodage de Messages : Convertit un texte en une série de matrices de points.
Décodage de Messages : Analyse les matrices de points pour retrouver le texte original.
Sauvegarde d'Images : Sauvegarde les images encodées en format PNG ou JPEG.
Analyse d'Images : Analyse les images pour extraire les matrices de points et les décoder.
4. Implémentation
4.1 Génération de Dictionnaire
Le dictionnaire de codage est généré de manière aléatoire en attribuant une matrice de points unique à chaque caractère de l'alphabet. Les matrices sont composées de points colorés qui peuvent être noirs, blancs, gris, rouges, verts ou bleus.
 
4.2 Encodage de Messages
Le texte est encodé en remplaçant chaque caractère par sa matrice de points correspondante. Les espaces sont représentés par des matrices vides.
4.3 Décodage de Messages
Le décodage est réalisé en analysant les matrices de points pour retrouver les caractères correspondants dans le dictionnaire de codage. Les matrices sont extraites de l'image et comparées avec les matrices du dictionnaire.
4.4 Sauvegarde et Chargement de Dictionnaire
Les dictionnaires de codage sont sauvegardés et chargés en format JSON pour une gestion facile des configurations de codage.
4.5 Sauvegarde d'Images
Les images encodées sont sauvegardées en format PNG ou JPEG pour une utilisation ultérieure.
 
5. Résultats
5.1 Exemple d'Encodage
Un exemple de texte encodé est illustré ci-dessous. Chaque caractère est représenté par une matrice de points unique.
 
5.2 Exemple de Décodage
Un exemple de décodage est illustré ci-dessous. Les matrices de points sont analysées pour retrouver le texte original.
 
6. Conclusion
Le projet a réussi à développer une application complète pour encoder et décoder des messages texte en utilisant des codes à points. L'application offre une interface utilisateur intuitive et des fonctionnalités avancées pour la gestion des dictionnaires de codage et la sauvegarde des images. Les résultats obtenus démontrent l'efficacité du système de codage à points.
7. Perspectives d'Amélioration
Optimisation de la Reconnaissance de Points : Améliorer l'algorithme d'analyse des images pour une meilleure précision.
Support de Plus de Caractères : Étendre le dictionnaire de codage pour inclure des caractères spéciaux et des langues non latines.
Interface Multilingue : Ajouter une interface multilingue pour une utilisation internationale.
## Contributeurs
- [Galdro-0](https://github.com/Galdro-0)
- [Hamza-El-Mourabit](https://github.com/Hamza-El-Mourabit)

