import streamlit as st
from src.state_manager import StateManager
from src.api_client import GeminiClient
from src.audio_generator import AudioGenerator
from src.ui_components import UIComponents

class App:
    def __init__(self):
        st.set_page_config(
            page_title="Aprenda idiomas com a Shirley",
            layout="centered",
            initial_sidebar_state="auto"
        )
        self.state_manager = StateManager()
        self.gemini_client = GeminiClient(st.secrets["GEMINI_API_KEY"])
        self.audio_generator = AudioGenerator()
        self.ui_components = UIComponents(self.state_manager, self.audio_generator)

    def send_message_action(self):
        current_message = self.state_manager.get_state("current_message")
        if current_message:
            user_message = {"role": "user", "text": current_message}
            self.state_manager.get_state('chat_history').append(user_message)
            
            self.state_manager.set_state('is_loading', True)
            
            # Clear the message by deleting the key and rerunning
            if 'current_message' in st.session_state:
                del st.session_state['current_message']

            ai_response_data = self.gemini_client.get_ai_content(user_message['text'], self.state_manager.get_state('selected_language'))
            self.state_manager.update_after_api_call(ai_response_data)
            
            # Rerun to refresh the UI
            st.rerun()

    def run(self):
        self.ui_components.display_header()
        self.ui_components.display_language_selector()
        self.ui_components.display_chat(self.send_message_action)

        if self.state_manager.get_state('vocabulary') or self.state_manager.get_state('sentences'):
            with st.container(border=True):
                st.subheader(f"Vocabulário e Frases: {self.state_manager.get_state('current_topic') if self.state_manager.get_state('current_topic') else 'Aguardando Tópico...'}")
                self.ui_components.display_vocabulary()
                self.ui_components.display_sentences(self.state_manager.check_answers)

if __name__ == "__main__":
    app = App()
    app.run()

