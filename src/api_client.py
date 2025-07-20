import streamlit as st
import requests
import json

class GeminiClient:
    def __init__(self, api_key):
        self.api_key = api_key
        self.api_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={self.api_key}"

    def get_ai_content(self, topic, language):
        """
        Chama a API Gemini para gerar vocabulário e frases.
        """
        prompt = f"""Gere um vocabulário e 5 frases com lacunas sobre o tópico "{topic}" para o idioma "{language}". As frases devem ter UMA palavra do vocabulário como lacuna. Forneça a resposta em formato JSON com as seguintes chaves: "topic", "vocabulary" (array de objetos com "word" e "translation"), "sentences" (array de objetos com "fullSentence", "blankWord", "sentenceWithBlank" - onde "sentenceWithBlank" deve conter EXATAMENTE UM "____" no lugar da "blankWord")."""

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

        try:
            response = requests.post(self.api_url, headers={'Content-Type': 'application/json'}, json=payload)
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