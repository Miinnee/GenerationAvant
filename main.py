import os
import requests
import tkinter as tk
from tkinter import PhotoImage, StringVar, OptionMenu

import uuid
from PIL import Image, ImageTk

# Définir les dossiers pour stocker les images
os.makedirs("images", exist_ok=True)
os.makedirs("images/accept", exist_ok=True)
os.makedirs("images/refuse", exist_ok=True)
os.makedirs("images/generated", exist_ok=True)

listGenre = ["Homme", "Femme"]
listTrancheAge = ["Jeune", "Adulte", "Agee"]

def generate_id(prefix="", length=None):
    unique_id = str(uuid.uuid4()).replace("-", "")  # Génère un UUID et supprime les tirets
    if length:
        unique_id = unique_id[:max(length - len(prefix), 0)]  # Limite la longueur de l'UUID
    return f"{prefix}{unique_id}"

def download_images():
    """
    Télécharge 10 images depuis un site générateur d'images et les enregistre localement.
    """
    os.makedirs("images", exist_ok=True)  # Crée le dossier "images" s'il n'existe pas
    os.makedirs("images/generated", exist_ok=True)
    for i in range(10):
        url = "https://thispersondoesnotexist.com/"
        response = requests.get(url)
        if response.status_code == 200:
            file_path = os.path.join("images/generated", generate_id("image_", 15) + ".jpg")
            with open(file_path, "wb") as f:
                f.write(response.content)
        else:
            print(f"Échec du téléchargement (statut {response.status_code}) pour l'image {i+1}")

download_images()

# Interface graphique principale
class ImageSorterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Sorter")

        self.image_files = [f"images/generated/{file}" for file in os.listdir("images/generated") if file.endswith(".jpg")]
        self.current_image_index = 0

        self.genre_var = StringVar(root)
        self.genre_var.set(listGenre[0])
        self.age_var = StringVar(root)
        self.age_var.set(listTrancheAge[0])

        self.img_label = tk.Label(root)
        self.img_label.pack()

        self.genre_menu = OptionMenu(root, self.genre_var, *listGenre)
        self.genre_menu.pack(side=tk.LEFT, padx=20, pady=20)

        self.age_menu = OptionMenu(root, self.age_var, *listTrancheAge)
        self.age_menu.pack(side=tk.LEFT, padx=20, pady=20)

        self.accept_button = tk.Button(root, text="Accepter", command=self.accept_image)
        self.accept_button.pack(side=tk.LEFT, padx=20, pady=20)

        self.refuse_button = tk.Button(root, text="Refuser", command=self.refuse_image)
        self.refuse_button.pack(side=tk.RIGHT, padx=20, pady=20)

        self.display_image()

    def display_image(self):
        if self.current_image_index < len(self.image_files):
            img_path = self.image_files[self.current_image_index]
            image = Image.open(img_path)
            image = image.resize((400, 400))
            self.tk_image = ImageTk.PhotoImage(image)
            self.img_label.config(image=self.tk_image)
        else:
            self.img_label.config(text="Toutes les images ont été triées.")
            self.accept_button.config(state=tk.DISABLED)
            self.refuse_button.config(state=tk.DISABLED)

    def accept_image(self):
        if self.current_image_index < len(self.image_files):
            genre = self.genre_var.get()
            age = self.age_var.get()
            img_path = self.image_files[self.current_image_index]
            accept_folder = "images/accept"
            new_index = len([name for name in os.listdir(accept_folder) if os.path.isfile(os.path.join(accept_folder, name))]) + 1
            new_name = f"{accept_folder}/{genre}_{age}_{new_index}.jpg"
            os.rename(img_path, new_name)
            self.current_image_index += 1
            self.display_image()

    def refuse_image(self):
        if self.current_image_index < len(self.image_files):
            img_path = self.image_files[self.current_image_index]
            refuse_folder = "images/refuse"
            new_name = f"{refuse_folder}/image_" + generate_id("", 15) + ".jpg"
            os.rename(img_path, new_name)
            self.current_image_index += 1
            self.display_image()

# Fenêtre de sélection de l'application
class AppSelector:
    def __init__(self, root):
        self.root = root
        self.root.title("Choix de l'application")

        self.label = tk.Label(root, text="Sélectionnez une application :")
        self.label.pack(pady=20)

        self.app_var = StringVar(root)
        self.app_var.set("Accepter/Refuser")
        self.app_menu = OptionMenu(root, self.app_var, "Accepter/Refuser", "Application de tri")

        self.label = tk.Label(root, text="Il y a actuellement ")
        self.label.pack(pady=20)


        self.app_menu.pack(pady=20)

        self.start_button = tk.Button(root, text="Lancer", command=self.launch_app)
        self.start_button.pack(pady=20)

    def launch_app(self):
        selected_app = self.app_var.get()

        if selected_app == "Accepter/Refuser":
            self.root.destroy()
            main_app = tk.Tk()
            ImageSorterApp(main_app)
            main_app.mainloop()
        else:
            print("Autre application sélectionnée. Implémentation à venir.")

# Créer la fenêtre principale et lancer la fenêtre de sélection
if __name__ == "__main__":
    root = tk.Tk()
    AppSelector(root)
    root.mainloop()
