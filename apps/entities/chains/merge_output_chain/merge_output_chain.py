from apps.entities.chat_models.chat_models import groq_chat
from .prompt import merge_output_prompt
from langchain_core.runnables import RunnableLambda

merge_output_chain = merge_output_prompt | groq_chat
