import threading
from time import sleep
from django.db import models
from .models import TaskJob, Task, TaskSchedule
from .serializers import TaskScheduleSerializer
from concurrent.futures import ThreadPoolExecutor, as_completed
import json
import re
from datetime import datetime, timedelta
from .prompts_manager import handle_prompt
from .prompts import task_generation_prompt, content_sections_generation_prompt, section_content_generation_prompt, external_resource_fetch_prompt

def generate_task(taskjob):
    prompt = task_generation_prompt(taskjob)
    data = {
  "task": "Python Learning Roadmap",
  "icon": "mdi:snake",
  "schedules": [
    {
      "date": "2025-03-24",
      "startTime": "12:00",
      "endTime": "16:00",
      "content-generating-prompt": "Generate a detailed session covering Python basics including variables, data types, and input/output.",
      "heading": "Python Basics",
      "icon": "mdi:keyboard"
    },
    {
      "date": "2025-03-25",
      "startTime": "12:00",
      "endTime": "16:00",
      "content-generating-prompt": "Generate a session covering Python control structures including if-else, loops, and logical operators.",
      "heading": "Control Structures",
      "icon": "mdi:code-braces"
    },
    {
      "date": "2025-03-31",
      "startTime": "12:00",
      "endTime": "16:00",
      "content-generating-prompt": "Generate a session about Python functions including defining functions, parameters, and return values.",
      "heading": "Functions in Python",
      "icon": "mdi:lambda"
    },
    {
      "date": "2025-04-01",
      "startTime": "12:00",
      "endTime": "16:00",
      "content-generating-prompt": "Generate a session covering Python data structures including lists, tuples, sets, and dictionaries.",
      "heading": "Data Structures",
      "icon": "mdi:database"
    },
    {
      "date": "2025-04-07",
      "startTime": "12:00",
      "endTime": "16:00",
      "content-generating-prompt": "Generate a session about Python object-oriented programming including classes, objects, inheritance, and polymorphism.",
      "heading": "OOP in Python",
      "icon": "mdi:vector-class"
    },
    {
      "date": "2025-04-08",
      "startTime": "12:00",
      "endTime": "16:00",
      "content-generating-prompt": "Generate a session covering Python file handling including reading and writing files, and working with file paths.",
      "heading": "File Handling",
      "icon": "mdi:file-document"
    },
    {
      "date": "2025-04-14",
      "startTime": "12:00",
      "endTime": "16:00",
      "content-generating-prompt": "Generate a session about Python error handling including try-except blocks and raising exceptions.",
      "heading": "Error Handling",
      "icon": "mdi:alert-circle"
    },
    {
      "date": "2025-04-15",
      "startTime": "12:00",
      "endTime": "16:00",
      "content-generating-prompt": "Generate a session covering Python modules and libraries including importing modules and working with libraries like math and os.",
      "heading": "Modules and Libraries",
      "icon": "mdi:library"
    },
    {
      "date": "2025-04-21",
      "startTime": "12:00",
      "endTime": "16:00",
      "content-generating-prompt": "Generate a session about Python web development basics using Flask.",
      "heading": "Web Development with Flask",
      "icon": "mdi:web"
    },
    {
      "date": "2025-04-22",
      "startTime": "12:00",
      "endTime": "16:00",
      "content-generating-prompt": "Generate a session covering Python data analysis using Pandas and NumPy.",
      "heading": "Data Analysis with Pandas and NumPy",
      "icon": "mdi:chart-line"
    },
    {
      "date": "2025-04-28",
      "startTime": "12:00",
      "endTime": "16:00",
      "content-generating-prompt": "Generate a session about working with APIs using Python including GET and POST requests.",
      "heading": "Working with APIs",
      "icon": "mdi:api"
    },
    {
      "date": "2025-04-29",
      "startTime": "12:00",
      "endTime": "16:00",
      "content-generating-prompt": "Generate a session covering Python automation including automating file handling and web scraping.",
      "heading": "Automation with Python",
      "icon": "mdi:robot"
    },
    {
      "date": "2025-05-05",
      "startTime": "12:00",
      "endTime": "16:00",
      "content-generating-prompt": "Generate a session about testing in Python including unit testing and debugging.",
      "heading": "Testing in Python",
      "icon": "mdi:test-tube"
    },
    {
      "date": "2025-05-06",
      "startTime": "12:00",
      "endTime": "16:00",
      "content-generating-prompt": "Generate a session about building a small Python project to consolidate learning.",
      "heading": "Project: Build a Python Application",
      "icon": "mdi:application"
    },
    {
      "date": "2025-05-12",
      "startTime": "12:00",
      "endTime": "16:00",
      "content-generating-prompt": "Generate a session covering Python best practices and coding standards.",
      "heading": "Python Best Practices",
      "icon": "mdi:star"
    },
    {
      "date": "2025-05-13",
      "startTime": "12:00",
      "endTime": "16:00",
      "content-generating-prompt": "Generate a session about optimizing Python code for better performance.",
      "heading": "Performance Optimization",
      "icon": "mdi:speedometer"
    }
  ]
}
              

    task = data["task"]
    icon = data["icon"]
    schedules = data["schedules"]
    task = Task.objects.create(taskjob = taskjob, title = task, icon = icon)

    for schedule in schedules:
        TaskSchedule.objects.create(task = task, icon = schedule["icon"], heading = schedule["heading"], content = schedule["content-generating-prompt"], date=schedule["date"], startTime = schedule["startTime"], endTime = schedule["endTime"])


    taskjob.generated = True
    taskjob.save()  

def generate_schedule(schedule):
    generatedContent = []
    # sections = handle_prompt(content_sections_generation_prompt(schedule))
    sections = [
    {"section": "Introduction to Python", "allocatedTime": 30},
    {"section": "Variables in Python", "allocatedTime": 40},
    {"section": "Data Types in Python", "allocatedTime": 45},
    {"section": "Type Conversion", "allocatedTime": 30},
    {"section": "Working with Strings", "allocatedTime": 35},
    {"section": "User Input and Output", "allocatedTime": 40},
    {"section": "Formatted Strings", "allocatedTime": 30}
]


    for section in sections:
        # content = section_content_generation_prompt(section)
        # content = handle_prompt(section_content_generation_prompt(section))
       
        content = {
  "html": "<div class='content'>\n    <h2>Introduction to Python</h2>\n    <p>Python is a high-level, interpreted programming language known for its simple and readable syntax. It was created by Guido van Rossum and first released in 1991. Python is widely used for web development, data analysis, artificial intelligence, machine learning, automation, and more.</p>\n\n    <h3>Why Learn Python?</h3>\n    <ul>\n        <li>Easy to read and write</li>\n        <li>Extensive library support</li>\n        <li>Cross-platform compatibility</li>\n        <li>Strong community support</li>\n        <li>Versatile use cases (web development, data science, AI, etc.)</li>\n    </ul>\n\n    <h3>Getting Started</h3>\n    <p>You can start using Python by installing it from the official website: <a href='https://www.python.org/' target='_blank'>https://www.python.org/</a></p>\n\n    <h3>Basic Syntax</h3>\n    <pre><code># Example: Hello World\nprint(\"Hello, World!\")\n\n# Example: Variables\nname = \"John\"\nage = 25\nprint(f\"My name is {name} and I am {age} years old.\")\n    </code></pre>\n\n    <h3>Running Python Code</h3>\n    <p>You can run Python code using the command line:</p>\n    <pre><code>python filename.py</code></pre>\n\n    <h3>Conclusion</h3>\n    <p>Python's simplicity and versatility make it an ideal programming language for both beginners and experienced developers.</p>\n</div>"
}

        # resources = handle_prompt(external_resource_fetch_prompt(section))
        # if(resources["success"]): resources = resources["data"]
        resources = {
    "articles": [
        {
            "title": "Python Introduction - GeeksforGeeks",
            "link": "https://www.geeksforgeeks.org/introduction-to-python/"
        },
        {
            "title": "Python For Beginners",
            "link": "https://www.python.org/about/gettingstarted/"
        },
        {
            "title": "Introduction to Python for Absolute Beginners - GeeksforGeeks",
            "link": "https://www.geeksforgeeks.org/introduction-to-python-for-absolute-beginners/"
        },
        {
            "title": "Introduction To Python Basics - Simplilearn",
            "link": "https://www.simplilearn.com/learn-the-basics-of-python-article"
        },
        {
            "title": "Introduction to Python - W3Schools",
            "link": "https://www.w3schools.com/python/python_intro.asp"
        }
    ],
    "videos": [
        {
            "title": "Python Programming Tutorial for Beginners",
            "thumbnail": "https://i.ytimg.com/vi/rfscVS0vtbw/hqdefault.jpg",
            "link": "https://www.youtube.com/watch?v=rfscVS0vtbw"
        },
        {
            "title": "Learn Python - Full Course for Beginners",
            "thumbnail": "https://i.ytimg.com/vi/rfscVS0vtbw/hqdefault.jpg",
            "link": "https://www.youtube.com/watch?v=rfscVS0vtbw"
        },
        {
            "title": "Python Crash Course for Beginners",
            "thumbnail": "https://i.ytimg.com/vi/rfscVS0vtbw/hqdefault.jpg",
            "link": "https://www.youtube.com/watch?v=rfscVS0vtbw"
        },
        {
            "title": "Python Tutorial - Python for Beginners [Full Course]",
            "thumbnail": "https://i.ytimg.com/vi/rfscVS0vtbw/hqdefault.jpg",
            "link": "https://www.youtube.com/watch?v=rfscVS0vtbw"
        },
        {
            "title": "Python Full Course - Learn Python in 12 Hours",
            "thumbnail": "https://i.ytimg.com/vi/rfscVS0vtbw/hqdefault.jpg",
            "link": "https://www.youtube.com/watch?v=rfscVS0vtbw"
        }
    ]
}

        generatedContent.append({"section" : section["section"], "allocatedTime" : section["allocatedTime"], "html" : content['html'], "articles" : resources["articles"], "videos" : resources["videos"]})
        # print({"html" : content, "articles" : resources["articles"], "videos" : resources["videos"]})
    

    schedule.content = json.dumps(generatedContent)
    schedule.content_generated = True
    schedule.save()
    

def generate_schedules_process():
    executor = ThreadPoolExecutor(max_workers=5)
    while True:
        schedules_within_7_days = TaskSchedule.objects.filter(date__lte = datetime.now() + timedelta(days=7), content_generated = False)
        
        for schedule in schedules_within_7_days:
           executor.submit(generate_schedule, schedule)

        sleep(10)


def start_bg_threads():
    create_task_thread = threading.Thread(target=generate_schedules_process)
    create_task_thread.daemon = True
    create_task_thread.start()
    
   

   

    # create_schedules_thread = threading.Thread(target=create_schedules)
    # create_schedules_thread.daemon = True
    # create_schedules_thread.start()



import multiprocessing
from concurrent.futures import ThreadPoolExecutor

# Function to multiply by 2
def multiply_by_2(number):
    result = number * 2
    print(f"Multiplied {number} by 2: {result}")
    return result

# Function to multiply by 3
def multiply_by_3(number):
    result = number * 3
    print(f"Multiplied {number} by 3: {result}")
    return result


def process_multiply_by_2(numbers):
    with ThreadPoolExecutor() as executor:
        results = executor.map(multiply_by_2, numbers)
        return list(results)

def process_multiply_by_3(numbers):
    with ThreadPoolExecutor() as executor:
        results = executor.map(multiply_by_3, numbers)
        return list(results)

# def main():
#     numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

   
#     mid = len(numbers) // 2
#     numbers_process_1 = numbers[:mid]  
#     numbers_process_2 = numbers[mid:] 


#     process_1 = multiprocessing.Process(target=process_multiply_by_2, args=(numbers_process_1,))
#     process_2 = multiprocessing.Process(target=process_multiply_by_3, args=(numbers_process_2,))

  
#     process_1.start()
#     process_2.start()

#     # Wait for both processes to complete
#     process_1.join()
#     process_2.join()

# if __name__ == "__main__":
#     main()

    
start_bg_threads()

