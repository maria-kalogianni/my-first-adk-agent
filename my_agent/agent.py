from google.adk.agents.llm_agent import Agent


MOCK_CAMPAIGNS = {
    "summer_sale": {"ctr": 6.2, "conversion_rate": 12.5, "spend": 5000},
    "brand_awareness": {"ctr": 1.3, "conversion_rate": 1.8, "spend": 8000},
    "product_launch": {"ctr": 3.8, "conversion_rate": 5.2, "spend": 12000},
    "retargeting": {"ctr": 4.5, "conversion_rate": 8.9, "spend": 3000},
}


def get_mock_campaign_data(campaign_name: str) -> dict:
    """Returns mock performance metrics for a given campaign."""
    #data = MOCK_CAMPAIGNS.get(campaign_name.lower().replace(" ", "_"))
    data = MOCK_CAMPAIGNS.get(campaign_name.lower().replace(" campaign", "").strip().replace(" ", "_"))
    if not data:
        available = ", ".join(MOCK_CAMPAIGNS.keys())
        return {"status": "error", "message": f"Campaign not found. Available: {available}"}
    return {"status": "success", "campaign_name": campaign_name, **data}


def evaluate_performance(ctr: float, conversion_rate: float, spend: float) -> dict:
    """Classifies campaign performance as High, Medium, or Low."""
    if ctr > 5.0:
        ctr_score = "High"
    elif ctr > 2.0:
        ctr_score = "Medium"
    else:
        ctr_score = "Low"

    if conversion_rate > 10.0:
        conv_score = "High"
    elif conversion_rate > 3.0:
        conv_score = "Medium"
    else:
        conv_score = "Low"

    scores = [ctr_score, conv_score]
    if scores.count("High") >= 2:
        overall = "High"
    elif scores.count("Low") >= 2:
        overall = "Low"
    else:
        overall = "Medium"

    return {
        "status": "success",
        "ctr_performance": ctr_score,
        "conversion_performance": conv_score,
        "overall": overall,
    }


campaign_agent = Agent(
    model='gemini-2.5-flash',
    name='campaign_agent',
    description='Evaluates advertising campaign performance and classifies it as High, Medium, or Low.',
    instruction=(
        'You are a campaign performance analyst. '
        'When asked about a campaign: first call get_mock_campaign_data to get the metrics, '
        'then call evaluate_performance with those metrics. '
        'Finally, summarize the results and give a recommendation.'
        
    ),
    tools=[get_mock_campaign_data, evaluate_performance],
)

root_agent = Agent(
    model='gemini-2.5-flash',
    name='root_agent',
    description='An orchestrator that routes questions to specialized sub-agents.',
    instruction=(
        'You are an orchestrator. '
        'For campaign performance questions, delegate to campaign_agent. '
        'For anything else, answer from your knowledge.'
        "Use the campaign name exactly as given without appending the word 'campaign'. Valid names are: summer_sale, brand_awareness, product_launch, retargeting."
    ),
    sub_agents=[campaign_agent],
)

