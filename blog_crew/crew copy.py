from langchain_openai import ChatOpenAI
import os
from textwrap import dedent
from crewai import Agent, Task, Crew, Process
from crewai_tools import SerperDevTool
from langchain.agents import Tool
from langchain_community.utilities.dalle_image_generator import DallEAPIWrapper
from dotenv import load_dotenv
load_dotenv()

# os.environ["OPENAI_API_KEY"] = "YOUR_API_KEY"
# os.environ["SERPER_API_KEY"] = "Your Key" # serper.dev API key
print(os.environ["SERPER_API_KEY"])
gpt4 = ChatOpenAI(model_name="gpt-4o", temperature=0.7)
gpt3 = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.7)
dalle = DallEAPIWrapper(n=1, size="512x512")

search_tool = SerperDevTool()
dalle_tool = Tool(
    name="DALL-E API",
    func=dalle.run,
    description="useful for generating images. The input to this should be a detailed prompt to generate an image in English.",
)

# Define your agents with roles and goals
researcher = Agent(
    role='Parenting Market Research Analyst',
    goal='Gather the latest insights and trends on newborn care and essential products',
    backstory="""You are part of a leading parenting advice platform.
  With a keen eye for detail and a motherly/fatherly instinct, you are always on top of the latest trends in newborn care.
  Your mission is to sift through mountains of data and distill only the most relevant and practical information for new parents.""",
    verbose=True,
    allow_delegation=False,
    tools=[search_tool],
    llm=gpt3
)
writer = Agent(
    role='Content Creator for Parenting Resources',
    goal='Translate research findings into engaging and insightful content for new parents using markdown syntax',
    backstory=dedent("""You have a knack for understanding the challenges and joys of parenthood.
  With a compassionate voice and a clear understanding of your audience, 
  you aim to write content that resonates, comforts, and guides new parents through their journey.
  You understand the importance of adding visual elements to your content to communicate your message."""),
    verbose=True,
    allow_delegation=True,
    tools=[dalle_tool],
    llm=gpt4
)


translator = Agent(
    role='The best blog translator',
    goal='Translate blog posts from one language to another without losing meaning and keeping the original tone',
    backstory="""You are a professional translator who can translate blog posts from one language to another without losing meaning and keeping the original tone.""",
    verbose=True,
    llm=gpt3
)

# User input for the topic/category
topic = input(dedent("""
    Please enter the topic or category you want to focus on:
    Examples:
    - Useful tips for the newborn's first month
    - How to save money when shopping for your baby
    - Best eco-friendly baby products
    - Preparing your pet for the new baby
    """))

# Create tasks for your agents
task1 = Task(
    description=dedent(f"""
        Research the most relevant and up-to-date information, expert advice, and products related to: '{topic}'.
        Highlight useful insights, and include a mix of high-quality, cost-effective, and eco-friendly options where applicable.
        The information gathered should be comprehensive and credible, effectively covering the essentials of the topic.
        """),
    expected_output="Comprehensive list of findings with sources",
    agent=researcher
)

task2 = Task(
    description=dedent(f"""
        Write an engaging and informative blog post focused on: '{topic}'.
        The content should be structured to offer value, either through advice, product recommendations, or practical tips.
        Ensure the tone is welcoming and supportive, aiming to connect with and assist your readers in their parenting journey.
        Use clear sections or headings to make the post easy to navigate.
        Use images to illustrate the content and add relevant context, if applicable, add one image per section. 
        Always add an Image below the title of the blog that have a visual representation of what the blog is about.
        For that you can use the DALL-E Tool, 
        that returns the URL of the image and you can add the image on your markdown output like this: ![image](image_url)
        """),
    expected_output=dedent(f"""Full blog post using markdown, 4-6 paragraphs with clear headings
                           and an Image for each section when applicable, for example. At least one image below the title of the blog.
                           The other images are option but if it makes sense you can add them too.
                           ## BLOG TITLE HEADER
                           Image
                           
                           ## SECTION 1
                           Image
                           <Content>
                           
                           ## SECTION 2
                           Image
                           <Content>
                           
                           <MORE SECTIONS...>"""),
    agent=writer,
    tools=[dalle_tool],
)

task3 = Task(
    description="Translate the blog post to Brazilian Portuguese",
    expected_output="Translated blog post in Brazilian Portuguese",
    agent=translator,
)

# Instantiate your crew with a sequential process
crew = Crew(
    agents=[researcher, writer, translator],
    tasks=[task1, task2, task3],
    verbose=2,  # You can set it to 1 or 2 to different logging levels
)

# Get your crew to work!
result = crew.kickoff()
print("######################")
print(result)
print(crew.usage_metrics)