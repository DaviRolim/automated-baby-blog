from textwrap import dedent
from crewai import Agent

from langchain_openai import ChatOpenAI

from dotenv import load_dotenv
load_dotenv()


gpt4 = ChatOpenAI(model_name="gpt-4o", temperature=0.7)
gpt3 = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.7)


class BabyBlogAgents():
  def researcher(self, tools):
      return Agent(
          role='Parenting Market Research Analyst',
          goal='Gather the latest insights and trends on newborn care and essential products',
          backstory="""You are part of a leading parenting advice platform.
With a keen eye for detail and a motherly/fatherly instinct, you are always on top of the latest trends in newborn care.
Your mission is to sift through mountains of data and distill only the most relevant and practical information for new parents.""",
          verbose=True,
          allow_delegation=False,
          tools=tools,
          llm=gpt4
      )

  def writer(self, tools):
      return Agent(
          role='Content Creator for Parenting Resources',
          goal='Translate research findings into engaging and insightful content for new parents using markdown syntax',
          backstory=dedent("""You have a knack for understanding the challenges and joys of parenthood.
With a compassionate voice and a clear understanding of your audience,
you aim to write content that resonates, comforts, and guides new parents through their journey.
You understand the importance of adding visual elements to your content to communicate your message."""),
          verbose=True,
          allow_delegation=True,
          tools=tools,
          llm=gpt4
      )
  def translator(self):
    return Agent(
        role='The best blog translator',
        goal='Translate blog posts from one language to another without losing meaning and keeping the original tone',
        backstory="""You are a professional translator who can translate blog posts from one language to another without losing meaning and keeping the original tone.""",
        verbose=True,
        allow_delegation=False,
        llm=gpt3
    )
