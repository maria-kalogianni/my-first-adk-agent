from datetime import datetime
from zoneinfo import ZoneInfo
from google.adk.agents.llm_agent import Agent
from google.adk.tools import google_search

CITY_TIMEZONES = {
    "athens": "Europe/Athens",
    "london": "Europe/London",
    "new york": "America/New_York",
    "tokyo": "Asia/Tokyo",
    "paris": "Europe/Paris",
    "berlin": "Europe/Berlin",
    "dubai": "Asia/Dubai",
    "sydney": "Australia/Sydney",
    "amsterdam": "Europe/Amsterdam",
}


def get_current_time(city: str) -> dict:
    """Returns the current time for a given city using its local timezone."""
    timezone_str = CITY_TIMEZONES.get(city.lower())
    if not timezone_str:
        available = ", ".join(CITY_TIMEZONES.keys())
        return {"status": "error", "message": f"City not found. Available: {available}"}

    now = datetime.now(ZoneInfo(timezone_str))
    return {
        "status": "success",
        "city": city,
        "timezone": timezone_str,
        "time": now.strftime("%H:%M:%S"),
        "date": now.strftime("%Y-%m-%d"),
    }


root_agent = Agent(
    model='gemini-2.5-flash',
    name='root_agent',
    description='A helpful assistant that can search the web and tell the time.',
    instruction=(
        'You are a helpful assistant. '
        'For current time or date questions, always use the get_current_time tool.'
    ),
    tools=[get_current_time],
)




# from google.adk.agents.llm_agent import Agent
# from google.adk.tools import google_search

# root_agent = Agent(
#     model='gemini-2.5-flash',
#     name='root_agent',
#     description='A helpful assistant that can search the web.',
#     #instruction='Answer user questions to the best of your knowledge. When you need up-to-date information, use the google_search tool.',
#     instruction='Always use the google_search tool for any question about current date, time, weather, news, or any real-time information. Never answer these from memory.',
#     tools=[google_search],
# )


# from datetime import datetime
# from google.adk.agents.llm_agent import Agent
# from google.adk.tools import google_search


# def get_current_time(city: str) -> dict:
#     """Returns the current time from the machine's clock."""
#     now = datetime.now()
#     return {
#         "status": "success",
#         "city": city,
#         "time": now.strftime("%H:%M:%S"),
#         "date": now.strftime("%Y-%m-%d"),
#     }


# root_agent = Agent(
#     model='gemini-2.5-flash',
#     name='root_agent',
#     description='A helpful assistant that can search the web and tell the time.',
#     instruction=(
#         'You are a helpful assistant. '
#         'For current time or date questions, always use the get_current_time tool. '
#         'For news, weather, or other real-time information, use google_search.'
#     ),
#     tools=[get_current_time, google_search],
# )
