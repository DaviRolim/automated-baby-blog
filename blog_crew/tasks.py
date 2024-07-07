from crewai import Task
from textwrap import dedent


class BabyBlogTasks():
  def research(self, agent, topic):
    return Task(
    description=dedent(f"""
        Research the most relevant and up-to-date information, expert advice, and products related to: '{topic}'.
        Highlight useful insights, and include a mix of high-quality, cost-effective, and eco-friendly options where applicable.
        The information gathered should be comprehensive and credible, effectively covering the essentials of the topic.
        """),
    expected_output="Comprehensive list of findings with sources",
    agent=agent
  )

  def write_markdown(self, agent, tools, topic, context):
    return Task(
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
                           and an Image for each section when applicable, for example. You MUST add at least one image, below the title of the blog.
                           The other images are option but if it makes sense you can add them too.
                           # BLOG TITLE HEADER
                           Image
                           
                           ## SECTION 1
                           <Content>
                           
                           ## SECTION 2
                           <Content>
                           
                           <MORE SECTIONS...>"""),
    agent=agent,
    tools=tools,
    context=context
  )

  def translate(self, agent, context):
    return Task(
        description="Translate the blog post to Brazilian Portuguese, without changing the markdown syntax, keeping the same heading structure, and images",
        expected_output="Translated blog post in Brazilian Portuguese, preserving markdown syntax",
        agent=agent,
        context=context
    )
        