import pandas as pd
from openai import OpenAI
from dotenv import load_dotenv
import random

load_dotenv()
client = OpenAI()

# extracting questions and picking one at random NOTE: randomise functionality not being used in this test case
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

#print("In 150 words or less, describe who you are, here's some points to start with: \n - What type of music do you listen to? \n - What do you do for fun? \n - Do you play an instrument or sport? \n ")
answer1 = answers
#print(question)
answer2 = answers

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

# NOTE: we are only using "if you woke up" question in this test prompt
completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are an assessor to a question on a test, your job is to assign a score between 1 and 10 for each of the 40 metrics provided to you for an answer to a test question"},
        {"role": "user", "content": f"Given the following metrics: {metrics_string}. You are tasked with the job of assessing an applicant who answered the questions: '1. In 150 words or less, describe who you are. and 2. Imagine you wake up one morning and all humans have disappeared, what do you do? with the answers: {finalString}. In your response, don't give me any explanations, just provide me with each metric and the answer's score for each. separate each metric name and number with a : so i can deal with it easily in my code"}
    ]
)

scores = completion.choices[0].message
# print(scores)

# creating dataframe for scores
def scoreFrame(chatCompletionMessage):
    content = chatCompletionMessage.content
    lines = content.split('\n')
    scoreLines = [line for line in lines if ':' in line]
    metricsScores = [line.split(': ') for line in scoreLines]
    df = pd.DataFrame(metricsScores, columns=['Metric', 'Score'])
    df['Score'] = df['Score'].astype(int)

    return df

results = scoreFrame(scores)
print(results)