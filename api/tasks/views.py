from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import TaskJob, Task, TaskSchedule, ScheduleSectionTest
from .serializers import TaskJobSerializer, TaskSerializer, TaskScheduleSerializer, ScheduleSectionTestSerializer
from rest_framework.response import Response
import calendar
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
from .background import generate_task
import json
from django.utils import timezone

executor = ThreadPoolExecutor(max_workers=5)

class TaskJobViewSet(viewsets.ModelViewSet):
    queryset = TaskJob.objects.all()
    serializer_class = TaskJobSerializer
    permission_classes = [IsAuthenticated]
    


    def create(self, request):
        # validity = validateTask(request.data.get("prompt"))

        # if(not validity["valid"]):
        #     return Response(validity["note"], status=400)

        data = request.data.copy()
        data['account'] = request.user.id
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            executor.submit(generate_task, serializer.save())
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def progress(self, request):
        response = []
        tasks = Task.objects.filter(taskjob__account = request.user)
        for task in tasks:
            response.append(
                {'taskId' : task.id,
                 'task' : task.title,
                 'icon' : task.icon,
                 'progress' : (len(TaskSchedule.objects.filter(task = task, status = 'complete'))/len(TaskSchedule.objects.filter(task = task)))*100
                 }
            )
        return Response(response)
    
    def list(self, request):
        response = []
        reload = False

        for task in Task.objects.filter(taskjob__account = request.user):
            tmp = {}
            tmp["id"] = task.id
            tmp["task"]  = task.title
            tmp["icon"] = task.icon
            tmp["startDate"] = task.taskjob.start_date.strftime('%Y %b %d').upper()
            tmp["endDate"] = task.taskjob.end_date.strftime('%Y %b %d').upper()
            tmp["progress"] = (len(TaskSchedule.objects.filter(task = task, status = 'complete'))/len(TaskSchedule.objects.filter(task = task)))*100
            tmp["remaining"] = f"{len(TaskSchedule.objects.filter(task = task, status = 'remaining'))} DAYS"
            response.append(tmp)

        for task in TaskJob.objects.filter(account = request.user, generated = False):
            response.append({"id" : 10000000000000000000000000})
            reload = True
        
        #tmp["startDate"] = datetime.strptime(task.taskjob.start_date, '%Y-%m-%d').strftime('%Y %b %d').upper()
           

        return Response({"reload" : reload , "data" : response})
    
    def roadmap(self, request, pk):
        return Response({"success" : True})

    def retrieve(self, request, pk):
        task = Task.objects.filter(taskjob__account = request.user, id = pk)

        if(len(task) == 0):
            return Response({"success" : False})
        
        response = {"success" : True, "data" : []}
        for (index, schedule) in enumerate(TaskSchedule.objects.filter(task = task[0]).order_by('date', 'startTime')):
            tmp = {"index" : index + 1, "id" : schedule.id, "heading" : schedule.heading, "icon" : schedule.icon, "status" : schedule.status, "date" : schedule.date, "startTime" : schedule.startTime, "endTime" : schedule.endTime, "link" : f"/tasks/{task[0].id}/{schedule.id}/"}
            response["data"].append(tmp)
        return Response(response)

class TaskScheduleViewSet(viewsets.ModelViewSet):
    queryset = TaskSchedule.objects.all()
    serializer_class = TaskScheduleSerializer

    def list(self, request):
        return Response(TaskSchedule.objects.filter(task__taskjob__account = request.user).values('id', 'heading', 'date', 'task__taskjob__theme_color', 'startTime', 'endTime' ))

    def get_today_schedules(self, request):
        return Response(TaskSchedule.objects.filter(task__taskjob__account = request.user, date = datetime.now()).values('id', 'icon', 'heading', 'task__id', 'task__title', 'startTime', 'endTime'))

    def schedules_calendar(self, request, task, year, month):
        schedules = TaskSchedule.objects.filter(task__taskjob__account = request.user, task = task, date__gte = f'{year}-{month}-01', date__lte = f'{year}-{month}-{calendar.monthrange(year, month)[1]}')
        
        response = []

        for schedule in schedules:
            response.append({"status" : schedule.status, "index" : int(str(schedule.date).split('-')[-1])})

        return Response(response)
    
    def retrieve(self, request, pk):
        schedule = TaskSchedule.objects.filter(id = pk, task__taskjob__account = request.user)

        if(schedule.exists()):
            schedule = schedule[0]
            schedule.accessRecord = timezone.now()
            schedule.save()
            return Response({"content" : schedule.content, "status" : schedule.status, "title" : schedule.heading})
        return Response({"success" : False},400)
    
    def status_toggle(self, request, pk):
        schedule = TaskSchedule.objects.filter(id = pk, task__taskjob__account = request.user)

        if(schedule.exists()):
            schedule = schedule[0]
            schedule.status = "remaining" if schedule.status == "completed" else "completed"
            schedule.save()
            return Response({"status" : schedule.status})
        return Response({"success" : False},400)
    
    def chat(self, request, pk, index):
        return Response({"response" : f"I'm Bot {pk} {index}"})

        
    def test(self, request, id, index, type):
        schedule = TaskSchedule.objects.filter(id = id, task__taskjob__account = request.user)
        print(type)
        if(schedule.exists()):
            content = schedule[0].content
            questions = 10
            if(type == 1):
                    choices = 5
                    prompt = (f"Consider {json.loads(content)[index]['html']} and generate {questions} MCQ with {choices}. They must be more reasonable, sensible and practical questions. I need them in form of [{{index : index, question : question, choices : [{{'index' : 'index', 'choice' : 'choice' }}] }}]")
                    questions = [
    {
        "index": 1,
        "question": "What year was Python first released?",
        "choices": [
            {"index": 1, "choice": "1980"},
            {"index": 2, "choice": "1991"},
            {"index": 3, "choice": "2000"},
            {"index": 4, "choice": "2005"}
        ]
    },
    {
        "index": 2,
        "question": "Who created Python?",
        "choices": [
            {"index": 1, "choice": "Guido van Rossum"},
            {"index": 2, "choice": "Dennis Ritchie"},
            {"index": 3, "choice": "Bjarne Stroustrup"},
            {"index": 4, "choice": "James Gosling"}
        ]
    },
    {
        "index": 3,
        "question": "Which of the following is NOT a reason to learn Python?",
        "choices": [
            {"index": 1, "choice": "Easy to read and write"},
            {"index": 2, "choice": "Extensive library support"},
            {"index": 3, "choice": "Complicated syntax"},
            {"index": 4, "choice": "Versatile use cases"}
        ]
    },
    {
        "index": 4,
        "question": "Where can you download Python?",
        "choices": [
            {"index": 1, "choice": "https://www.python.org/"},
            {"index": 2, "choice": "https://www.microsoft.com/"},
            {"index": 3, "choice": "https://www.apple.com/"},
            {"index": 4, "choice": "https://www.google.com/"}
        ]
    },
    {
        "index": 5,
        "question": "Which of the following is the correct syntax to print 'Hello, World!' in Python?",
        "choices": [
            {"index": 1, "choice": "print(Hello, World!)"},
            {"index": 2, "choice": "echo 'Hello, World!'"},
            {"index": 3, "choice": "console.log('Hello, World!')"},
            {"index": 4, "choice": "print('Hello, World!')"}
        ]
    },
    {
        "index": 6,
        "question": "Which data type is used to store numbers in Python?",
        "choices": [
            {"index": 1, "choice": "int"},
            {"index": 2, "choice": "string"},
            {"index": 3, "choice": "list"},
            {"index": 4, "choice": "bool"}
        ]
    },
    {
        "index": 7,
        "question": "How do you run a Python program from the command line?",
        "choices": [
            {"index": 1, "choice": "python filename.py"},
            {"index": 2, "choice": "run filename.py"},
            {"index": 3, "choice": "execute filename.py"},
            {"index": 4, "choice": "python3 filename.py"}
        ]
    },
    {
        "index": 8,
        "question": "Which of the following is an example of a variable in Python?",
        "choices": [
            {"index": 1, "choice": "name = 'John'"},
            {"index": 2, "choice": "int(10)"},
            {"index": 3, "choice": "print()"},
            {"index": 4, "choice": "'hello world'"}
        ]
    },
    {
        "index": 9,
        "question": "What is the correct way to define a string variable in Python?",
        "choices": [
            {"index": 1, "choice": "name = 'John'"},
            {"index": 2, "choice": "string name = 'John'"},
            {"index": 3, "choice": "var name = 'John'"},
            {"index": 4, "choice": "name = John"}
        ]
    },
    {
        "index": 10,
        "question": "Which of the following is NOT a feature of Python?",
        "choices": [
            {"index": 1, "choice": "Cross-platform compatibility"},
            {"index": 2, "choice": "High performance in system-level programming"},
            {"index": 3, "choice": "Strong community support"},
            {"index": 4, "choice": "Extensive library support"}
        ]
    }
]
                    return Response({"questions" : questions})
            elif(type == 2):
                    prompt = (f"Consider {json.loads(content)[index]['html']} and generate {questions} essay questions. They must be more reasonable, sensible and practical questions. I need them in form of [{{index : index, question : question}}]")        
                    
                    questions = [
    {
        "index": 1,
        "question": "Explain why Python is considered a beginner-friendly programming language."
    },
    {
        "index": 2,
        "question": "Discuss the significance of Python's simple and readable syntax in its widespread adoption."
    },
    {
        "index": 3,
        "question": "How has Python's community support contributed to its growth and popularity?"
    },
    {
        "index": 4,
        "question": "Describe the different use cases of Python and explain why it is considered versatile."
    },
    {
        "index": 5,
        "question": "What are the key advantages of Python's cross-platform compatibility, and how does it benefit developers?"
    },
    {
        "index": 6,
        "question": "Why is Python's extensive library support one of its most powerful features?"
    },
    {
        "index": 7,
        "question": "What steps should a beginner take to start learning Python, and how can the official Python website assist in this process?"
    },
    {
        "index": 8,
        "question": "Describe the role of variables in Python, providing examples of how they are used in the language."
    },
    {
        "index": 9,
        "question": "How do you run a Python program from the command line, and why is this important for a developer?"
    },
    {
        "index": 10,
        "question": "Discuss the advantages of Python for both beginners and experienced developers in different fields like web development, data analysis, and machine learning."
    }
]

                    return Response({"questions" : questions})

            elif(type == 3):
                    prompt = (f"Consider {json.loads(content)[index]['html']} and generate {questions} programming questions. They must be more reasonable, sensible and practical questions. I need them in form of [{{index : index, question : question}}]")        
                    print(prompt)
                    questions = [
    {
        "index": 1,
        "question": "Write a Python program to print 'Hello, World!' to the console."
    },
    {
        "index": 2,
        "question": "Create a Python program that stores your name and age in variables, then prints a message 'My name is [name] and I am [age] years old.'"
    },
    {
        "index": 3,
        "question": "Write a Python program that accepts a user's name and age as input and prints a message 'Hello [name], you are [age] years old.'"
    },
    {
        "index": 4,
        "question": "Write a Python program that uses variables to store the radius of a circle and calculates the area of the circle (Area = π * radius^2)."
    },
    {
        "index": 5,
        "question": "Write a Python program that asks the user for their favorite color and prints 'Your favorite color is [color].'"
    },
    {
        "index": 6,
        "question": "Create a Python program that defines a function `greet(name)` which takes a name as an argument and prints 'Hello, [name]!'"
    },
    {
        "index": 7,
        "question": "Write a Python program that takes two numbers from the user and prints their sum."
    },
    {
        "index": 8,
        "question": "Write a Python program that accepts a string input from the user and prints the string in uppercase."
    },
    {
        "index": 9,
        "question": "Write a Python program that calculates the perimeter of a rectangle, given its length and width."
    },
    {
        "index": 10,
        "question": "Write a Python program that takes a filename as input and prints the contents of the file."
    }
]

                    return Response({"questions" : questions})
       
        return Response({"message" : "Invalid Request"},400)
    
class ScheduleSectionTestViewSet(viewsets.ModelViewSet):
    queryset = ScheduleSectionTest.objects.all()
    serializer_class = ScheduleSectionTestSerializer
    permission_classes = [IsAuthenticated] 

    def eval(self, request, id, index, type, pk):
        objs = ScheduleSectionTest.objects.filter(schedule = id, sectionIndex = index, type = type, id = pk)
        if(objs.exists()):
            obj = objs[0]
            return Response({"answers" : json.loads(obj.answers), "questions" : json.loads(obj.questions)})
        return Response({"success" : False}, 400)

    def fetch_tests(self, request, id, type, index):
        return Response([{"id" : test.id, "text" : "Test"} for test in ScheduleSectionTest.objects.filter(schedule = id, sectionIndex = index, type = type)])


    def save(self, request):
        questions = json.loads(request.data["questions"])
        answers = json.loads(request.data["answers"])
        postdata = request.data

        if(postdata.get("type") == "mcq"):  
            for index, question in enumerate(questions):
                print(question["index"] in answers)
                print(question["index"], answers)
                questions[index]['selected'] = answers[str(question["index"])] if str(question["index"]) in answers else None

            prompt = f"""
                {json.dumps(questions)}

                Evaluate 'selected' choice with the given question and give me the output in form of
                {{"total_questions" : total questions count, "correct_answers" : correct answers count, "answers" : [{{"index" : question index, "answer" : correct choice index, "info" : small description explaining the answer}}]}}

            """

            generatedAnswers = {
    "total_questions": 10,
    "correct_answers": 5,
    "answers": [
        {
        "index": 1,
        "answer": 2,
        "info": "Python was first released in 1991 by Guido van Rossum."
        },
        {
        "index": 2,
        "answer": 1,
        "info": "Guido van Rossum is the creator of Python. The selected answer (4 - James Gosling) is incorrect, as he created Java."
        },
        {
        "index": 3,
        "answer": 3,
        "info": "Python is known for its simplicity and readability. 'Complicated syntax' is NOT a reason to learn Python, making this the correct answer."
        },
        {
        "index": 4,
        "answer": 1,
        "info": "Python can be downloaded from its official website: https://www.python.org/. The selected answer is correct."
        },
        {
        "index": 5,
        "answer": 4,
        "info": "The correct syntax to print 'Hello, World!' in Python is print('Hello, World!'). The selected answer (3 - console.log('Hello, World!')) is incorrect as it is JavaScript syntax."
        },
        {
        "index": 6,
        "answer": 1,
        "info": "Python uses 'int' to store whole numbers and 'float' for decimal numbers. No answer was selected."
        },
        {
        "index": 7,
        "answer": 1,
        "info": "A Python program can be run using 'python filename.py' or 'python3 filename.py'. The selected answer (4 - python3 filename.py) is also correct."
        },
        {
        "index": 8,
        "answer": 1,
        "info": "In Python, variables are assigned using '=', e.g., name = 'John'. The selected answer is correct."
        },
        {
        "index": 9,
        "answer": 1,
        "info": "Strings in Python are assigned using single or double quotes, e.g., name = 'John'. The selected answer is correct."
        },
        {
        "index": 10,
        "answer": 2,
        "info": "Python is not designed for high performance in system-level programming like C or Rust. The selected answer is correct."
        }
    ]
    }

            serializer = self.serializer_class(data={"schedule" : postdata.get('schedule'), "sectionIndex" : postdata.get('sectionIndex'), "questions" : postdata.get('questions'), "answers" : json.dumps({"eval" : generatedAnswers["answers"], "given" : answers}), "marks" : int(generatedAnswers["correct_answers"]) * 100/ int(generatedAnswers["total_questions"]), "type" : "mcq"})

            if(serializer.is_valid()):
                return Response({"success" : True, "active" : serializer.save().id, "tests" : [{"id" : test.id, "text" : "Test"} for test in ScheduleSectionTest.objects.filter(schedule = postdata.get('schedule'), type = "mcq", sectionIndex = postdata.get('sectionIndex'))]})
            return Response({"success" : False}, 400)

        if(postdata.get("type") == "essay"):
            print(questions)
            print(answers)
            for index, question in enumerate(questions):
                print(question["index"] in answers)
                print(question["index"], answers)
                questions[index]['answer'] = answers[str(question["index"])] if str(question["index"]) in answers else None

            prompt = f"""
                ```{json.dumps(questions)}
                ```
                Evaluate each question with answer and give me the output in form of python dictionary
                {{"total_questions" : total questions count, "correct_answers" : correct answers count, "answers" : [{{"index" : question index, "correct" : (python True/False), "give "answer" : complete correct answer with a feedback. even the ansswer given or not, i need correct answer}}]}}

            """

           


            generatedAnswers = {
    "total_questions": 10,
    "correct_answers": 0,
    "answers": [
        {
            "index": 1,
            "correct": False,
            "answer": "Incorrect. The response 'czd' does not explain why Python is considered a beginner-friendly programming language. A correct answer would mention Python's simple, readable syntax, its extensive documentation, a supportive community, and its widespread use in educational contexts."
        },
        {
            "index": 2,
            "correct": False,
            "answer": "No answer provided. A correct answer would highlight Python's simple and readable syntax, which is designed to be intuitive and close to human language, making it easier for beginners to learn and understand."
        },
        {
            "index": 3,
            "correct": False,
            "answer": "No answer provided. A correct answer would mention how Python's active community provides extensive resources, tutorials, libraries, and frameworks, all contributing to the growth and popularity of Python."
        },
        {
            "index": 4,
            "correct": False,
            "answer": "No answer provided. Python is versatile because it supports a wide range of applications such as web development, data analysis, machine learning, automation, and scripting. Its cross-platform support and vast ecosystem make it suitable for diverse use cases."
        },
        {
            "index": 5,
            "correct": False,
            "answer": "No answer provided. Python's cross-platform compatibility allows developers to write code that runs on Windows, macOS, and Linux without modification. This reduces development time and effort, as well as increases the portability of applications."
        },
        {
            "index": 6,
            "correct": False,
            "answer": "No answer provided. Python's extensive library support is one of its most powerful features, as it includes libraries for web development, data science, machine learning, and more. This helps developers solve complex problems with minimal code."
        },
        {
            "index": 7,
            "correct": False,
            "answer": "No answer provided. A beginner should start by installing Python, using resources such as the official Python website, tutorials, and online communities. The Python website offers documentation, guides, and examples that are helpful for getting started."
        },
        {
            "index": 8,
            "correct": False,
            "answer": "No answer provided. Variables in Python are used to store data values. For example, 'x = 5' assigns the value 5 to the variable 'x'. Variables can store different types of data, including integers, floats, strings, and more."
        },
        {
            "index": 9,
            "correct": False,
            "answer": "No answer provided. To run a Python program from the command line, you can use the command 'python scriptname.py'. This is important for developers because it allows them to test their code, debug, and deploy it in different environments."
        },
        {
            "index": 10,
            "correct": False,
            "answer": "No answer provided. Python offers advantages for beginners and experienced developers alike. Its readability and simplicity make it ideal for beginners, while its versatility and powerful libraries make it suitable for professionals working in web development, data analysis, machine learning, and other fields."
        }
    ]
}
            
            serializer = self.serializer_class(data={"schedule" : postdata.get('schedule'), "sectionIndex" : postdata.get('sectionIndex'), "questions" : postdata.get('questions'), "answers" : json.dumps({"eval" : generatedAnswers["answers"], "given" : answers}), "marks" : int(generatedAnswers["correct_answers"]) * 100/ int(generatedAnswers["total_questions"]), "type" : "essay"})

            if(serializer.is_valid()):
                return Response({"success" : True, "active" : serializer.save().id, "tests" : [{"id" : test.id, "text" : "Test"} for test in ScheduleSectionTest.objects.filter(schedule = postdata.get('schedule'), type = "essay", sectionIndex = postdata.get('sectionIndex'))]})
            return Response({"success" : False}, 400)
        

        if(postdata.get("type") == "code"):
            print(questions)
            print(answers)
            for index, question in enumerate(questions):
                print(question["index"] in answers)
                print(question["index"], answers)
                questions[index]['answer'] = answers[str(question["index"])] if str(question["index"]) in answers else None

            prompt = f"""
                ```{json.dumps(questions)}
                ```
                Evaluate each question with answer and give me the output in form of python dictionary
                {{"total_questions" : total questions count, "correct_answers" : correct answers count, "inline comment charactor stream" : languge comment charater stream. for and example '#' for python '//' for javascript, "answers" : [{{"index" : question index, "correct" : (python True/False), "answer" : correct code, "note" : note on the code }}]}}

            """

            print(prompt)
           


            generatedAnswers = {
    "total_questions": 10,
    "correct_answers": 0,
    "inline comment charactor stream": "#",
    "answers": [
        {
            "index": 1,
            "correct": False,
            "answer": "print('Hello, World!')",
            "note": "Provided answer 'dsad' is incorrect.",
            "inline comment charactor stream": "#"
        },
        {
            "index": 2,
            "correct": False,
            "answer": "name = 'John'\nage = 25\nprint(f'My name is {name} and I am {age} years old.')",
            "note": "No answer provided.",
            "inline comment charactor stream": "#"
        },
        {
            "index": 3,
            "correct": False,
            "answer": "name = input('Enter your name: ')\nage = input('Enter your age: ')\nprint(f'Hello {name}, you are {age} years old.')",
            "note": "No answer provided.",
            "inline comment charactor stream": "#"
        },
        {
            "index": 4,
            "correct": False,
            "answer": "import math\nradius = 5\narea = math.pi * radius ** 2\nprint(f'Area of circle: {area}')",
            "note": "No answer provided.",
            "inline comment charactor stream": "#"
        },
        {
            "index": 5,
            "correct": False,
            "answer": "color = input('Enter your favorite color: ')\nprint(f'Your favorite color is {color}.')",
            "note": "No answer provided.",
            "inline comment charactor stream": "#"
        },
        {
            "index": 6,
            "correct": False,
            "answer": "def greet(name):\n    print(f'Hello, {name}!')",
            "note": "No answer provided.",
            "inline comment charactor stream": "#"
        },
        {
            "index": 7,
            "correct": False,
            "answer": "num1 = int(input('Enter first number: '))\nnum2 = int(input('Enter second number: '))\nprint(f'Sum: {num1 + num2}')",
            "note": "No answer provided.",
            "inline comment charactor stream": "#"
        },
        {
            "index": 8,
            "correct": False,
            "answer": "text = input('Enter a string: ')\nprint(text.upper())",
            "note": "No answer provided.",
            "inline comment charactor stream": "#"
        },
        {
            "index": 9,
            "correct": False,
            "answer": "length = 5\nwidth = 3\nperimeter = 2 * (length + width)\nprint(f'Perimeter: {perimeter}')",
            "note": "No answer provided.",
            "inline comment charactor stream": "#"
        },
        {
            "index": 10,
            "correct": False,
            "answer": "filename = input('Enter filename: ')\nwith open(filename, 'r') as file:\n    print(file.read())",
            "note": "No answer provided.",
            "inline comment charactor stream": "#"
        }
    ]
}

            serializer = self.serializer_class(data={"schedule" : postdata.get('schedule'), "sectionIndex" : postdata.get('sectionIndex'), "questions" : postdata.get('questions'), "answers" : json.dumps({"eval" : generatedAnswers["answers"], "given" : answers}), "marks" : int(generatedAnswers["correct_answers"]) * 100/ int(generatedAnswers["total_questions"]), "type" : "code"})

            if(serializer.is_valid()):
                return Response({"success" : True, "active" : serializer.save().id, "tests" : [{"id" : test.id, "text" : "Test"} for test in ScheduleSectionTest.objects.filter(schedule = postdata.get('schedule'), type = "code", sectionIndex = postdata.get('sectionIndex'))]})
            return Response({"success" : False}, 400)