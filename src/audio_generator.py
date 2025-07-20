from gtts import gTTS
from io import BytesIO
import base64

class AudioGenerator:
    def __init__(self):
        self.lang_code_map = {
            'Inglês': 'en', 'Português': 'pt', 'Espanhol': 'es',
            'Francês': 'fr', 'Alemão': 'de', 'Japonês': 'ja'
        }

    def text_to_speech_base64(self, text, lang):
        """Gera áudio a partir de texto usando gTTS e o idioma da sessão."""
        lang_code = self.lang_code_map.get(lang, 'en')
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