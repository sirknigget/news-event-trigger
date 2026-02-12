from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from src.config import Config

def classify_event(title: str, description: str, config: Config) -> bool:
    llm = ChatOpenAI(model_name="gpt-4o-mini", openai_api_key=config.openai_api_key, temperature=0)
    
    prompt_template = """You are a news analyst. You will be given a news event title and description. 
    You need to determine if the following specific triggering event has happened: "{triggering_event}"
    
    GUIDELINES:
    - Respond 'True' ONLY if the event described in "{triggering_event}" has actually occurred as a confirmed fact in the news report.
    - Respond 'False' for:
        - Verbal threats, warnings, or predictions of the event.
        - "Tensions rising" or "fears of" the event without it actually happening.
        - Related but distinct events which are not the triggering event.
        - Rumors or unsubstantiated claims.
    
    Respond with only 'True' if the event has happened, and 'False' otherwise.
    
    News Title: {title}
    News Description: {description}
    """
    
    prompt = PromptTemplate(
        input_variables=["title", "description", "triggering_event"],
        template=prompt_template
    )
    
    chain = prompt | llm

    response = chain.invoke({
        "title": title,
        "description": description,
        "triggering_event": config.triggering_event
    })
    
    result = response.content.strip().lower()
    return result == "true"
