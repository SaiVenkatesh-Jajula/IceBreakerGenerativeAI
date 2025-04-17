import os

from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

from agents.linkedin_lookup_agent import lookup
from output_parsers import summary_parser
from third_parties.linkedin import scrape_linkedin_profile

load_dotenv()
api_key=os.getenv('OPENAI_API_KEY')

def ice_break(name):
    summary_template="""
        given Linked Profile information {information} about a Person, I want you to create:
        1. A short summary about him/her.
        2. Two Interesting facts about him/her.
        
        \n{format_instructions}
    """

    summary_prompt_template = PromptTemplate(input_variables=["information"], template=summary_template,
                                             partial_variables={"format_instructions":summary_parser.get_format_instructions()})

    llm = ChatOpenAI(temperature=0, model_name="gpt-4o-mini", openai_api_key=api_key)

    chain= summary_prompt_template | llm | summary_parser

    agent_output_url=lookup(name)

    linkedin_data = scrape_linkedin_profile(agent_output_url)
    if linkedin_data is None:
        return None,None

    res=chain.invoke(input={"information":linkedin_data})

    return res,linkedin_data.get("photoUrl")

# summary, image_url= ice_break("Srilekha Godavarthi")
#
# print(summary.summary)
# print(summary.facts[0])
# print(summary.facts[1])
# print(image_url)


