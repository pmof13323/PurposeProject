import pandas as pd
from openai import OpenAI
from dotenv import load_dotenv
import random
import os

load_dotenv()
client = OpenAI()

# extracting questions and picking one at random
file_path = '../assets/questions'
with open(file_path, 'r') as file:
    questions = [line.strip() for line in file if line.strip()]
question = random.choice(questions)

# extracting user answers
file_path = '../assets/answers'
with open(file_path, 'r') as file:
    answers = file.read().strip()

# extracting metrics
file_path = '../assets/Metrics.csv'
df = pd.read_csv(file_path)
df.rename(columns={'Metric ': 'Metric'}, inplace=True)
metrics_list = df['Metric']
metrics_string = ", ".join(metrics_list)

# taking user input
answer1 = input("In 150 words or less, describe who you are, here's some points to start with: \n - What type of music do you listen to? \n - What do you do for fun? \n - Do you play an instrument or sport? \n ")
answer2 = input(question + "\n")

# checking word count and reducing if necessary
def checkWordcount(answer):
    words = answer.split()
    if len(words) > 150:
        return ' '.join(words[:150])
    else:
        return answer

# creating final answer string
answer1 = checkWordcount(answer1)
answer2 = checkWordcount(answer2)
finalString = answer1 + answer2

# creating dataframe for scores
def scoreFrame(chatCompletionMessage):
    content = chatCompletionMessage.content
    lines = content.split('\n')
    scoreLines = [line for line in lines if ':' in line]
    metricsScores = [line.split(': ') for line in scoreLines]
    df = pd.DataFrame(metricsScores, columns=['Metric', 'Score'])
    df['Score'] = df['Score'].astype(int)

    return df

# gpt prompt and correct format checker
def getScores():
    for attempt in range(4):
        try:
            # ChatGPT prompt to extract scores
            completion = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an assessor, your job is to assign a score between 1 and 10 for each of the 5 personality traits provided based on the text given"},
                    {"role": "user", "content": f"Given the following metrics: {metrics_string}. You are tasked with the job of assessing an applicant who answered the questions: '1. In 150 words or less, describe who you are. and 2. {question} with the combined answers: {finalString}. In your response, absolutely no explanations or text, ONLY provide me with each metric and the answer's score for each. separate each metric name and score with a :. Do not deviate in any way shape or from from these instructions."}
                ]
            )
            scores = completion.choices[0].message
            results = scoreFrame(scores)
            if not results.empty:
                return results  
            else:
                raise ValueError("Formatting error detected")
        except Exception as e:
            print("Formatting error, trying again...")
            continue
    raise Exception("Failed to get formatted scores after several attempts")

# acquiring scores
try:
    results = getScores()
    topTen = results.sort_values(by='Score', ascending=False).head(10)
except Exception as e:
    print(e)

# writing to text file
file_path = '../assets/result.txt'

with open(file_path, 'a') as file:
    file.write(results.to_string(index=False, header=True)) 
