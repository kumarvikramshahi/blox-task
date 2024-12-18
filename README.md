# BLOX task
NOTE: Help of perplexity.ai is being taken for fixing grammer issue in text answer in Questions 1, and for some code help in Questions 3.

Each question's answers are located in their respective files, along with the corresponding code.
As instructed in assignment Question 1 is mandetory and we need to solve any 2 out of others.
so i have solved Question 1st, 2nd, 3rd, and 4th. 3rd question is not complete i just gave a try but can't solve completly.

## Steps to run code
* clone repo 
```
git clone https://github.com/kumarvikramshahi/blox-task.git
```

* enter folder

```
cd blox-task
```

* make virtual enviroment

```
python3 -m venv venv
```

* activate venv (for mac/linux)

```
source venv/bin/activate
```

* install dependencies

```
pip install -r requirements.txt
```

* To run Question-2 

```
python question_2/question_2.py
```

* To run question_3

```
python question_3/json_parser.py
```

* To run Question_4 (3rd part):-

```
cd question_4
```
```
uvicorn 3_api_with_rate_limiter:app --reload --port 3000
```

* To run Question_4 (2nd part - don't close fastAPI server running in previous question, so open new terminal tab inside question_4 folder):-

```
python 2_20calls_per_min.py
```

* To run Question_4 (1st part)

```
python 1_call_to_rate_limiter.py
```
