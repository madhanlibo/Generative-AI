from agno.agent import Agent  # Import the main Agent class from agno framework
from agno.models.google import Gemini  # Import Google's Gemini model for AI capabilities
from agno.playground import Playground, serve_playground_app  # Import Playground for web interface and serve function for running the app
from agno.storage.sqlite import SqliteStorage  # Import SQLite storage for persisting agent conversations
from agno.tools.duckduckgo import DuckDuckGoTools  # Import DuckDuckGo search tools for web searching capabilities
from agno.tools.yfinance import YFinanceTools  # Import Yahoo Finance tools for financial data retrieval

import os  # Import os module for environment variable access
from dotenv import load_dotenv  # Import dotenv for loading environment variables from .env file
load_dotenv()  # Load environment variables from .env file into the current environment

agent_storage:str = "tmp/agents.db"  # Define the database file path for storing agent conversations

web_agent = Agent(  # Create a web search agent with DuckDuckGo capabilities
    name="Web Agent",  # Set the agent's display name
    model = Gemini(id="gemini-2.5-flash-preview-05-20"),  # Use Google's Gemini 2.5 Flash model
    tools=[DuckDuckGoTools()],  # Provide DuckDuckGo search functionality
    instructions=["Always include sources"],  # Give the agent specific instructions
    storage=SqliteStorage(table_name="web_agent", db_file=agent_storage),  # Store conversations in SQLite
    add_datetime_to_instructions=True,  # Include current date/time in agent instructions
    add_history_to_messages=True,  # Include conversation history in messages
    num_history_responses=5,  # Limit history to last 5 responses
    markdown=True,  # Enable markdown formatting in responses
)

finance_agent = Agent(  # Create a finance-focused agent with Yahoo Finance capabilities
    name="Finance Agent",  # Set the agent's display name
    model = Gemini(id="gemini-2.5-flash-preview-05-20"),  # Use Google's Gemini 2.5 Flash model
    tools=[YFinanceTools(stock_price=True, analyst_recommendations=True, company_info=True, company_news=True)],  # Enable all Yahoo Finance features
    instructions=["Always use tables to display data"],  # Instruct agent to format data in tables
    storage=SqliteStorage(table_name="finance_agent", db_file=agent_storage),  # Store conversations in SQLite with separate table
    add_datetime_to_instructions=True,  # Include current date/time in agent instructions
    add_history_to_messages=True,  # Include conversation history in messages
    num_history_responses=5,  # Limit history to last 5 responses
    markdown=True,  # Enable markdown formatting in responses
)

app = Playground(agents=[web_agent, finance_agent]).get_app()  # Create a Playground app with both agents and get the ASGI application

if __name__ == "__main__":  # Run the application only if this script is executed directly (not imported)
    serve_playground_app("main:app", reload=True)  # Start the web server with auto-reload enabled


# Copy and paste the localhost URL provided by the server into your agro website to interact with the Playground.