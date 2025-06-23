# src/python/langchain_gemini.py
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from settings import settings

# A biblioteca irá procurar a variável de ambiente GOOGLE_API_KEY automaticamente
embed_model = GoogleGenerativeAIEmbeddings(
    model="models/embedding-001",
    task_type="RETRIEVAL_DOCUMENT"
)

# O mesmo para o modelo de chat
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    temperature=0,
    convert_system_message_to_human=True
)