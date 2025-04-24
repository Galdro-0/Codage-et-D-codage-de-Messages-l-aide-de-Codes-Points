import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
import matplotlib.pyplot as plt#
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.patches import Circle, Rectangle
import random
import json
import os

# Couleurs disponibles avec RGB
COULEURS = {
    'noir': [0, 0, 0],
    'blanc': [1, 1, 1],
    'none': [0.9, 0.9, 0.9],#gris clair
    'rouge': [1, 0, 0],
    'vert': [0, 1, 0],
    'gris': [0.5, 0.5, 0.5],
    'bleu': [0, 0, 1]
}

class CodagePointsApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Codage à Points")
        self.root.geometry("1100x700")
        
        # Paramètres
        # Chaîne contenant les lettres à encoder (majuscules et minuscules)
        self.alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
        # Ce dictionnaire servira à associer chaque lettre à une matrice de couleurs
        self.dico = None
        self.point_radius = 0.4
        self.matrices_par_ligne = 15
        self.last_matrices = None
        
        # Interface
        self.create_widgets()
    
    def create_widgets(self):
        # Frame principal
        main_frame = ttk.Frame(self.root, padding=10)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Panneau de contrôle (gauche)
        control_frame = ttk.Frame(main_frame, padding=5, relief="ridge", borderwidth=1)
        control_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 5))
        
        # Titre
        ttk.Label(control_frame, text="Codage à Points", font=('Arial', 12, 'bold')).pack(pady=(0, 10))
        
        # Zone de texte
        ttk.Label(control_frame, text="Texte à encoder:").pack(anchor=tk.W)
        self.text_input = scrolledtext.ScrolledText(control_frame, width=30, height=5, wrap=tk.WORD)
        self.text_input.pack(fill=tk.X, pady=(0, 10))
        self.text_input.insert(tk.END, "Hello World")
        
        # Boutons dictionnaire
        dict_frame = ttk.Frame(control_frame)
        dict_frame.pack(fill=tk.X, pady=(0, 10))
        ttk.Button(dict_frame, text="Générer dictionnaire", command=self.generer_dictionnaire).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(dict_frame, text="Charger", command=self.charger_dictionnaire).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(dict_frame, text="Sauvegarder", command=self.sauvegarder_dictionnaire).pack(side=tk.LEFT)
        
        # Options d'affichage
        ttk.Label(control_frame, text="Options d'affichage:", font=('Arial', 12, 'bold')).pack(anchor=tk.W, pady=(10, 5))
        
        # Taille des points
        size_frame = ttk.Frame(control_frame)
        size_frame.pack(fill=tk.X, pady=(0, 5))
        ttk.Label(size_frame, text="Taille des points:").pack(side=tk.LEFT)
        self.radius_var = tk.DoubleVar(value=0.4)
        ttk.Scale(size_frame, from_=0.2, to=0.6, variable=self.radius_var, 
                 command=lambda _: self.actualiser_parametres()).pack(side=tk.RIGHT, fill=tk.X, expand=True)
        
        # Matrices par ligne
        mpl_frame = ttk.Frame(control_frame)
        mpl_frame.pack(fill=tk.X, pady=(0, 10))
        ttk.Label(mpl_frame, text="Matrices par ligne:").pack(side=tk.LEFT)
        self.mpl_var = tk.IntVar(value=15)
        ttk.Scale(mpl_frame, from_=5, to=25, variable=self.mpl_var,
                 command=lambda _: self.actualiser_parametres()).pack(side=tk.RIGHT, fill=tk.X, expand=True)
        
        # Boutons d'action
        ttk.Button(control_frame, text="Encoder et afficher", command=self.encoder_afficher).pack(fill=tk.X, pady=(10, 5))
        ttk.Button(control_frame, text="Sauvegarder l'image", command=self.sauvegarder_image).pack(fill=tk.X, pady=(0, 5))
        ttk.Button(control_frame, text="Décoder l'image", command=self.decoder_afficher).pack(fill=tk.X, pady=(0, 10))
        
        # Statut
        self.status_var = tk.StringVar(value="Prêt")
        ttk.Label(control_frame, textvariable=self.status_var, relief="sunken", anchor=tk.W).pack(fill=tk.X, side=tk.BOTTOM, pady=(10, 0))
        
        # Panneau d'affichage (droite)
        display_frame = ttk.Frame(main_frame, padding=5)
        display_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Figure matplotlib
        self.fig, self.ax = plt.subplots(figsize=(10, 8))
        self.canvas = FigureCanvasTkAgg(self.fig, master=display_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Message initial
        self.ax.text(0.5, 0.5, "Encodez un texte pour afficher le résultat", ha='center', va='center', fontsize=12)
        self.ax.set_xlim(0, 1)
        self.ax.set_ylim(0, 1)
        self.ax.axis('off')
        self.canvas.draw()
    
    def actualiser_parametres(self, *args):
        """Met à jour l'affichage quand les paramètres changent"""
        if self.last_matrices:
            self.point_radius = self.radius_var.get()
            self.matrices_par_ligne = self.mpl_var.get()
            self.afficher_matrices(self.last_matrices)
    
    def creer_dictionnaire(self, alphabet):
        """ Crée un dictionnaire de codage aléatoire pour les caractères de l'alphabet.
            Chaque caractère (insensible à la casse) se voit attribuer une matrice de points colorés unique."""
        dico = {}
        deja_utilise = set()
        chars_uniques = set()
        char_mapping = {}
        
        # Identifier les caractères uniques
        for char in alphabet:
            char_lower = char.lower() if char.isalpha() else char
            chars_uniques.add(char_lower)
            char_mapping[char] = char_lower
        
        # Créer une matrice pour chaque caractère unique
        matrices = {}
        for char in chars_uniques:
            while True:
                matrice = tuple((i, j, random.choice(list(COULEURS.keys()))) for i in range(3) for j in range(3))
                if matrice not in deja_utilise:
                    deja_utilise.add(matrice)
                    matrices[char] = matrice
                    break
        
        # Assigner les matrices aux caractères originaux
        for char in alphabet:
            dico[char] = matrices[char_mapping[char]]
        
        return dico
    
    def generer_dictionnaire(self):
        """Génère un nouveau dictionnaire de codage"""
        try:
            self.dico = self.creer_dictionnaire(self.alphabet)
            self.status_var.set(f"Dictionnaire généré pour {len(self.alphabet)} caractères")
            messagebox.showinfo("Succès", "Dictionnaire de codage généré avec succès!")
        except Exception as e:
            self.status_var.set(f"Erreur: {str(e)}")
            messagebox.showerror("Erreur", f"Impossible de générer le dictionnaire: {str(e)}")
    
    def charger_dictionnaire(self):
        """Charge un dictionnaire depuis un fichier JSON"""
        try:
            file_path = filedialog.askopenfilename(
                title="Charger un dictionnaire",
                filetypes=[("Fichiers JSON", ".json"), ("Tous les fichiers", ".*")]
            )
            if not file_path:
                return
            
            with open(file_path, 'r') as f:
                data = json.load(f)
                # Conversion des listes en tuples
                self.dico = {}
                for char, matrix_list in data.items():
                    self.dico[char] = tuple(tuple(item) for item in matrix_list)
            
            self.status_var.set(f"Dictionnaire chargé depuis {os.path.basename(file_path)}")
            messagebox.showinfo("Succès", "Dictionnaire chargé avec succès!")
        except Exception as e:
            self.status_var.set(f"Erreur: {str(e)}")
            messagebox.showerror("Erreur", f"Impossible de charger le dictionnaire: {str(e)}")
    
    def sauvegarder_dictionnaire(self):
        """Sauvegarde le dictionnaire dans un fichier JSON"""
        if not self.dico:
            messagebox.showwarning("Attention", "Aucun dictionnaire à sauvegarder. Générez d'abord un dictionnaire.")
            return
        
        try:
            file_path = filedialog.asksaveasfilename(
                title="Sauvegarder le dictionnaire",
                defaultextension=".json",
                filetypes=[("Fichiers JSON", ".json"), ("Tous les fichiers", ".*")]
            )
            if not file_path:
                return
            
            # Conversion des tuples en listes pour la sérialisation JSON
            serializable_dict = {char: [list(item) for item in matrix] for char, matrix in self.dico.items()}
            
            with open(file_path, 'w') as f:
                json.dump(serializable_dict, f, indent=2)
            
            self.status_var.set(f"Dictionnaire sauvegardé dans {os.path.basename(file_path)}")
            messagebox.showinfo("Succès", "Dictionnaire sauvegardé avec succès!")
        except Exception as e:
            self.status_var.set(f"Erreur: {str(e)}")
            messagebox.showerror("Erreur", f"Impossible de sauvegarder le dictionnaire: {str(e)}")
    
    def encoder_afficher(self):
        """Encode le texte et affiche le résultat"""
        texte = self.text_input.get("1.0", tk.END).strip()
        if not texte:
            messagebox.showwarning("Attention", "Veuillez entrer un texte à encoder.")
            return
        
        if not self.dico:
            if messagebox.askyesno("Dictionnaire manquant", 
                                  "Aucun dictionnaire n'a été généré. Voulez-vous en générer un maintenant?"):
                self.generer_dictionnaire()
            else:
                return
        
        try:
            # Mise à jour des paramètres
            self.point_radius = self.radius_var.get()
            self.matrices_par_ligne = self.mpl_var.get()
            
            # Encoder le texte en remplaçant les espaces par None
            matrices = [None if c == ' ' else self.dico.get(c) for c in texte]
            self.last_matrices = matrices  # Sauvegarder pour réafficher
            
            # Affichage
            self.afficher_matrices(matrices)
            
            # Mise à jour du statut
            nb_espaces = texte.count(' ')
            self.status_var.set(f"Texte encodé: {len(texte) - nb_espaces} caractères avec {nb_espaces} espaces")
        except Exception as e:
            self.status_var.set(f"Erreur: {str(e)}")
            messagebox.showerror("Erreur", f"Impossible d'encoder le texte: {str(e)}")
    
    def afficher_matrices(self, matrices):
        """Affiche les matrices de points"""
        # Réinitialiser la figure
        self.ax.clear()
        self.ax.set_aspect('equal')
        self.ax.invert_yaxis()  # (0,0) en haut à gauche
        
        # Paramètres d'affichage
        espacement = 3.5
        
        # Dimensions
        nb_lignes = (len(matrices) - 1) // self.matrices_par_ligne + 1
        self.ax.set_xlim(-1, self.matrices_par_ligne * espacement + 1)
        self.ax.set_ylim(-1, nb_lignes * espacement + 1)
        self.ax.axis('off')
        
        # Statistiques
        nb_caracteres = sum(1 for m in matrices if m is not None)
        nb_espaces = sum(1 for m in matrices if m is None)
        self.ax.set_title(f"Codage à points: {nb_caracteres} caractères avec {nb_espaces} espaces", fontsize=14, pad=10)
        
        # Dessiner les matrices
        for idx, matrice in enumerate(matrices):
            col = idx % self.matrices_par_ligne
            row = idx // self.matrices_par_ligne
            x_base = col * espacement
            y_base = row * espacement
            
            # Dessiner le cadre
            is_space = matrice is None
            rect_props = {
                'xy': (x_base - 0.5, y_base - 0.5),
                'width': 3, 'height': 3,
                'fill': is_space,
                'edgecolor': 'gray',
                'linestyle': '-',
                'linewidth': 0.5,
                'alpha': 0.1 if is_space else 0.3
            }
            if is_space:
                rect_props['facecolor'] = 'lightgray'
            
            self.ax.add_patch(Rectangle(**rect_props))
            
            # Si c'est un espace
            if is_space:
                self.ax.text(x_base + 1, y_base + 1.5, "⎵", 
                           ha='center', va='center', fontsize=14, color='black', alpha=0.7)
            # Sinon, dessiner les points
            elif matrice:
                for i, j, couleur in matrice:
                    x = x_base + j
                    y = y_base + i
                    
                    # Ombre pour effet 3D
                    if couleur not in ['none', 'blanc']:
                        self.ax.add_patch(Circle((x + 0.05, y + 0.05), self.point_radius,
                                              color='black', alpha=0.2))
                    
                    # Point principal
                    circle_props = {
                        'xy': (x, y),
                        'radius': self.point_radius,
                        'facecolor': COULEURS[couleur]
                    }
                    if couleur in ['blanc', 'none']:
                        circle_props['edgecolor'] = '#333333'
                        circle_props['linewidth'] = 0.5
                    
                    self.ax.add_patch(Circle(**circle_props))
        
        # Quadrillage optionnel
        for x in range(0, int(self.matrices_par_ligne * espacement) + 1, int(espacement)):
            self.ax.axvline(x - 0.5, color='gray', linestyle='-', linewidth=0.5, alpha=0.3)
        for y in range(0, int(nb_lignes * espacement) + 1, int(espacement)):
            self.ax.axhline(y - 0.5, color='gray', linestyle='-', linewidth=0.5, alpha=0.3)
        
        # Mettre à jour le canvas
        self.canvas.draw()
    
    def sauvegarder_image(self):
        """Sauvegarde l'image affichée"""
        try:
            file_path = filedialog.asksaveasfilename(
                title="Sauvegarder l'image",
                defaultextension=".png",
                filetypes=[("Images PNG", ".png"), ("Images JPEG", ".jpg"), ("Tous les fichiers", ".")]
            )
            if not file_path:
                return
            
            self.fig.savefig(file_path, dpi=300, bbox_inches='tight')
            self.status_var.set(f"Image sauvegardée dans {os.path.basename(file_path)}")
            messagebox.showinfo("Succès", "Image sauvegardée avec succès!")
        except Exception as e:
            self.status_var.set(f"Erreur: {str(e)}")
            messagebox.showerror("Erreur", f"Impossible de sauvegarder l'image: {str(e)}")

    def analyser_image(self):
        """Analyse l'image affichée pour extraire les matrices de points"""
        try:
            # Paramètres de la grille
            espacement = 3.5
            marge_erreur = 0.3  # Tolérance pour la position des points
            
            # Récupérer tous les éléments du dessin
            patches = self.ax.patches
            matrices_dict = {}
            
            # 1. D'abord trouver tous les rectangles pour localiser les matrices
            rectangles = [p for p in patches if isinstance(p, Rectangle)]
            
            for rect in rectangles:
                x, y = rect.get_xy()
                width, height = rect.get_width(), rect.get_height()
                
                # Vérifier si c'est un cadre de matrice (3x3)
                if abs(width - 3) < 0.1 and abs(height - 3) < 0.1:
                    col = round((x + 0.5) / espacement)
                    row = round((y + 0.5) / espacement)
                    matrices_dict[(row, col)] = {}
            
            # 2. Ensuite analyser les cercles
            cercles = [p for p in patches if isinstance(p, Circle) and (not hasattr(p, 'get_alpha') or p.get_alpha() != 0.2)]
            
            for cercle in cercles:
                x, y = cercle.get_center()
                facecolor = cercle.get_facecolor()[:3]  # Ignorer alpha
                
                # Trouver la matrice la plus proche
                found = False
                for (row, col), points in matrices_dict.items():
                    x_base = col * espacement
                    y_base = row * espacement
                    
                    # Vérifier si dans cette matrice
                    if (x_base - marge_erreur <= x <= x_base + 3 + marge_erreur and 
                        y_base - marge_erreur <= y <= y_base + 3 + marge_erreur):
                        
                        # Position dans la matrice
                        i = round(y - y_base)
                        j = round(x - x_base)
                        
                        # Trouver la couleur la plus proche
                        min_dist = float('inf')
                        best_color = 'none'
                        for name, rgb in COULEURS.items():
                            dist = sum((fc - c)**2 for fc, c in zip(facecolor, rgb))
                            if dist < min_dist:
                                min_dist = dist
                                best_color = name
                        
                        matrices_dict[(row, col)][(i, j)] = best_color
                        found = True
                        break
                
                if not found:
                    print(f"Point orphelin à ({x:.2f}, {y:.2f})")
            
            # 3. Convertir en liste ordonnée
            if not matrices_dict:
                return []
            
            max_row = max(k[0] for k in matrices_dict.keys())
            max_col = max(k[1] for k in matrices_dict.keys())
            matrices = []
            
            for row in range(max_row + 1):
                for col in range(max_col + 1):
                    if (row, col) in matrices_dict:
                        # Construire la matrice 3x3
                        matrice = []
                        for i in range(3):
                            for j in range(3):
                                color = matrices_dict[(row, col)].get((i, j), 'none')
                                matrice.append((i, j, color))
                        matrices.append(tuple(matrice))
                    else:
                        matrices.append(None)
            
            return matrices
        
        except Exception as e:
            self.status_var.set(f"Erreur d'analyse: {str(e)}")
            messagebox.showerror("Erreur", f"Impossible d'analyser l'image: {str(e)}")
            return []

    def decoder_matrices(self, matrices):
        """Décode une liste de matrices en texte"""
        if not self.dico:
            messagebox.showwarning("Attention", "Aucun dictionnaire disponible pour décoder.")
            return ""
        
        texte = []
        for matrice in matrices:
            if matrice is None:  # Espace
                texte.append(' ')
                continue
            
            # Convertir la matrice en format comparable
            matrice_tuple = tuple(tuple(item) for item in matrice)
            
            # Trouver le caractère correspondant à la matrice
            found = False
            for char, code in self.dico.items():
                if tuple(tuple(item) for item in code) == matrice_tuple:
                    texte.append(char)
                    found = True
                    break
            
            if not found:
                texte.append('?')  # Caractère inconnu
        
        return ''.join(texte)

    def decoder_afficher(self):
        """Décode l'image affichée et montre le résultat"""
        if not self.dico:
            messagebox.showwarning("Attention", "Aucun dictionnaire chargé. Chargez ou générez un dictionnaire d'abord.")
            return
        
        matrices = self.analyser_image()
        if not matrices:
            messagebox.showwarning("Attention", "Aucune matrice trouvée à décoder.")
            return
        
        texte_decode = self.decoder_matrices(matrices)
        
        # Afficher le résultat dans une nouvelle fenêtre
        fenetre_resultat = tk.Toplevel(self.root)
        fenetre_resultat.title("Résultat du décodage")
        
        frame = ttk.Frame(fenetre_resultat, padding=10)
        frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(frame, text="Texte décodé:", font=('Arial', 12, 'bold')).pack(anchor=tk.W)
        
        text_output = scrolledtext.ScrolledText(frame, width=50, height=10, wrap=tk.WORD)
        text_output.pack(fill=tk.BOTH, expand=True)
        text_output.insert(tk.END, texte_decode)
        text_output.config(state=tk.DISABLED)
        
        ttk.Button(frame, text="Fermer", command=fenetre_resultat.destroy).pack(pady=(10, 0))

# Lancement de l'application
if __name__ == "__main__":
    root = tk.Tk()
    app = CodagePointsApp(root)
    root.mainloop()