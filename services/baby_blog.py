import asyncpg
import datetime
async def create_blog_post(topic: str, crew):
    print(f"Creating blog post for {topic}")
    crew_result = crew.run(topic)
    # the result above is a markdown file
    # Extract the first header (the blog title) from the markdown file
    # Find the first # and get everything after it until the next line
    blog_title = crew_result.split("#")[1].split("\n")[0]
    print(f"Blog Title: {blog_title}")
    # Find the first image url within the markdown
    image_url = crew_result.split("![image]")[1].split("\n")[0].replace("(", "").replace(")", "")
    print(f"Image URL: {image_url}")

    conn = await asyncpg.connect('postgresql://postgres:postgres@db:5432/testdb')
    print("Connected")
    print(conn)
    await conn.execute('''
        INSERT INTO posts(title, image_url, content, created_at) VALUES($1, $2, $3, $4)
    ''', blog_title, image_url, crew_result, datetime.date.today())
    print("Inserted")

    # Close the connection.
    await conn.close()

    
    