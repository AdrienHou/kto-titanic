import os
import asyncio
from typing import Any

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from pydantic import SecretStr
# TODO : Importer le client MCP depuis la librairie facilitant les échanges MCP
from langchain_mcp_adapters.client import MultiServerMCPClient

# TODO : Définir le système Prompt
SYSTEM_PROMPT = """You are a helpful assistant that predicts Titanic passenger survival.

To make a prediction, use the predict_survival tool with ALL required parameters:
- pclass (integer): Passenger class - 1 (First), 2 (Second), or 3 (Third)
- sex (string): "male" or "female"
- sibsp (integer): Number of siblings/spouses aboard (0-8)
- parch (integer): Number of parents/children aboard (0-9)

If the user doesn't specify all parameters, ask politely for missing information.
NEVER guess values - always ask the user.

Examples:
- "A man" → Ask: "What class? Any family aboard?"
- "A man in third class alone" → Use: pclass=3, sex="male", sibsp=0, parch=0

Be friendly and explain predictions clearly."""

class ChatbotAgent:
    def __init__(self) -> None:
        mcp_server_host: str = os.getenv(
            "MCP_SERVER_HOST", "http://titanic-mcp-server.adrienhssy-dev.svc.cluster.local:8000"
        )
        # TODO : Mettre en place dans un attribut de classe la configuration du client MCP en déclarant les servers mcp cibles
        self.mcp_server_host = mcp_server_host
        self.mcp_connections = {"titanic": {"url": f"{mcp_server_host}/mcp", "transport": "streamable_http"}}

        # TODO : Mettre en place dans un attribut de classe l'abstraction du LLM de Langchain en tant que ChatOpenAI
        # TODO : Faites en sorte que le mot de passe de l'API soit sécurisé avec pydantic SecretStr
        api_key = os.getenv("OPENAI_API_KEY", "dummy-key")
        self.llm = ChatOpenAI(
            model=os.getenv("LLM_MODEL", "gpt-4o-mini"),
            api_key=SecretStr(api_key),
            base_url=os.getenv("OPENAI_BASE_URL", "https://models.github.ai/inference"),
            temperature=0.7,
        )

    async def chat_async(self, message: str) -> str:
        """Chat async utilisant l'adaptateur MCP Langchain officiel."""
        # TODO : Créer le client MCP avec la configuration définie dans le constructeur
        mcp_client = MultiServerMCPClient(self.mcp_connections)

        # TODO : Récupérer les outils disponibles depuis le client MCP
        tools = await mcp_client.get_tools()

        # TODO : Lier les outils au LLM pour obtenir un LLM capable d'utiliser les outils
        llm_with_tools = self.llm.bind_tools(tools)

        # TODO : Construire les messages avec le system prompt et le message utilisateur
        messages = [SystemMessage(content=SYSTEM_PROMPT), HumanMessage(content=message)]

        # TODO : Invoquer le LLM avec les messages construits
        response = await llm_with_tools.ainvoke(messages)

        # TODO : Vérifier si une tool a été appelée dans la réponse
        if response.tool_calls:
            tool_call = response.tool_calls[0]
            tool_name = tool_call["name"]
            tool_args = tool_call["args"]

            for tool in tools:
                if tool.name == tool_name:
                    result = await tool.ainvoke(tool_args)
                    if hasattr(result, "content") and result.content:
                        content = result.content[0]
                        if hasattr(content, "text"):
                            return content.text
                        return str(content)
                    return str(result)
        # TODO : Retourner le résultat du tool si c'est la réponse du llm, sinon, sa réponse générée.
        return str(response.content)

    def chat(self, message: str) -> str:
        return asyncio.run(self.chat_async(message))
