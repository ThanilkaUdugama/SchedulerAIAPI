from .utils import getAllocatedTimes

from langchain.prompts import PromptTemplate

# task_gen_prompt_template = """
# You are a helpful assistant. Your task is to create a detailed schedule to achieve the task '{prompt}'.
# Follow these rules strictly:

# 1. The schedule must stay within the start date '{start_date}' and end date '{end_date}'.
# 2. Use the allocated times '{allocated_times}' (in 24-hour format) to define the task times.
# 3. Output must follow this JSON format:

# {{
#     "task": task title,
#     "icon": task icon code from the font awesome library,
#     "schedules": [
#         {{
#             "date": schedule date,
#             "startTime": start time,
#             "endTime": end time,
#             "content-generating-prompt": prompt to generate complete content relate to the session,
#             "heading": title related to the content,
#             "icon": related icon code from the iconify icon library
#         }},
#         ...
#     ]
# }}

# Instructions:
# - Generate a task title based on the task objective.
# - Choose a relevant iconify icon code for the task.
# - Split the task over available days and times, keeping the workload balanced.
# - Provide a meaningful content-generating prompt and heading for each session.
# - Ensure that the schedule remains within the given time frame.

# Example:
# {{
#     "task": "Learn Python Basics",
#     "icon": "fa-code",
#     "schedules": [
#         {{
#             "date": "2025-03-20",
#             "startTime": "10:00",
#             "endTime": "12:00",
#             "content-generating-prompt": "Explain Python variables and data types.",
#             "heading": "Python Basics - Variables and Data Types",
#             "icon": "fa-python"
#         }}
#     ]
# }}

# Generate a complete schedule now.
# """


# sections_gen_template = """
# You are an expert assistant with a strong background in instructional design and curriculum development. Your task is to generate a detailed and structured content plan for a specified topic. The plan should cover the topic comprehensively while adhering to the allocated time.

# ---

# ### 📝 **Task Overview**
# - **Topic:** {heading}
# - **Context:** {context}
# - **Allocated Time:** From {start_time} to {end_time}

# ---

# ### 🎯 **Step 1: Understand the Scope**
# You are tasked with generating a structured content plan for the topic **"{heading}"** within the context of **"{context}"**. The content should be structured logically, ensuring that all key concepts are covered while maintaining a smooth flow.

# ---

# ### ⏳ **Step 2: Time Allocation Guidelines**
# - The total available time is from **{start_time}** to **{end_time}**.
# - Break down the content into **logical sections**.
# - Ensure each section has a clear objective and goal.
# - Allocate time to each section based on the complexity and importance of the content.
# - The sum of all section times **MUST NOT exceed the total allocated time**.

# ---

# ### 🛠️ **Step 3: Formatting Instructions**
# - The output should be in **JSON format**.
# - Each section should have a:
#   - **Section title** – Descriptive and clear.
#   - **Allocated time** – In minutes.
#   - **Content description** – A short prompt to generate relavant content.
# - Ensure the JSON output is properly formatted.

# ---

# ### ✅ **Expected Output Format**
# ```json
# [
#     {{
#         "section": "<Title of the section>",
#         "allocatedTime": "<Allocated time in minutes>",
#         "description": "<A short prompt to generate relavant content>"
#     }},
#     {{
#         "section": "<Title of the section>",
#         "allocatedTime": "<Allocated time in minutes>",
#         "description": "<A short prompt to generate relavant content>"
#     }}
# ]"""



# content_generation_prompt_template = """
# You are a highly skilled educational content creator. Your task is to generate structured learning content that covers the topic **"{section}"** within the allocated time of **{allocated_time} minutes**.

# ---

# ### 🎯 **Task Overview**
# - **Topic:** {section}
# - **Allocated Time:** {allocated_time} minutes
# - **Audience:** Learners with varying levels of knowledge in the topic.

# ---

# ### ⏳ **Time Allocation Guidelines**
# - The content should be structured logically to fit within the allocated time.
# - Ensure that the content includes an introduction, main points, and a conclusion.
# - Make sure the content flow is smooth and engaging to maximize learning effectiveness.

# ---

# ### 🛠️ **Formatting Instructions**
# - The output should be in **JSON format**.
# - The content should be embedded within HTML tags, wrapped inside a `<div class="content"></div>`.
# - The JSON structure should follow this format strictly:

# ```json
# {
#     "title": "<Title of the topic>",
#     "html": "<Generated HTML content>",
#     "summary": "<Short summary of the content>"
# }"
# """


# content_search_prompt_template = """
# You are a highly skilled research assistant. Your task is to search the internet and YouTube for resources related to the topic **"{section}"**.

# ---

# ### 🎯 **Task Overview**
# - **Topic:** {section}
# - **Goal:** Provide a structured list of related articles and videos to help learners explore more about the topic.

# ---

# ### 🌐 **Step 1: Search for Articles**
# - Conduct a thorough search on reputable websites.
# - Identify 5 high-quality articles related to the topic.
# - Extract the article title and URL.

# ---

# ### 🎬 **Step 2: Search for Videos**
# - Conduct a YouTube search for the same topic.
# - Identify 5 relevant and high-quality videos.
# - Extract the video title, thumbnail URL, and video URL.

# ---

# ### 🛠️ **Formatting Instructions**
# - The output should be in **JSON format**.
# - Ensure that the output follows this exact structure:

# ```json
# {
#     "articles": [
#         {
#             "title": "Article Title",
#             "link": "URL of the article"
#         }
#     ],
#     "videos": [
#         {
#             "title": "Video Title",
#             "thumbnail": "URL of the thumbnail",
#             "link": "URL of the video"
#         }
#     ]
# }"
# """


# TASK_GEN_PROMPT_TEMPLATE = PromptTemplate(
#     input_variables=[
#         "prompt", 
#         "start_date", 
#         "end_date", 
#         "allocated_times"
#     ],
#     template=task_gen_prompt_template
# )


# SECTIONS_GEN_PROMPT_TEMPLATE = PromptTemplate(
#     input_variables=[
#         "heading", 
#         "start_date", 
#         "end_date", 
#         "context"
#     ],
#     template=sections_gen_template
# )


# CONTENT_GEN_PROMPT_TEMPLATE = PromptTemplate(
#     input_variables=["section", "allocated_time"],
#     template=content_generation_prompt_template)


# CONTENT_RESOURCE_PROMPT_TEMPLATE = PromptTemplate(
#     input_variables=["section"],
#     template=content_search_prompt_template)



def task_generation_prompt(taskjob):
    messages =  [
                    {"role": "assistant", "content": "Assign me a task, I will schedule it for you to achieve it."},
                    {"role": "user", "content":  taskjob.prompt + ".Please Schedule roadmap for achieving the task"},
                    {"role": "assistant", "content": "Give me the start date and end date"},
                    {"role": "user", "content":  f"Start date is {taskjob.start_date} and endDate is {taskjob.end_date}"},
                    {"role": "assistant", "content": "What are the allocated days and times for the task"},
                    {"role": "user", "content":  f"I allocated {getAllocatedTimes(taskjob.allocated_time)} (Times are in 24 hour format)"},
                    {"role" :  "assistant", "content": "what format you need the response"},
                    {"role" : "user", "content" : """ must be in JSON format. the structure is
{
    'task' : [Generate a task title considering the task trying to achieve],
    'icon' : [related icon code from the iconify icon library, make sure to give me a existing code and they must be white and different each other.],
    'schedules' : [
        schedules must stricktly stay within the start date and end date
        {
            'date' : [Schedule Date],
            'startTime' : [task start time considering given allocated times],
            'endTime' : [task end time considering given allocated times],
            'content-generating-prompt' :  [Prompt to generate complete content relate to the session],
            'heading' : [title related to the content],
            'icon' : [related icon code from the iconify icon library, make sure to give me a existing code and they must be white and different each other.],
        }
    ]
}
                     
                     #note : only give me the JSON. no other output

"""}
                ]
    
    return messages
    

def content_sections_generation_prompt(schedule):
    messages = [
        {"role": "assistant", "content": "Give me topic and I would generate a python list of topics in JSON format of content covering the topic"},
        {"role": "user", "content": f"The topic is {schedule.content}. In context of {schedule.task.title}"},
        {"role": "assistant", "content": "How much time do you allocate to cover the topic?"},
        {"role": "user", "content": f"Allocated time is from {schedule.startTime} to {schedule.endTime}."},
        {"role": "assistant", "content": "What is the format of the output?"},
        {"role": "user", "content": "[{'section': 'Section Title', 'allocatedTime': 'Allocated Time in Minutes'}] . Output JSON must be in this format strictly."}
    ]
    return messages


def section_content_generation_prompt(section):
    messages = [
        {"role" : "assistant", "content" : "Give me topic and allocated time I would generate content that covers the topic for learners in the allocated time"},
        {"role" : "user", "content" : f"The topic is {section['section']} and allocated time is {section['allocatedTime']} Minutes."},
        {"role" : "assistant", "content" : "In what format should I generate the content?"},
        {"role" : "user", "content" : "Generate content in JSON format. generate HTML within <div class='content'></div>. the HTML must under the 'html' key"},
    ]
    return messages

def external_resource_fetch_prompt(section):
    messages = [
        {"role" : "assistant", "content" :  "Give me topic and I would search in internet and find related articles"},
        {"role" : "user", "content" :  f"The topic is {section['section']} and give me 5 related articles to explore more."},
        {"role" : "assistant", "content" : "Is that it?"},
        {"role" : "user", "content" : "Also I need related Videos. Search Youtube for related videos and give me 5 videos"},
        {"role" : "assistant", "content" : "What is the format of the output"},
        {"role" : "user", "content" : "I need output in JSON format. the structure is \{'articles' : [List of articles in structure of \{'title' : Article Title, 'link': URL of the article\}]\, 'videos' : [List of related video data in format of \{'title' : Video Title, 'thumbnail' : Thumbnail URL, 'link' : URL of the video\}]}"}

    ]
    return messages

def task_validity_check_prompt(taskjob):
    messages = [
        {"role" : "assistant", "content" :  "Give me task and allocated time duration and I would validate whether the plan is realistic"},
        {"role" : "user", "content" : f"The task is {taskjob.prompt}. Start date is {taskjob.start_date} and endDate is {taskjob.end_date}. The allocated time is {getAllocatedTimes(taskjob.allocated_time)}"},
        {"role" : "assistant", "content" : "What's the output format"},
        {"role" : "user", "content" : "Give me output in JSON format. the structure is \{'valid' : true or false, 'note' : if the plan is not valid, mention the minimum allocate hours and suggest what to do. like extending end date to x date \}"}

    ]
    return messages





