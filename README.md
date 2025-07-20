# Shirley - A sua Tutora de Idiomas com IA

Shirley é uma aplicação web interativa criada com Streamlit e alimentada pela API Gemini da Google. Ela ajuda os utilizadores a aprender novos idiomas através de conversas e exercícios de preenchimento de lacunas.

## Funcionalidades

*   **Chat Interativo:** Converse com uma IA para praticar as suas competências linguísticas.
*   **Geração de Vocabulário:** A IA gera uma lista de vocabulário com base no tópico da conversa.
*   **Exercícios de Preenchimento de Lacunas:** A IA cria frases para completar para testar a sua compreensão.
*   **Feedback Instantâneo:** Verifique as suas respostas e obtenha feedback imediato.
*   **Pronúncia de Áudio:** Ouça a pronúncia correta de cada palavra do vocabulário.

## Como Executar a Aplicação

1.  **Clone o repositório:**

    ```bash
    git clone https://github.com/seu-usuario/shirley.git
    cd shirley
    ```

2.  **Instale as dependências:**

    ```bash
    pip install -r requirements.txt
    ```

3.  **Configure a sua chave da API do Gemini:**

    *   Crie um ficheiro chamado `secrets.toml` na pasta `.streamlit`.
    *   Adicione a sua chave da API do Gemini ao ficheiro da seguinte forma:

        ```toml
        GEMINI_API_KEY = "SUA_CHAVE_API_AQUI"
        ```

4.  **Execute a aplicação:**

    ```bash
    streamlit run app.py
    ```

5.  Abra o seu navegador e aceda a `http://localhost:8501`.

## Tecnologias Utilizadas

*   **Streamlit:** Para a interface do utilizador da aplicação web.
*   **Google Gemini:** Para a geração de conteúdo de IA.
*   **gTTS:** Para a funcionalidade de text-to-speech.
*   **Python:** A linguagem de programação principal.