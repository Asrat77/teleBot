import tkinter as tk
from tkinter import Scrollbar, Text, Entry, Button
from tkinter import simpledialog
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from data.training_data import training_data
from responses.greetings import greetings_responses
from chatterbot import languages

languages.ENG.ISO_639_1 = "en_core_web_sm"

tele_bot = ChatBot('TeleBot',
                   storage_adapter='chatterbot.storage.SQLStorageAdapter',
                   logic_adapters=[
                       {
                           'import_path': 'chatterbot.logic.BestMatch',
                           'default_response': "I'm sorry, I didn't understand that. Could you please rephrase?",
                           'maximum_similarity_threshold': 0.60  # Adjust the threshold as needed
                       }
                   ])

# Training the bot
trainer = ListTrainer(tele_bot)
trainer.train(training_data)

# Training with specific response categories
trainer.train(greetings_responses)

class ChatBotGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("ChatBot GUI")
        self.root.geometry("400x500")

        # Set default mode to Light Mode
        self.mode_var = tk.StringVar(value="Light")

        # Set background color for the main container
        self.root.configure(bg=self.get_bg_color())

        # Create mode buttons on the bottom of the sidebar
        light_button = tk.Radiobutton(root, text="Light Mode", variable=self.mode_var, value="Light", command=self.toggle_mode, font=("Arial", 10))
        light_button.grid(row=2, column=0, padx=10, pady=5, sticky='w')
        dark_button = tk.Radiobutton(root, text="Dark Mode", variable=self.mode_var, value="Dark", command=self.toggle_mode, font=("Arial", 10))
        dark_button.grid(row=3, column=0, padx=10, pady=5, sticky='w')

        # Create a Text widget to display the chat
        self.chat_display = Text(root, height=15, width=40, wrap='word', state='disabled', bg=self.get_bg_color(), font=("Arial", 12))
        self.chat_display.grid(row=0, column=1, rowspan=2, padx=10, pady=10, sticky="nsew")

        # Create a Scrollbar for the Text widget
        scrollbar = Scrollbar(self.root, command=self.chat_display.yview)
        scrollbar.grid(row=0, column=2, rowspan=2, sticky='ns')
        self.chat_display.config(yscrollcommand=scrollbar.set)

        # Create an Entry widget for user input
        self.user_input = Entry(root, width=30, font=("Arial", 12))
        self.user_input.grid(row=2, column=1, padx=10, pady=10, sticky="ew")

        # Create a Button to send messages
        send_button = Button(root, text="Send", command=self.send_message, bg="#607D8B", fg="white", font=("Arial", 12, "bold"))
        send_button.grid(row=2, column=2, padx=10, pady=10, sticky="ew")

        # Configure row and column weights for expansion
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_columnconfigure(1, weight=1)

    def send_message(self):
        user_message = self.user_input.get().strip()

        if not user_message:
            return

        self.display_message("You: " + user_message, 'user')

        bot_response = tele_bot.get_response(user_message)

        if bot_response.confidence < 0.6:
            self.learn_from_user(user_message)
        else:
            self.display_message("TeleBot: " + str(bot_response), 'bot')

        self.user_input.delete(0, 'end')

    def learn_from_user(self, user_message):
        # Ask the user for the correct response
        correct_response = simpledialog.askstring("Learn from User",
                                                  f"I don't know the answer. Can you provide the correct response for '{user_message}'?")

        if correct_response:
            buffer = [user_message, correct_response]
            trainer.train(buffer)

            # Display a confirmation message
            self.display_message("Thank you for teaching me!", 'bot')
        else:
            self.display_message("I couldn't learn from you this time. Please provide a valid response.", 'bot')

    def display_message(self, message, sender):
        self.chat_display.config(state='normal')
        self.chat_display.insert('end', message + '\n', sender)
        self.chat_display.config(state='disabled')
        # Autoscroll to the bottom
        self.chat_display.yview(tk.END)

    def toggle_mode(self):
        # Update the background color for the main container and chat display based on the selected mode
        self.root.configure(bg=self.get_bg_color())
        self.chat_display.config(bg=self.get_bg_color())

    def get_bg_color(self):
        # Return the background color based on the selected mode
        return '#607D8B' if self.mode_var.get() == 'Dark' else '#CFD8DC'

if __name__ == "__main__":
    root = tk.Tk()
    app = ChatBotGUI(root)
    root.mainloop()
