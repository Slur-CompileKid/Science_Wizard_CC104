import tkinter as tk
from playsound import playsound
import random
import time
import os
import threading
from tkinter import ttk
from constants import THEME_FG, BUTTON_BG, BUTTON_FG, ENTRY_BG, ENTRY_HIGHLIGHT, FONT
from dataStructures import Queue, Stack
from PIL import Image, ImageTk, ImageDraw, ImageFont
import pygame

class ScienceWizard:
    def __init__(self, root):
        self.root = root
        self.root.title("Science Wizard")
        self.root.geometry("600x400")

        # Load a different background image for loading
        try:
            self.bg_image = tk.PhotoImage(file='ito.png')  # Different image for loading
            self.bg_image_id = self.canvas.create_image(0, 0, anchor="nw", image=self.bg_image)
        except:
            self.bg_image_id = None

        self.canvas = tk.Canvas(root, width=400, height=600)
        self.canvas.pack(fill="both", expand=True)
        if self.bg_image:
            self.canvas.create_image(0, 0, anchor="nw", image=self.bg_image)

        self.leaderboard_file = 'leaderboard.txt'
        self.leaderboard = self.load_leaderboard()
        self.player_name = ""

        self.word_queue = Queue()
        self.attempt_stack = Stack()

        self.words = [
            {'word': 'cell','definition': 'The basic unit of life in all living organisms.','audio': 'musics1.mp3'},
            {'word': 'nucleus','definition': 'The control center of a cell that contains DNA.','audio': 'musics2.mp3'},
            {'word': 'osmosis', 'definition': 'The movement of water across a membrane from high to low concentration.','audio': 'musics3.mp3'},
            {'word': 'mitochondria','definition': 'Organelles that produce energy for the cell; known as the "powerhouse."','audio': 'musics4.mp3'},
            {'word': 'photosynthesis','definition': 'The process by which plants make food using sunlight, water, and carbon dioxide.','audio': 'musics5.mp3'},
            {'word': 'chlorophyll','definition': 'The green pigment in plants that captures sunlight for photosynthesis.','audio': 'musics6.mp3'},
            {'word': 'enzyme', 'definition': 'A protein that speeds up chemical reactions in the body.','audio': 'musics7.mp3'},
            {'word': 'genetics','definition': 'The study of heredity and how traits are passed from parents to offspring','audio': 'musics8.mp3'},
            {'word': 'mutation', 'definition': 'A change in the DNA sequence that can affect traits.','audio': 'musics9.mp3'},
            {'word': 'ecology','definition': 'The study of how organisms interact with each other and their environment.','audio': 'musics10.mp3'},
            {'word': 'habitat', 'definition': 'The natural home or environment of an organism.', 'audio': 'musics11.mp3'},
            {'word': 'adaptation', 'definition': 'A trait helps an organism survive in its environment.','audio': 'musics12.mp3'},
            {'word': 'species', 'definition': 'A group of organisms survive in its environment.','audio': 'musics13.mp3'},
            {'word': 'vertebrate', 'definition': 'An animal with backbone.', 'audio': 'musics14.mp3'},
            {'word': 'pneumonoultramicroscopicsilicovolcanoconiosis','definition': 'A lung disease caused by inhaling extremely fine silicate or quartz dust, often found near volcanoes or in mining environments.','audio': 'musics15.mp3'},
            {'word': 'atom', 'definition': 'The smallest unit of matter that retains the properties of a chemical element.', 'audio': 'musics16.mp3'},
            {'word': 'molecule', 'definition': 'A group of atoms bonded together, representing the smallest unit of a compound..', 'audio': 'musics17.mp3'},
            {'word': 'element', 'definition': 'A pure substance made of only one type of atom, cannot be broken down chemically.', 'audio': 'musics18.mp3'},
            {'word': 'compound', 'definition': 'A substance formed when two or more different chemical elements are chemically bonded together.', 'audio': 'musics19.mp3'},
            {'word': 'catalyst', 'definition': ' A substance that speeds up a chemical reaction without being consumed.  .', 'audio': 'musics20.mp3'},
            {'word': 'metamorphosis', 'definition': ' A biological process where an animal undergoes a dramatic change in its body structure as it develops from its immature form to its adult stage.', 'audio': 'musics21.mp3'},
            {'word': 'acid', 'definition': 'A chemical that gives off hydrogen ions in water and forms salts by combining with certain metals.', 'audio': 'musics22.mp3'},
            {'word': 'base', 'definition': 'a substance that can accept protons (hydrogen ions) or donate a pair of electrons.', 'audio': 'musics23.mp3'},
            {'word': 'joule', 'definition': 'The standard SI unit of energy used to measure the energy changes in chemical reactions.', 'audio': 'musics24.mp3'},
            {'word': 'electron', 'definition': 'a stable, subatomic particle with a negative charge that orbits the nucleus of an atom.', 'audio': 'musics25.mp3'},
            {'word': 'proton', 'definition': 'A subatomic particle with a positive electric charge that is found in the nucleus of every atom.', 'audio': 'musics26.mp3'},
            {'word': 'neutron', 'definition': 'A a subatomic particle with no electric charge that is found in the nucleus of an atom, along with protons.', 'audio': 'musics27.mp3'},
            {'word': 'solution', 'definition': 'A homogeneous mixture where one or more substances (solutes) are evenly and completely dissolved in another substance (solvent).', 'audio': 'musics28.mp3'},
            {'word': 'evaporation', 'definition': 'The process where a liquid turns into a gas, or vapor, below its boiling point.', 'audio': 'musics29.mp3'},
            {'word': 'berkelium', 'definition': 'A synthetic, highly radioactive chemical element with atomic number 97 and the symbol Bk.', 'audio': 'musics30.mp3'},
        ]

        self.current_word = None
        self.lives = 3
        self.score = 0
        self.correct_words = []
        self.all_inputs = []
        self.current_word_index = 0

        self.music_thread = None
        self.stop_music = False

        self.text_images = {}

        self.progress = ttk.Progressbar(self.canvas, orient="horizontal", length=300, mode="determinate")
        self.canvas.create_window(300, 160, window=self.progress)
        # Set font and font_size for loading text here
        self.loading_text_id = self.create_text_image("Loading...", 300, 190, font="arial.ttf", font_size=15, color=THEME_FG)

        self.root.after(100, self.simulate_loading)

    def create_text_image(self, text, x, y, font="arial.ttf", font_size=12, color=(255, 255, 255), anchor="center"):
        try:
            font_obj = ImageFont.truetype(font, font_size)
        except:
            font_obj = ImageFont.load_default()

        bbox = font_obj.getbbox(text)
        width = bbox[2] - bbox[0]
        height = bbox[3] - bbox[1]

        padding = 50
        img_width = width + padding
        img_height = height + padding

        img = Image.new('RGBA', (img_width, img_height), (0, 0, 0, 0))

        draw = ImageDraw.Draw(img)
        text_x = (img_width - width) // 2
        text_y = (img_height - height) // 2
        draw.text((text_x, text_y), text, fill=color, font=font_obj)

        tk_img = ImageTk.PhotoImage(img)

        img_id = self.canvas.create_image(x, y, anchor=anchor, image=tk_img)

        self.text_images[img_id] = tk_img

        return img_id

    def simulate_loading(self):
        for i in range(101):
            self.progress['value'] = i
            self.root.update_idletasks()
            time.sleep(0.05)
        self.start_background_music()  # Start background music after loading
        self.show_title()

    def show_title(self):
        # Change to a different background image for the title screen
        if self.bg_image_id:
            self.canvas.delete(self.bg_image_id)
        try:
            self.bg_image = tk.PhotoImage(file='naparabang.png')  # Different image for title
            self.bg_image_id = self.canvas.create_image(0, 0, anchor="nw", image=self.bg_image)
        except:
            self.bg_image = None

        # Removed the text creation for "SCIENCE WIZARD"
        self.progress.destroy()
        self.canvas.delete(self.loading_text_id)
        self.root.after(2000, self.show_intro)

    def show_intro(self):
        # Switch back to the original background image for the rest of the program
        if self.bg_image_id:
            self.canvas.delete(self.bg_image_id)
        try:
            self.bg_image = tk.PhotoImage(file='ito.png')  # Original background
            self.bg_image_id = self.canvas.create_image(0, 0, anchor="nw", image=self.bg_image)
        except:
            self.bg_image = None

        # Removed the deletion of title_label_id since it's no longer created
        self.name_label = tk.Label(self.canvas, text="Player's Name:", bg="#001833", fg="white", font="CAMBRIA")
        self.canvas.create_window(300, 30, window=self.name_label)
        self.name_entry = tk.Entry(self.canvas, width=30, bg=ENTRY_BG, fg="black", font=FONT, highlightbackground=ENTRY_HIGHLIGHT, highlightthickness=2)
        self.canvas.create_window(300, 70, window=self.name_entry)

        self.intro_label = tk.Label(self.canvas, text="Welcome to the Spelling Adventure!\n"
                                                      "\nEmbark on a journey through the world of science."
                                                      "\nSpell the words correctly to score points."
                                                      "\nYou have 3 lives (🍃🍃🍃)."
                                                      "\nWrong answers or skips will cost a life.\n"
                                                      "\nGet ready...", wraplength=500, bg="#03045E", fg="white", font=("Century",12))
        self.canvas.create_window(300, 200, window=self.intro_label)
        self.start_button = tk.Button(self.canvas, text="Start Game", command=self.start_intro, bg="#FFD1DC", fg="#D90166", font="CooperBlack")
        self.canvas.create_window(300, 320, window=self.start_button)

    def load_leaderboard(self):
        if os.path.exists(self.leaderboard_file):
            with open(self.leaderboard_file, 'r') as f:
                lines = f.readlines()
                leaderboard = []
                for line in lines:
                    parts = line.strip().split(',')
                    if len(parts) == 2:
                        name, score = parts
                        leaderboard.append((name, int(score)))
                return sorted(leaderboard, key=lambda x: x[1], reverse=True)[:10]
        return []

    def save_leaderboard(self):
        with open(self.leaderboard_file, 'w') as f:
            for name, score in self.leaderboard:
                f.write(f"{name},{score}\n")

    def get_lives_display(self):
        return "🍃" * self.lives

    def start_intro(self):
        self.player_name = self.name_entry.get().strip()
        if not self.player_name:
            self.player_name = "Anonymous"
        self.name_label.destroy()
        self.name_entry.destroy()
        self.intro_label.destroy()
        self.start_button.destroy()

        try:
            playsound('intro.mp3')
        except Exception as e:
            print(f"Error playing intro sound: {e}")

        self.root.after(3000, self.show_game_ui)

    def show_game_ui(self):
        # Removed self.start_background_music() from here since it's now started after loading

        self.title_label = tk.Label(self.canvas, text="SCIENCE WIZARD", bg="#1C2951", fg=THEME_FG, font=("algerian", 15, "bold"))
        self.canvas.create_window(300, 350, window=self.title_label)

        self.word_number_label = tk.Label(self.canvas, text="", bg="#001833", fg=THEME_FG, font=("CAMBRIA",10))
        self.canvas.create_window(50, 20, window=self.word_number_label)
        self.high_score_label = tk.Label(self.canvas, text=f"High Score: {self.get_high_score()}", bg="#001833", fg=THEME_FG, font=("CAMBRIA",10))
        self.canvas.create_window(300, 20, window=self.high_score_label)
        self.lives_label = tk.Label(self.canvas, text=f"Lives: {self.get_lives_display()}", bg="#001833", fg=THEME_FG, font=("CAMBRIA",10))
        self.canvas.create_window(550, 20, window=self.lives_label)
        self.definition_label = tk.Label(self.canvas, text="", wraplength=400, bg="#03045E", fg=THEME_FG, font=("CAMBRIA",12), highlightbackground="#023E8A", highlightthickness=3)
        self.canvas.create_window(300, 100, window=self.definition_label)
        self.play_sound_button = tk.Button(self.canvas, text="Spell", command=self.play_sound, bg="#8A3324", fg=BUTTON_FG, font=("Century", 11))
        self.canvas.create_window(300, 160, window=self.play_sound_button)
        self.entry = tk.Entry(self.canvas, width=30, bg=ENTRY_BG, fg="black", font=FONT, highlightbackground=ENTRY_HIGHLIGHT, highlightthickness=2)
        self.canvas.create_window(300, 210, window=self.entry)
        self.submit_button = tk.Button(self.canvas, text="Submit", command=self.check_answer, bg="#FF6E00", fg=BUTTON_FG, font=("Century",11))
        self.canvas.create_window(250, 250, window=self.submit_button)
        self.skip_button = tk.Button(self.canvas, text="Skip", command=self.skip_word, bg="#363636", fg=BUTTON_FG, font=("Century",11))
        self.canvas.create_window(350, 250, window=self.skip_button)

        self.start_game()

    def get_high_score(self):
        if self.leaderboard:
            return self.leaderboard[0][1]
        return 0

    def start_background_music(self):
        pygame.mixer.init()  # Initialize pygame mixer
        self.music_thread = threading.Thread(target=self.play_background_music)
        self.music_thread.start()
    def play_background_music(self):
        try:
            pygame.mixer.music.load('Magical_Mystery(256k).mp3')
            pygame.mixer.music.play(-1)  # Loop indefinitely
            while not self.stop_music:
                time.sleep(0.1)  # Small sleep to prevent busy waiting
        except Exception as e:
            print(f"Error playing background music: {e}")

    def start_game(self):
        random.shuffle(self.words)
        selected_words = random.sample(self.words, 15)
        for word in selected_words:
            self.word_queue.enqueue(word)

        self.score = 0
        self.correct_words = []
        self.all_inputs = []
        self.attempt_stack = Stack()
        self.lives = 3
        self.lives_label.config(text=f"Lives: {self.get_lives_display()}")
        self.current_word_index = 1
        self.word_number_label.config(text=f"Word {self.current_word_index} of 15")  # Fixed to 15
        self.getnext_Word()

    def getnext_Word(self):
        if not self.word_queue.is_empty() and self.lives > 0:
            self.current_word = self.word_queue.dequeue()
            self.definition_label.config(text=f"Definition: {self.current_word['definition']}")
            self.entry.delete(0, tk.END)
            self.word_number_label.config(text=f"Word {self.current_word_index} of 15")
            self.current_word_index += 1
        else:
            self.end_game()

    def play_sound(self):
        if self.current_word:
            try:
                playsound(self.current_word['audio']) # Play the audio file, audio ra key
            except Exception as e: # try catch exception, para d mata maw mag exit ket wat sueod ro music
                self.definition_label.config(text=f"Error playing sound: {e}")

    def check_answer(self):
        if self.current_word and self.lives > 0:
            user_input = self.entry.get().strip().lower()  # Convert correct word to lowercase for comparison
            correct_word = self.current_word['word'].lower()

            self.all_inputs.append(user_input)

            is_correct = user_input == correct_word

            self.attempt_stack.push((self.current_word['word'], is_correct))

            if is_correct:
                try:
                    playsound('correct-156911.mp3')
                except:
                    pass
                self.correct_words.append({'word': self.current_word['word'], 'definition': self.current_word['definition']})
                self.score += 1  # Increment score for correct answer
                self.definition_label.config(text=f"Correct! ")
                self.root.after(2000, self.getnext_Word)
            else:
                try:
                    playsound('incorrect-293358.mp3')
                except:
                    pass
                self.lives -= 1 # Deduct life on wrong answer
                self.lives_label.config(text=f"Lives: {self.get_lives_display()}")
                if self.lives > 0:
                    self.definition_label.config(text=f"Incorrect.\n Try again! Lives left: {self.get_lives_display()}. ")
                else:
                    self.definition_label.config(text=f"Out of lives. \nThe correct word is: {self.current_word['word']}. ")
                    self.end_game()

    def skip_word(self):
        if self.current_word and self.lives > 0:
            self.lives -= 1 # Deduct life on skip
            self.lives_label.config(text=f"Lives: {self.get_lives_display()}")
            if self.lives > 0:
                self.getnext_Word()
            else:
                self.end_game()

    def end_game(self):
            self.stop_music = True
            pygame.mixer.music.stop()  # Stop the music
            if self.music_thread:
                self.music_thread.join()

            self.leaderboard.append((self.player_name, self.score))
            self.leaderboard = sorted(self.leaderboard, key=lambda x: x[1], reverse=True)[:3]  # Consistent with save, but load is 10 - consider unifying
            self.save_leaderboard()
        # Check if perfect score (all 15 words correct)
            if self.score == 15:
                self.show_congratulations()
            else:
                leaderboard_text = ("Game Over!"
                                "\nYour Score: {}\n"
                                "\nScience Wizards:\n").format(self.score)
            canvas = tk.Canvas(root, width=400, height=300)
            canvas.pack()
            canvas.create_text(200, 150, text=leaderboard_text, anchor="center", font=("Century", 14))

            try:
                playsound('game-over-arcade-6435.mp3')
            except:
                pass
            for i, (name, score) in enumerate(self.leaderboard, 1):
                leaderboard_text += f"{i}. {name}: {score}\n"
            self.definition_label.config(text=leaderboard_text)
            self.play_sound_button.destroy()
            self.entry.destroy()
            self.submit_button.destroy()
            self.lives_label.destroy()
            self.word_number_label.destroy()
            self.high_score_label.destroy()
            self.skip_button.config(text="Restart", command=self.replay_game)

            label_y = self.definition_label.winfo_y() + self.definition_label.winfo_height()
            button_y = label_y + 20  # 20 pixels below
            self.skip_button.place(x=root.winfo_width() // 2, y=button_y, anchor="center")


            if not self.attempt_stack.is_empty():
                last_attempt = self.attempt_stack.peek()
                print(f"Last attempt: Word '{last_attempt[0]}' was {'correct' if last_attempt[1] else 'incorrect'}")
                print(f"Final Score: {self.score} ")

    def show_congratulations(self):
        self.definition_label.config(text="Wow! You're truly a wizard! \n", font=("Papyrus", 10), fg="#FFD1DC", bg="#D90166")
        self.play_sound_button.destroy()
        self.entry.destroy()
        self.submit_button.destroy()
        self.lives_label.destroy()
        self.word_number_label.destroy()
        self.high_score_label.destroy()
        self.skip_button.config(text="Restart", command=self.replay_game)

    def replay_game(self):  # para mag uman
        # Go back to show_intro before replaying
        self.stop_music = False
        self.show_intro()
        self.skip_button.destroy()
        self.high_score_label.destroy()
        self.definition_label.destroy()
        self.title_label.destroy()


if __name__ == "__main__":
    root = tk.Tk()  # main window para kay tkinter
    game = ScienceWizard(root)  # instantiate kuno
    root.mainloop()  # starts the Tkinter event loop
