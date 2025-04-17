from dotenv import load_dotenv

from tools.tools import get_profile_url_tavily

load_dotenv()
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.tools import Tool
from langchain.agents import create_react_agent, AgentExecutor
from langchain import hub


def lookup(name):
    #ReAct Agent
    template = """
    You are a smart assistant tasked with finding LinkedIn profile URLs.

    Given the full name: "{name_of_person}", search the web and return **only one** valid and accessible LinkedIn profile URL for this person.

    - Do not loop more than 3 times.
    - Only look through the top 3 search results.
    - Return only a single valid LinkedIn profile URL as plain text — no explanation or markdown.
    - The result should look like: https://www.linkedin.com/in/xyz

    Nothing else should be in your answer.
    """
    prompt_templatee = PromptTemplate(input_variables=["name_of_person"], template=template)
    llm = ChatOpenAI(temperature=0, model='gpt-4o-mini')

    tools_for_agent=[
        Tool(
            name="Find LinkedIn Profile URL from Google",
            func=get_profile_url_tavily,
            description="Useful for when you need to get the Linkedin profile URL"
        )
    ]

    #pulling a pre-built ReAct prompt template from the LangChain Hub.
    react_prompt = hub.pull("hwchase17/react")

    agent=create_react_agent(llm=llm, tools=tools_for_agent,prompt=react_prompt)
    agent_executer= AgentExecutor(agent=agent, tools=tools_for_agent, verbose=True)

    result =  agent_executer.invoke(input={"input":prompt_templatee.format_prompt(name_of_person=name)})

    linkedin_profile_url = result['output']
    return linkedin_profile_url

# linked_url=lookup("dr. sebastian konrad")
# print(linked_url)
