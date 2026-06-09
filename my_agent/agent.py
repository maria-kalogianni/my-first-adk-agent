from google.adk.agents.llm_agent import Agent
from google.adk.tools import google_search

root_agent = Agent(
    model='gemini-2.5-flash',
    name='root_agent',
    description='A helpful assistant that can search the web.',
    instruction='Answer user questions to the best of your knowledge. When you need up-to-date information, use the google_search tool.',
    tools=[google_search],
)
