from apps.entities.chat_models.chat_models import groq_chat
from apps.entities.chains.general_chat_chain.prompt import general_prompt

general_chain = general_prompt | groq_chat
