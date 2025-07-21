import streamlit as st

class UIComponents:
    def __init__(self, state_manager, audio_generator):
        self.state_manager = state_manager
        self.audio_generator = audio_generator

    def display_header(self):
        st.markdown(
            """
            <style>
            .header-title {
                font-size: 2.25rem; /* text-3xl */
                font-weight: 700; /* font-bold */
                color: #1e40af; /* text-blue-700 */
                text-align: center;
                margin-bottom: 1.5rem;
            }
            .stSelectbox > div > div {
                border-radius: 0.5rem; /* rounded-lg */
                border-width: 2px; /* border-2 */
                border-color: #93c5fd; /* border-blue-300 */
                background-color: #eff6ff; /* bg-blue-50 */
                color: #1e40af; /* text-blue-700 */
            }
            .stSelectbox > div > div:focus-within {
                outline: none;
                box-shadow: 0 0 0 2px #3b82f6; /* focus:ring-2 focus:ring-blue-500 */
                border-color: transparent; /* focus:border-transparent */
            }
            .chat-container {
                height: 200px; /* h-48 */
                overflow-y: auto;
                border: 1px solid #d1d5db; /* border border-gray-300 */
                border-radius: 0.5rem; /* rounded-lg */
                background-color: #ffffff; /* bg-white */
                padding: 0.5rem;
                margin-bottom: 1rem;
            }
            .user-message {
                text-align: right;
            }
            .ai-message {
                text-align: left;
            }
            .message-bubble {
                display: inline-block;
                padding: 0.5rem;
                border-radius: 0.5rem;
                margin-bottom: 0.25rem;
            }
            .user-bubble {
                background-color: #3b82f6; /* bg-blue-500 */
                color: white;
            }
            .ai-bubble {
                background-color: #e5e7eb; /* bg-gray-200 */
                color: #374151; /* text-gray-800 */
            }
            .chat-input-container {
                display: flex !important;
                gap: 0.5rem !important;
                align-items: flex-end !important;
                width: 100% !important;
                margin-bottom: 0 !important;
            }
            .chat-input-wrapper {
                flex: 1 !important;
                min-width: 0 !important;
            }
            .chat-input-wrapper > div {
                margin-bottom: 0 !important;
            }
            .chat-input-wrapper > div > div {
                margin-bottom: 0 !important;
            }
            .send-button-wrapper {
                flex-shrink: 0 !important;
                width: 60px !important;
                display: flex !important;
                align-items: flex-end !important;
            }
            .send-button-wrapper > div {
                margin-bottom: 0 !important;
                height: 48px !important;
                width: 100% !important;
            }
            .send-button-wrapper button {
                background-color: #3b82f6 !important;
                color: white !important;
                border: none !important;
                border-radius: 0.5rem !important;
                padding: 0.75rem !important;
                font-weight: 600 !important;
                cursor: pointer !important;
                display: flex !important;
                align-items: center !important;
                justify-content: center !important;
                width: 100% !important;
                height: 48px !important;
                font-size: 1.2rem !important;
                margin: 0 !important;
            }
            .send-button-wrapper button:hover {
                background-color: #2563eb !important;
            }
            .send-button-wrapper button:focus {
                outline: none !important;
                box-shadow: 0 0 0 2px #3b82f6, 0 0 0 4px #bfdbfe !important;
            }
            .send-button-wrapper button:disabled {
                background-color: #9ca3af !important;
                cursor: not-allowed !important;
            }
            /* Ensure text input has consistent height */
            .stTextInput > div > div > input {
                height: 48px !important;
                border-radius: 0.5rem !important;
                border-width: 2px !important;
                border-color: #93c5fd !important;
                padding: 0.75rem !important;
                box-sizing: border-box !important;
            }
            .vocabulary-item {
                background-color: #dbeafe; /* bg-blue-100 */
                padding: 0.5rem;
                border-radius: 0.375rem; /* rounded-md */
                display: flex;
                justify-content: space-between;
                align-items: center;
            }
            .vocabulary-word {
                font-weight: 600; /* font-semibold */
                color: #1e40af; /* text-blue-800 */
            }
            .vocabulary-translation {
                font-style: italic;
                color: #4b5563; /* text-gray-700 */
            }
            .sentence-card {
                background-color: #ffffff; /* bg-white */
                padding: 0.75rem;
                border-radius: 0.5rem; /* rounded-lg */
                box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05); /* shadow-sm */
                border: 1px solid #e5e7eb; /* border border-gray-200 */
                margin-bottom: 1rem;
            }
            .sentence-input {
                display: inline-block;
                width: 128px; /* w-32 */
                min-width: 80px; /* min-w-[80px] */
                padding: 0.5rem 0.75rem; /* px-2 py-1 */
                margin: 0 0.25rem; /* mx-1 */
                border-radius: 0.375rem; /* rounded-md */
                border-width: 2px; /* border-2 */
            }
            .sentence-input.correct {
                border-color: #22c55e; /* border-green-500 */
                background-color: #f0fdf4; /* bg-green-50 */
            }
            .sentence-input.incorrect {
                border-color: #ef4444; /* border-red-500 */
                background-color: #fef2f2; /* bg-red-50 */
            }
            .sentence-input:focus {
                outline: none;
                box-shadow: 0 0 0 1px #60a5fa; /* focus:ring-1 focus:ring-blue-400 */
            }
            .check-button {
                background-color: #16a34a; /* bg-green-600 */
                color: white;
                padding: 0.75rem; /* py-3 */
                width: 100%; /* w-full */
                border-radius: 0.5rem; /* rounded-lg */
                font-size: 1.125rem; /* text-lg */
                font-weight: 600; /* font-semibold */
                box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06); /* shadow-md */
            }
            .check-button:hover {
                background-color: #15803d; /* hover:bg-green-700 */
            }
            .check-button:focus {
                outline: none;
                box-shadow: 0 0 0 2px #22c55e, 0 0 0 4px #bbf7d0; /* focus:ring-2 focus:ring-green-500 focus:ring-offset-2 */
            }
            </style>
            """,
            unsafe_allow_html=True
        )
        st.markdown('<h1 class="header-title">Aprenda idiomas com a Shirley</h1>', unsafe_allow_html=True)

    def display_language_selector(self):
        st.selectbox(
            "Escolha seu Idioma",
            ('Inglês', 'Português', 'Espanhol', 'Francês', 'Alemão', 'Japonês'),
            key='selected_language',
            on_change=self.state_manager.reset_all
        )

    def display_chat(self, send_message_callback):
        with st.container(border=True):
            st.subheader("Converse com a Shirley")
            
            with st.container():
                st.markdown('<div class="chat-container">', unsafe_allow_html=True)
                for msg in self.state_manager.get_state('chat_history'):
                    if msg["role"] == "user":
                        st.markdown(f'<div class="user-message"><span class="message-bubble user-bubble">{msg["text"]}</span></div>', unsafe_allow_html=True)
                    else:
                        st.markdown(f'<div class="ai-message"><span class="message-bubble ai-bubble">{msg["text"]}</span></div>', unsafe_allow_html=True)
                
                if self.state_manager.get_state('is_loading'):
                    st.markdown('<div class="text-center text-gray-500"><span class="animate-pulse">A Shirley está pensando...</span></div>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)

            # Create a container for the input and button
            st.markdown('<div class="chat-input-container">', unsafe_allow_html=True)
            
            # Create columns for input and button
            col1, col2 = st.columns([5, 1])
            
            with col1:
                st.markdown('<div class="chat-input-wrapper">', unsafe_allow_html=True)
                st.text_input(
                    "Peça um tópico (ex: 'viagem', 'comida')",
                    key="current_message",
                    disabled=self.state_manager.get_state('is_loading'),
                    placeholder="Digite seu tópico aqui...",
                    label_visibility="collapsed"
                )
                st.markdown('</div>', unsafe_allow_html=True)
            
            with col2:
                st.markdown('<div class="send-button-wrapper">', unsafe_allow_html=True)
                if st.button("✈️", key="send_button", disabled=self.state_manager.get_state('is_loading'), help="Enviar mensagem", use_container_width=True):
                    if st.session_state.current_message:
                        send_message_callback()
                st.markdown('</div>', unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)

    def display_vocabulary(self):
        if self.state_manager.get_state('vocabulary'):
            st.write("**Vocabulário:**")
            vocab_cols = st.columns(2)
            for i, item in enumerate(self.state_manager.get_state('vocabulary')):
                with vocab_cols[i % 2]:
                    st.markdown(f"**{item['word']}**<br>{item['translation']}", unsafe_allow_html=True)
                    audio_base64 = self.audio_generator.text_to_speech_base64(item['word'], self.state_manager.get_state('selected_language'))
                    if audio_base64:
                        st.audio(audio_base64, format='audio/mp3')

    def display_sentences(self, check_answers_callback):
        if self.state_manager.get_state('sentences'):
            st.write("**Complete as Frases:**")
            for i, sentence in enumerate(self.state_manager.get_state('sentences')):
                with st.container(border=True):
                    full_sentence = sentence.get('fullSentence', '')
                    blank_word = sentence.get('blankWord', '')
                    
                    if not full_sentence or not blank_word or blank_word not in full_sentence:
                        st.warning(f"Frase {i+1} inválida.")
                        continue

                    parts = full_sentence.split(blank_word, 1)
                    
                    spec = [max(1, len(parts[0])), len(blank_word) + 5, max(1, len(parts[1]))]
                    col1, col2, col3 = st.columns(spec)

                    with col1:
                        st.write(parts[0])
                    
                    with col2:
                        answer_key = i
                        user_answer = st.text_input(
                            label=f"_{i}", 
                            value=self.state_manager.get_state('user_answers').get(answer_key, ''), 
                            key=f"answer_{i}",
                            label_visibility="collapsed"
                        )
                        self.state_manager.get_state('user_answers')[answer_key] = user_answer
                    
                    with col3:
                        if len(parts) > 1:
                            st.write(parts[1])

                    feedback = self.state_manager.get_state('feedback').get(answer_key)
                    if feedback == 'correct':
                        st.success("Correto!")
                    elif feedback == 'incorrect':
                        st.error(f"Incorreto, tente novamente.")

            st.button(
                "Verificar Respostas",
                on_click=check_answers_callback,
                use_container_width=True,
                key="check_answers_button",
                help="Clique para verificar se suas respostas estão corretas."
            )