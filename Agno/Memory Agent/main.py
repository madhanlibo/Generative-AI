from agno.agent import Agent
from agno.models.google import Gemini
from agno.embedder.google import GeminiEmbedder
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.knowledge.pdf_url import PDFUrlKnowledgeBase
from agno.vectordb.lancedb import LanceDb
from agno.vectordb.search import SearchType

import os
from dotenv import load_dotenv
load_dotenv()

agent = Agent(
    model = Gemini(id="gemini-2.5-flash-preview-05-20"),
    description = "You are a tech fianncial expert",
    instructions = [
        "Search your knowledge base for Amazon company investment and revenue.",
        "If the question is better suited for the web, search the web to fill in gaps.Just directly search web don't ask for permission",
        "Prefer the information in your knowledge base over the web results."
    ],
    knowledge = PDFUrlKnowledgeBase(
        urls = ["https://s2.q4cdn.com/299287126/files/doc_financials/2024/ar/Amazon-com-Inc-2023-Shareholder-Letter.pdf"],
        vector_db = LanceDb(
            table_name="recipes",
            uri="/tmp/lancedb",
            search_type=SearchType.keyword,
            embedder=GeminiEmbedder(),
        ),
        tools = [DuckDuckGoTools()],
        show_tool_calls = True,
        markdown = True
    )
)

if agent.knowledge is not None:
    agent.knowledge.load()

agent.print_response("What is revenue distribution of Amazon in 2023",stream=True)