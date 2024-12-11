import tkinter as tk
from tkinter import scrolledtext
import threading
import os

# Importera funktionerna från backend
# (Om du sparade backend i en separat fil, importera här, t.ex., från alice_backend import ...)

def start_interaction():
    def interact():
        user_input = speech_to_text()
        if user_input:
            display_text(f"Du: {user_input}")
            response = generate_response(user_input)
            display_text(f"Alice: {response}")
            audio_file = text_to_speech(response)
            if audio_file:
                os.system(f"start {audio_file}")  # Windows, använd 'afplay' för Mac
            else:
                display_text("Alice kunde inte generera en röst.")
        else:
            display_text("Jag kunde inte höra dig. Försök igen!")

    # Kör interaktionen i en separat tråd för att undvika att GUI fryser
    threading.Thread(target=interact).start()

def display_text(text):
    output_text.config(state=tk.NORMAL)
    output_text.insert(tk.END, text + "\n")
    output_text.config(state=tk.DISABLED)
    output_text.see(tk.END)

# Skapa huvudfönstret
root = tk.Tk()
root.title("Alice - Din AI-assistent")

# Skapa en textvy för att visa konversationen
output_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, state=tk.DISABLED, height=15, width=50)
output_text.pack(padx=10, pady=10)

# Skapa en knapp för att starta interaktion
talk_button = tk.Button(root, text="Prata med Alice", command=start_interaction, font=("Arial", 14))
talk_button.pack(pady=10)

# Kör huvudloopen
root.mainloop()
