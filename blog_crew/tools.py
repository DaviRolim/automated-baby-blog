from crewai_tools import SerperDevTool
from dotenv import load_dotenv
from langchain.agents import Tool
from langchain_community.utilities.dalle_image_generator import DallEAPIWrapper
load_dotenv()

class BabyBlogTools():
  def __init__(self):
    self.search_tool = SerperDevTool()
    dalle = DallEAPIWrapper(n=1, size="512x512")
    self.dalle_tool = Tool(
    name="DALL-E API",
    func=dalle.run,
    description="useful for generating images. The input to this should be a detailed prompt to generate an image in English.",
)
  def search_tool(self):
    return self.search_tool

  def dalle_tool(self):
    return self.dalle_tool