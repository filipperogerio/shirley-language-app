import streamlit as st

class StateManager:
    def __init__(self):
        self.initialize_state()

    def initialize_state(self):
        defaults = {
            'selected_language': 'Inglês',
            'chat_history': [],
            'vocabulary': [],
            'sentences': [],
            'user_answers': {},
            'feedback': {},
            'current_topic': '',
            'is_loading': False
        }
        for key, value in defaults.items():
            if key not in st.session_state:
                st.session_state[key] = value

    def get_state(self, key):
        return st.session_state.get(key)

    def set_state(self, key, value):
        st.session_state[key] = value

    def reset_all(self):
        self.set_state('chat_history', [])
        self.set_state('vocabulary', [])
        self.set_state('sentences', [])
        self.set_state('user_answers', {})
        self.set_state('feedback', {})
        self.set_state('current_topic', '')

    def update_after_api_call(self, ai_response_data):
        if ai_response_data:
            self.set_state('current_topic', ai_response_data.get('topic', ''))
            self.set_state('vocabulary', ai_response_data.get('vocabulary', []))
            self.set_state('sentences', ai_response_data.get('sentences', []))

            initial_user_answers = {i: '' for i in range(len(self.get_state('sentences')))}
            initial_feedback = {i: '' for i in range(len(self.get_state('sentences')))}
            self.set_state('user_answers', initial_user_answers)
            self.set_state('feedback', initial_feedback)

            ai_chat_response = f"Ótimo! Aqui está o vocabulário e as frases sobre \"{self.get_state('current_topic')}\" em {self.get_state('selected_language')}:"
            self.get_state('chat_history').append({"role": "ai", "text": ai_chat_response})
        else:
            self.get_state('chat_history').append({"role": "ai", "text": "Desculpe, não consegui gerar o conteúdo. Por favor, tente novamente com outro tópico."})
        
        self.set_state('is_loading', False)

    def check_answers(self):
        new_feedback = {}
        for i, sentence in enumerate(self.get_state('sentences')):
            user_answer = self.get_state('user_answers').get(i, '').strip().lower()
            correct_answer = sentence['blankWord'].strip().lower()
            if user_answer == correct_answer:
                new_feedback[i] = 'correct'
            else:
                new_feedback[i] = 'incorrect'
        self.set_state('feedback', new_feedback)
        st.rerun()