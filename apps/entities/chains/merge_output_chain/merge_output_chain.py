from apps.entities.chat_models.chat_models import groq_chat
from .prompt import merge_output_prompt

merge_output_chain = merge_output_prompt | groq_chat
