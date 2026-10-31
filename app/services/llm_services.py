from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from app.core.config import settings
from dotenv import load_dotenv
load_dotenv()



llm = ChatGroq(model="openai/gpt-oss-20b", temperature=.1,
               groq_api_key=settings.GROQ_API_KEY)


prompt_template = ChatPromptTemplate.from_messages([
    (
        "system",
        "You are an expert prompt optimization engine. Your goal is to rewrite "
        "the user's prompt to be as concise, dense, and token-efficient as possible "
        "without losing any critical context, constraints, or instructions. "
        "Output ONLY the optimized prompt text without any conversational filler, explanations, or quotes."
    ),  
    ("user", "{text}")
])

compression_chain = prompt_template | llm | StrOutputParser()


def semantic_compression(text:str) -> str:
    """
    Uses Langchain and openai/gpt (via Groq) to perform advanced semantic compression.
    """
    if not text:
        return ""
    try:
        compressed = compression_chain.invoke({"text": text}).strip()
        return compressed if compressed else text


    except Exception as e:
        print(f"Langchain semantic compression warning: {e}")
        return text