import os
import json
import google.generativeai as ai
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label

# API key
API_KEY = 'AIzaSyB5dVbogTrL1KsRIQrN3TZV9KTldtOzaPE'
ai.configure(api_key=API_KEY)

# Initialize the generative AI model
model = ai.GenerativeModel("gemini-pro")

class ChatApp(App):
    def build(self):
        self.username = None
        self.password = None
        self.load_credentials()
        
        self.layout = BoxLayout(orientation='vertical')

        # Create chat history area within a ScrollView
        self.chat_history = TextInput(size_hint_y=8, readonly=True, background_color=(0.13, 0.13, 0.13, 1), foreground_color=(1, 1, 1, 1))
        scroll_view = ScrollView(size_hint=(1, 0.8), do_scroll_x=False, do_scroll_y=True)
        scroll_view.add_widget(self.chat_history)  # Add the TextInput to the ScrollView
        self.layout.add_widget(scroll_view)

        # Create user input area
        self.user_input = TextInput(size_hint_y=None, height='30dp', multiline=False)
        self.layout.add_widget(self.user_input)

        # Create send button
        self.send_button = Button(text="Send", size_hint_y=None, height='40dp')
        self.send_button.bind(on_press=self.send_message)
        self.layout.add_widget(self.send_button)

        return self.layout

    def send_message(self, instance):
        user_message = self.user_input.text.strip()
        if user_message:
            self.chat_history.text += f"You: {user_message}\n"
            self.user_input.text = ""

            try:
                response = model.start_chat().send_message(user_message)
                self.chat_history.text += f"Chatbot: {response.text}\n"
            except Exception as e:
                self.chat_history.text += f"Chatbot: Error occurred - {str(e)}\n"

            self.save_messages()

    def load_credentials(self):
        if os.path.exists("credentials.json"):
            with open("credentials.json", "r") as f:
                try:
                    credentials = json.load(f)
                    self.username = credentials.get("username")
                    self.password = credentials.get("password")
                except json.JSONDecodeError:
                    print("Error: The credentials file is empty or corrupted.")

    def save_messages(self):
        if self.username:
            filename = f"{self.username}_chat_history.json"
            messages = self.chat_history.text.splitlines()
            with open(filename, "w") as f:
                json.dump(messages, f)

if __name__ == '__main__':
    ChatApp().run()
