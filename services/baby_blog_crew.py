import os
from crewai import Crew

from blog_crew.tasks import BabyBlogTasks
from blog_crew.agents import BabyBlogAgents
from blog_crew.tools import BabyBlogTools

print(f"SERPER_API_KEY: {os.environ['SERPER_API_KEY']}")



class BabyBlogCrew():
    def __init__(self):
        self.agents = BabyBlogAgents()
        self.tasks = BabyBlogTasks()
        self.tools = BabyBlogTools()

    def run(self, topic):
        print("Creating Agents")
        # Create agents
        researcher = self.agents.researcher([self.tools.search_tool])
        writer = self.agents.writer([self.tools.dalle_tool])
        translator = self.agents.translator()

        print("Creating Tasks")
        # Create tasks
        research = self.tasks.research(researcher, topic)
        write = self.tasks.write_markdown(
            writer, [self.tools.dalle_tool], topic, [research])
        # translate = self.tasks.translate(translator, [write])

        print("Creating Crew")
        crew = Crew(
            agents=[researcher, writer, translator],
            tasks=[research, write],#, translate],
            verbose=2
        )
        print("######################")
        print("Kickoff BabyBlogCrew")
        result = crew.kickoff()
        print("Crew Result")
        print("######################")
        print(result)
        print(crew.usage_metrics)
        return result

# Get your crew to work!
