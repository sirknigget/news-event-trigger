import os
import sys
import asyncio
from typing import List, Tuple
from dataclasses import dataclass
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.classifier import classify_event
from src.config import Config

NUM_CASES = 10

# Define Pydantic model for test case generation
class NewsTestCase(BaseModel):
    title: str = Field(description="The news event title")
  #  description: str = Field(description="The news event description")
    expected_classification: bool = Field(description="True if the event matches the trigger, False otherwise")

class TestCases(BaseModel):
    cases: List[NewsTestCase]

def generate_test_cases(triggering_event: str, num_cases: int) -> List[NewsTestCase]:
    llm = ChatOpenAI(model_name="gpt-4.1", temperature=0.7)
    
    parser = PydanticOutputParser(pydantic_object=TestCases)
    
    prompt = PromptTemplate(
        template="""You are an expert news analyst and test data generator.
        Generate {num_cases} diverse news event test cases (titles) related to the following triggering event:
        "{triggering_event}"
        
        Approximately half of the cases should be positive matches (True) where the event has actually happened.
        The other half should be negative matches (False), such as:
        - Related topics but not the specific event (e.g., rumors, threats, political statements without military action).
        - Completely unrelated events but with similar keywords.
        - Near misses.
        
        {format_instructions}
        """,
        input_variables=["num_cases", "triggering_event"],
        partial_variables={"format_instructions": parser.get_format_instructions()}
    )
    
    chain = prompt | llm | parser
    
    try:
        result = chain.invoke({"num_cases": num_cases, "triggering_event": triggering_event})
        return result.cases
    except Exception as e:
        print(f"Error generating test cases: {e}")
        return []

def run_evaluation():
    # Load config or create dummy
    # We need OPENAI_API_KEY
    if not os.getenv("OPENAI_API_KEY"):
        print("OPENAI_API_KEY not found. Please set it to run tests.")
        return

    triggering_event = "Military confrontation between Iran and US or Israel has occurred"
    
    dummy_config = Config(
        rss_feed_url="",
        keyword_filter="",
        triggering_event=triggering_event,
        lookback_minutes=0,
        pushover_user_keys=[],
        pushover_api_token="",
        openai_api_key=os.getenv("OPENAI_API_KEY")
    )

    print(f"Generating test cases using gpt-4o for event: '{triggering_event}'...")
    test_cases = generate_test_cases(triggering_event, num_cases=NUM_CASES)
    
    if not test_cases:
        print("No test cases generated.")
        return

    print(f"Generated {len(test_cases)} test cases. Running evaluation with gpt-4o-mini...")
    
    passed = 0
    failed = 0
    
    for i, case in enumerate(test_cases):
        print(f"\nCase {i+1}:")
        print(f"  Title: {case.title}")
        print(f"  Expected: {case.expected_classification}")
        
        prediction = classify_event(case.title, None, dummy_config)
        print(f"  Predicted: {prediction}")
        
        if prediction == case.expected_classification:
            print("  Result: PASS")
            passed += 1
        else:
            print("  Result: FAIL")
            failed += 1

    print(f"\nEvaluation Complete.")
    print(f"Passed: {passed}/{len(test_cases)}")
    print(f"Failed: {failed}/{len(test_cases)}")
    
    if failed > 0:
        print("Evaluation FAILED.")
        sys.exit(1)
    else:
        print("Evaluation PASSED.")
        sys.exit(0)

if __name__ == "__main__":
    run_evaluation()
