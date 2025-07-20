import streamlit as st
import json
import requests
import os
from gtts import gTTS
from io import BytesIO
import base64

# --- Configurações da Página ---
st.set_page_config(
    page_title="Aprenda idiomas com a Shirley",
    layout="centered",
    initial_sidebar_state="auto"
)

# --- Variáveis de Estado da Sessão ---
# Inicializa o estado da sessão se ainda não estiver definido
if 'selected_language' not in st.session_state:
    st.session_state.selected_language = 'Inglês' # Idioma inicial
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'vocabulary' not in st.session_state:
    st.session_state.vocabulary = []
if 'sentences' not in st.session_state:
    st.session_state.sentences = []
if 'user_answers' not in st.session_state:
    st.session_state.user_answers = {}
if 'feedback' not in st.session_state:
    st.session_state.feedback = {}
if 'current_topic' not in st.session_state:
    st.session_state.current_topic = ''
if 'is_loading' not in st.session_state:
    st.session_state.is_loading = False

# --- Função para Chamar a API Gemini ---
def get_ai_content(topic, language):
    """
    Chama a API Gemini para gerar vocabulário e frases.
    """
    prompt = f"Gere um vocabulário e 5 frases com lacunas sobre o tópico \"{topic}\" para o idioma \"{language}\". As frases devem ter UMA palavra do vocabulário como lacuna. Forneça a resposta em formato JSON com as seguintes chaves: \"topic\", \"vocabulary\" (array de objetos com \"word\" e \"translation\"), \"sentences\" (array de objetos com \"fullSentence\", \"blankWord\", \"sentenceWithBlank\" - onde \"sentenceWithBlank\" deve conter EXATAMENTE UM \"____\" no lugar da \"blankWord\")."

    payload = {
        "contents": [{"role": "user", "parts": [{"text": prompt}]}],
        "generationConfig": {
            "responseMimeType": "application/json",
            "responseSchema": {
                "type": "OBJECT",
                "properties": {
                    "topic": {"type": "STRING"},
                    "vocabulary": {
                        "type": "ARRAY",
                        "items": {
                            "type": "OBJECT",
                            "properties": {
                                "word": {"type": "STRING"},
                                "translation": {"type": "STRING"},
                            },
                            "propertyOrdering": ["word", "translation"],
                        },
                    },
                    "sentences": {
                        "type": "ARRAY",
                        "items": {
                            "type": "OBJECT",
                            "properties": {
                                "fullSentence": {"type": "STRING"},
                                "blankWord": {"type": "STRING"},
                                "sentenceWithBlank": {"type": "STRING"},
                            },
                            "propertyOrdering": ["fullSentence", "blankWord", "sentenceWithBlank"],
                        },
                    },
                },
                "propertyOrdering": ["topic", "vocabulary", "sentences"],
            },
        },
    }

    # API_KEY will be provided by the Canvas environment at runtime
    api_key = st.secrets["GEMINI_API_KEY"]
    api_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={api_key}"

    try:
        response = requests.post(api_url, headers={'Content-Type': 'application/json'}, json=payload)
        response.raise_for_status() # Levanta um erro para códigos de status HTTP ruins (4xx ou 5xx)
        result = response.json()

        if result.get('candidates') and len(result['candidates']) > 0 and \
           result['candidates'][0].get('content') and result['candidates'][0]['content'].get('parts') and \
           len(result['candidates'][0]['content']['parts']) > 0:
            json_response_str = result['candidates'][0]['content']['parts'][0]['text']
            return json.loads(json_response_str)
        else:
            return None
    except requests.exceptions.RequestException as e:
        st.error(f"Erro ao chamar a API Gemini: {e}")
        return None
    except json.JSONDecodeError as e:
        st.error(f"Erro ao decodificar a resposta JSON da API: {e}")
        return None

# --- Função para Enviar Mensagem (Ação do Botão/Enter) ---
def send_message_action():
    if st.session_state.current_message:
        user_message = {"role": "user", "text": st.session_state.current_message}
        st.session_state.chat_history.append(user_message)
        
        st.session_state.is_loading = True
        st.session_state.current_message = "" # Limpa a caixa de texto imediatamente

        # Chamar a função de API e atualizar o estado
        ai_response_data = get_ai_content(user_message['text'], st.session_state.selected_language)
        
        if ai_response_data:
            st.session_state.current_topic = ai_response_data.get('topic', '')
            st.session_state.vocabulary = ai_response_data.get('vocabulary', [])
            st.session_state.sentences = ai_response_data.get('sentences', [])

            # Inicializa user_answers e feedback
            initial_user_answers = {i: '' for i in range(len(st.session_state.sentences))}
            initial_feedback = {i: '' for i in range(len(st.session_state.sentences))}
            st.session_state.user_answers = initial_user_answers
            st.session_state.feedback = initial_feedback

            ai_chat_response = f"Ótimo! Aqui está o vocabulário e as frases sobre \"{st.session_state.current_topic}\" em {st.session_state.selected_language}:"
            st.session_state.chat_history.append({"role": "ai", "text": ai_chat_response})
        else:
            st.session_state.chat_history.append({"role": "ai", "text": "Desculpe, não consegui gerar o conteúdo. Por favor, tente novamente com outro tópico."})
        
        st.session_state.is_loading = False

# --- Função para Verificar Respostas ---
def check_answers_action():
    new_feedback = {}
    for i, sentence in enumerate(st.session_state.sentences):
        user_answer = st.session_state.user_answers.get(i, '').strip().lower()
        correct_answer = sentence['blankWord'].strip().lower()
        if user_answer == correct_answer:
            new_feedback[i] = 'correct'
        else:
            new_feedback[i] = 'incorrect'
    st.session_state.feedback = new_feedback
    st.rerun()

# --- Função para Gerar Áudio ---
def text_to_speech_base64(text, lang):
    """Gera áudio a partir de texto usando gTTS e o idioma da sessão."""
    lang_code_map = {
        'Inglês': 'en', 'Português': 'pt', 'Espanhol': 'es',
        'Francês': 'fr', 'Alemão': 'de', 'Japonês': 'ja'
    }
    lang_code = lang_code_map.get(lang, 'en')
    try:
        tts = gTTS(text=text, lang=lang_code, slow=False)
        audio_fp = BytesIO()
        tts.write_to_fp(audio_fp)
        audio_fp.seek(0)
        audio_base64 = base64.b64encode(audio_fp.read()).decode('utf-8')
        return f"data:audio/mp3;base64,{audio_base64}"
    except Exception as e:
        print(f"Erro ao gerar áudio para '{text}': {e}")
        return None

# --- Layout da Aplicação Streamlit ---

# Título do Aplicativo
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
    .stTextInput > div > div > input {
        border-radius: 0.5rem 0 0 0.5rem; /* rounded-l-lg */
        border-width: 2px; /* border-2 */
        border-color: #93c5fd; /* border-blue-300 */
        padding: 0.75rem; /* p-3 */
    }
    .stButton > button {
        border-radius: 0 0.5rem 0.5rem 0; /* rounded-r-lg */
        background-color: #2563eb; /* bg-blue-600 */
        color: white;
        padding: 0.75rem; /* p-3 */
        font-weight: 600; /* font-semibold */
    }
    .stButton > button:hover {
        background-color: #1d4ed8; /* hover:bg-blue-700 */
    }
    .stButton > button:focus {
        outline: none;
        box-shadow: 0 0 0 2px #3b82f6, 0 0 0 4px #bfdbfe; /* focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 */
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

# Seleção de Idioma
st.selectbox(
    "Escolha seu Idioma",
    ('Inglês', 'Português', 'Espanhol', 'Francês', 'Alemão', 'Japonês'),
    key='selected_language',
    on_change=lambda: [
        setattr(st.session_state, 'chat_history', []),
        setattr(st.session_state, 'vocabulary', []),
        setattr(st.session_state, 'sentences', []),
        setattr(st.session_state, 'user_answers', {}),
        setattr(st.session_state, 'feedback', {}),
        setattr(st.session_state, 'current_topic', '')
    ]
)

# Layout de uma coluna
with st.container(border=True):
    st.subheader("Converse com a Shirley")
    
    # Área de exibição do chat
    with st.container():
        st.markdown('<div class="chat-container">', unsafe_allow_html=True)
        for msg in st.session_state.chat_history:
            if msg["role"] == "user":
                st.markdown(f'<div class="user-message"><span class="message-bubble user-bubble">{msg["text"]}</span></div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="ai-message"><span class="message-bubble ai-bubble">{msg["text"]}</span></div>', unsafe_allow_html=True)
        
        if st.session_state.is_loading:
            st.markdown('<div class="text-center text-gray-500"><span class="animate-pulse">A Shirley está pensando...</span></div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True) # Fecha chat-container

    # Campo de entrada de texto para o chat
    st.text_input(
        "Peça um tópico (ex: 'viagem', 'comida')",
        key="current_message",
        on_change=send_message_action,
        disabled=st.session_state.is_loading,
        placeholder="Digite seu tópico aqui..."
    )
    # Nota: Em Streamlit, o botão de envio é geralmente o Enter no text_input,
    # ou um st.button separado se a ação for mais complexa.
    # Para replicar o botão de envio visual, podemos estilizar o text_input ou adicionar um ícone.
    # Por simplicidade, o on_change do text_input já aciona o envio.

if st.session_state.vocabulary or st.session_state.sentences:
    with st.container(border=True):
        st.subheader(f"Vocabulário e Frases: {st.session_state.current_topic if st.session_state.current_topic else 'Aguardando Tópico...'}")

        # Seção de Vocabulário
        if st.session_state.vocabulary:
            st.write("**Vocabulário:**")
            # Apresentar vocabulário em grelha
            vocab_cols = st.columns(2)
            for i, item in enumerate(st.session_state.vocabulary):
                with vocab_cols[i % 2]:
                    st.markdown(f"**{item['word']}**<br>{item['translation']}", unsafe_allow_html=True)
                    audio_base64 = text_to_speech_base64(item['word'], st.session_state.selected_language)
                    if audio_base64:
                        st.audio(audio_base64, format='audio/mp3')

        # Seção de Exercícios (Frases com Lacunas)
        if st.session_state.sentences:
            st.write("**Complete as Frases:**")
            for i, sentence in enumerate(st.session_state.sentences):
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
                            value=st.session_state.user_answers.get(answer_key, ''), 
                            key=f"answer_{i}",
                            label_visibility="collapsed"
                        )
                        st.session_state.user_answers[answer_key] = user_answer
                    
                    with col3:
                        if len(parts) > 1:
                            st.write(parts[1])

                    feedback = st.session_state.feedback.get(answer_key)
                    if feedback == 'correct':
                        st.success("Correto!")
                    elif feedback == 'incorrect':
                        st.error(f"Incorreto, tente novamente.")


        st.button(
            "Verificar Respostas",
            on_click=check_answers_action,
            use_container_width=True,
            key="check_answers_button",
            help="Clique para verificar se suas respostas estão corretas."
        )

