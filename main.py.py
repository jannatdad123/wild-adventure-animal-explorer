import tkinter as tk
from tkinter import messagebox
import pygame
from PIL import Image
import re
import csv
import os

#  PATH SETUP 
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATA_DIR = os.path.join(BASE_DIR, "data")
IMAGE_DIR = os.path.join(BASE_DIR, "assets", "images")
AUDIO_DIR = os.path.join(BASE_DIR, "assets", "audio")

USERS_FILE = os.path.join(DATA_DIR, "users.csv")
ANIMALS_FILE = os.path.join(DATA_DIR, "animals.csv")

os.makedirs(DATA_DIR, exist_ok=True)

# DATA SETUP
if not os.path.exists(USERS_FILE):
    with open(USERS_FILE, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Username", "Password", "Email"])

animals_data = [
    ["Cat", "Black, White, Brown", "Eyes, Nose, Skin, Tongue, Ear", "Gives birth to babies", "3-4 kg", "Carnivore", "cat.jpg", "cat.mp3.mp3"],
    ["Dog", "Black, Brown, White", "Eyes, Nose, Skin, Tongue, Ear", "Gives birth to babies", "45 kg", "Omnivore", "dog.png", "dog.mp3.mp3"],
    ["Monkey", "Black, White, Light Brown", "Eyes, Nose, Skin, Tongue, Ear", "Gives birth to babies", "Varies by species", "Omnivore", "monkey.jpeg", "monkey.mp3.mp3"],
    ["Parrot", "Blue, Green, Yellow, Multicolor", "Eyes, Taste, Smell, Hearing", "Lays eggs", "30-40 grams", "Herbivore", "parrot.jpeg", "parrot.mp3.mp3"],
    ["Owl", "Black, Brown", "Eyes, Hearing", "Lays eggs", "40 grams", "Carnivore", "owl.jpg", "owl.mp3.mp3"],
    ["Frog", "Green, Grey, Light Brown", "Eyes, Ear, Taste Buds, Nasal Organs", "Lays eggs", "22 grams", "Insects", "frog.jpg", "frog.mp3.mp3"],
    ["Lizard", "Green, Light Brown", "Jacobson's Organ", "Lays eggs", "Varies by species", "Insectivore / Carnivore", "lizard.jpg", "lizard.mp3.mp3"],
    ["Python Snake", "Brown, Green, Yellow", "Skin, Tongue, Heat Sensing", "Lays eggs", "1-5 kg", "Carnivore", "snake.jpeg", "snake.mp3.mp3"],
    ["Bees", "Brown Band, Golden Yellow", "Antennae", "Lays eggs", "80-120 mg", "Nectar", "bees.jpeg", "bees.mp3.mp3"],
]

if not os.path.exists(ANIMALS_FILE):
    with open(ANIMALS_FILE, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([
            "Animal Name", "Color", "Sensory Organs", "Reproduction Method",
            "Weight", "Diet", "Image File", "Sound File"
        ])
        writer.writerows(animals_data)


#  MAIN APP 
class AnimalApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Wild Adventure - Animal Kingdom Explorer")
        self.geometry("520x440")
        self.resizable(False, False)
        self.current_frame = None
        self.switch_frame(LoginFrame)

    def switch_frame(self, frame_class):
        new_frame = frame_class(self)

        if self.current_frame is not None:
            self.current_frame.destroy()

        self.current_frame = new_frame
        self.current_frame.pack(fill="both", expand=True)


# SIGNUP FRAME 
class SignupFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg="#f0f0f0")
        self.master = master

        tk.Label(self, text="Create Account", font=("Helvetica", 18, "bold"), bg="#f0f0f0").pack(pady=15)

        self.username_entry = self.create_input("Username")
        self.password_entry = self.create_input("Password", show="*")
        self.email_entry = self.create_input("Email")

        tk.Button(self, text="Sign Up", command=self.register_user, bg="#4CAF50", fg="white",
                  font=("Helvetica", 12), width=25).pack(pady=10)

        tk.Button(self, text="Back to Login", command=lambda: self.master.switch_frame(LoginFrame),
                  bg="#008CBA", fg="white", font=("Helvetica", 12), width=25).pack()

    def create_input(self, label, show=None):
        tk.Label(self, text=label, bg="#f0f0f0", font=("Helvetica", 11)).pack()
        entry = tk.Entry(self, font=("Helvetica", 12), show=show, width=30)
        entry.pack(pady=5)
        return entry

    def register_user(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        email = self.email_entry.get().strip()

        if not username or not password or not email:
            messagebox.showerror("Error", "Please fill in all fields.")
            return

        if not re.match(r"^[a-zA-Z0-9]+$", username):
            messagebox.showerror("Error", "Username must be alphanumeric.")
            return

        if not re.match(r"^(?=.*[A-Z])(?=.*\d).{8,15}$", password):
            messagebox.showerror("Error", "Password must be 8-15 characters long and contain at least one uppercase letter and one number.")
            return

        if not re.match(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", email):
            messagebox.showerror("Error", "Invalid email address.")
            return

        with open(USERS_FILE, "a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([username, password, email])

        messagebox.showinfo("Success", "Account created successfully!")
        self.master.switch_frame(LoginFrame)


#  LOGIN FRAME 
class LoginFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg="#f0f0f0")
        self.master = master

        tk.Label(self, text="Wild Adventure", font=("Helvetica", 20, "bold"), bg="#f0f0f0").pack(pady=20)
        tk.Label(self, text="Animal Kingdom Explorer", font=("Helvetica", 12), bg="#f0f0f0").pack(pady=5)

        self.username_entry = self.create_input("Username")
        self.password_entry = self.create_input("Password", show="*")

        tk.Button(self, text="Login", command=self.validate_login, bg="#4CAF50", fg="white",
                  font=("Helvetica", 12), width=25).pack(pady=10)

        tk.Button(self, text="Sign Up", command=lambda: self.master.switch_frame(SignupFrame),
                  bg="#008CBA", fg="white", font=("Helvetica", 12), width=25).pack()

    def create_input(self, label, show=None):
        tk.Label(self, text=label, bg="#f0f0f0", font=("Helvetica", 11)).pack()
        entry = tk.Entry(self, font=("Helvetica", 12), show=show, width=30)
        entry.pack(pady=5)
        return entry

    def validate_login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        if not username or not password:
            messagebox.showerror("Error", "Please fill in all fields.")
            return

        with open(USERS_FILE, "r", newline="") as file:
            reader = csv.reader(file)
            next(reader)

            for row in reader:
                if len(row) >= 2 and row[0] == username and row[1] == password:
                    self.master.switch_frame(MainMenuFrame)
                    return

        messagebox.showerror("Error", "Invalid username or password.")


# MAIN MENU 
class MainMenuFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg="#f0f0f0")
        self.master = master

        tk.Label(self, text="Main Menu", font=("Helvetica", 18, "bold"), bg="#f0f0f0").pack(pady=15)
        tk.Label(self, text="Select an animal category", font=("Helvetica", 11), bg="#f0f0f0").pack(pady=5)

        categories = [
            ("Mammals", MammalFrame),
            ("Aves", AvesFrame),
            ("Amphibians", AmphibianFrame),
            ("Reptiles", ReptileFrame),
            ("Insects", InsectFrame),
        ]

        for text, frame in categories:
            tk.Button(self, text=text, command=lambda f=frame: self.master.switch_frame(f),
                      bg="#4CAF50", fg="white", font=("Helvetica", 12), width=25).pack(pady=5)

        tk.Button(self, text="Logout", command=lambda: self.master.switch_frame(LoginFrame),
                  bg="#d9534f", fg="white", font=("Helvetica", 12), width=25).pack(pady=15)


#  ANIMAL INFO FRAME 
class AnimalFrame(tk.Frame):
    def __init__(self, master, animal_name, color, sensory_organs, reproduction_method, weight, diet, image_file, sound_file):
        super().__init__(master, bg="#f0f0f0")
        self.master = master
        self.animal_name = animal_name
        self.image_path = os.path.join(IMAGE_DIR, image_file)
        self.sound_path = os.path.join(AUDIO_DIR, sound_file)
        self.sound_timer = None

        tk.Label(self, text=f"{animal_name} Information", font=("Helvetica", 16, "bold"), bg="#f0f0f0").pack(pady=12)

        info = [
            ("Color", color),
            ("Sensory Organs", sensory_organs),
            ("Reproduction Method", reproduction_method),
            ("Weight", weight),
            ("Diet", diet),
        ]

        for label, value in info:
            tk.Label(self, text=f"{label}: {value}", bg="#f0f0f0",
                     font=("Helvetica", 11), wraplength=450, justify="left").pack(pady=3)

        tk.Button(self, text="View Image", command=self.show_image, bg="#4CAF50", fg="white", width=25).pack(pady=8)
        tk.Button(self, text="Play Sound", command=self.play_sound, bg="#4CAF50", fg="white", width=25).pack(pady=3)
        tk.Button(self, text="Back to Menu", command=lambda: self.master.switch_frame(MainMenuFrame),
                  bg="#008CBA", fg="white", width=25).pack(pady=12)

    def show_image(self):
        if not os.path.exists(self.image_path):
            messagebox.showerror("Error", f"Image file not found:\n{self.image_path}")
            return

        img = Image.open(self.image_path)
        img.show()

    def play_sound(self):
        if not os.path.exists(self.sound_path):
            messagebox.showerror("Error", f"Sound file not found:\n{self.sound_path}")
            return

        try:
            pygame.mixer.init()
            pygame.mixer.music.load(self.sound_path)
            pygame.mixer.music.play()
            self.sound_timer = self.after(6000, self.stop_sound)
        except Exception as e:
            messagebox.showerror("Sound Error", f"Could not play sound:\n{e}")

    def stop_sound(self):
        try:
            pygame.mixer.music.stop()
        except Exception:
            pass

        if self.sound_timer:
            self.after_cancel(self.sound_timer)
            self.sound_timer = None


# CATEGORY FRAME
class CategoryFrame(tk.Frame):
    title = "Category"
    animals = []

    def __init__(self, master):
        super().__init__(master, bg="#f0f0f0")
        self.master = master

        tk.Label(self, text=self.title, font=("Helvetica", 16, "bold"), bg="#f0f0f0").pack(pady=15)

        for animal_name, frame_class in self.animals:
            tk.Button(self, text=animal_name, command=lambda f=frame_class: self.master.switch_frame(f),
                      bg="#4CAF50", fg="white", width=25).pack(pady=5)

        tk.Button(self, text="Back", command=lambda: self.master.switch_frame(MainMenuFrame),
                  bg="#008CBA", fg="white", width=25).pack(pady=15)


class MammalFrame(CategoryFrame):
    title = "Mammals"
    animals = [("Cat", lambda master: CatFrame(master)), ("Dog", lambda master: DogFrame(master)), ("Monkey", lambda master: MonkeyFrame(master))]


class AvesFrame(CategoryFrame):
    title = "Aves"
    animals = [("Parrot", lambda master: ParrotFrame(master)), ("Owl", lambda master: OwlFrame(master))]


class AmphibianFrame(CategoryFrame):
    title = "Amphibians"
    animals = [("Frog", lambda master: FrogFrame(master))]


class ReptileFrame(CategoryFrame):
    title = "Reptiles"
    animals = [("Lizard", lambda master: LizardFrame(master)), ("Python Snake", lambda master: SnakeFrame(master))]


class InsectFrame(CategoryFrame):
    title = "Insects"
    animals = [("Bees", lambda master: BeeFrame(master))]


# ================= INDIVIDUAL ANIMAL FRAMES =================
class CatFrame(AnimalFrame):
    def __init__(self, master):
        super().__init__(master, "Cat", "Black, White, Brown", "Eyes, Nose, Skin, Tongue, Ear", "Gives birth to babies", "3-4 kg", "Carnivore", "cat.jpg", "cat.mp3.mp3")


class DogFrame(AnimalFrame):
    def __init__(self, master):
        super().__init__(master, "Dog", "Black, Brown, White", "Eyes, Nose, Skin, Tongue, Ear", "Gives birth to babies", "45 kg", "Omnivore", "dog.png", "dog.mp3.mp3")


class MonkeyFrame(AnimalFrame):
    def __init__(self, master):
        super().__init__(master, "Monkey", "Black, White, Light Brown", "Eyes, Nose, Skin, Tongue, Ear", "Gives birth to babies", "Varies by species", "Omnivore", "monkey.jpeg", "monkey.mp3.mp3")


class ParrotFrame(AnimalFrame):
    def __init__(self, master):
        super().__init__(master, "Parrot", "Blue, Green, Yellow, Multicolor", "Eyes, Taste, Smell, Hearing", "Lays eggs", "30-40 grams", "Herbivore", "parrot.jpeg", "parrot.mp3.mp3")


class OwlFrame(AnimalFrame):
    def __init__(self, master):
        super().__init__(master, "Owl", "Black, Brown", "Eyes, Hearing", "Lays eggs", "40 grams", "Carnivore", "owl.jpg", "owl.mp3.mp3")


class FrogFrame(AnimalFrame):
    def __init__(self, master):
        super().__init__(master, "Frog", "Green, Grey, Light Brown", "Eyes, Ear, Taste Buds, Nasal Organs", "Lays eggs", "22 grams", "Insects", "frog.jpg", "frog.mp3.mp3")


class LizardFrame(AnimalFrame):
    def __init__(self, master):
        super().__init__(master, "Lizard", "Green, Light Brown", "Jacobson's Organ", "Lays eggs", "Varies by species", "Insectivore / Carnivore", "lizard.jpg", "lizard.mp3.mp3")


class SnakeFrame(AnimalFrame):
    def __init__(self, master):
        super().__init__(master, "Python Snake", "Brown, Green, Yellow", "Skin, Tongue, Heat Sensing", "Lays eggs", "1-5 kg", "Carnivore", "snake.jpeg", "snake.mp3.mp3")


class BeeFrame(AnimalFrame):
    def __init__(self, master):
        super().__init__(master, "Bees", "Brown Band, Golden Yellow", "Antennae", "Lays eggs", "80-120 mg", "Nectar", "bees.jpeg", "bees.mp3.mp3")


#  RUN APP 
if __name__ == "__main__":
    app = AnimalApp()
    app.mainloop()