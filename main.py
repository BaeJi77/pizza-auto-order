from openai import OpenAI


def read_openai_key(file_path):
    # 파일을 열고 내용을 읽은 후 출력합니다.
    try:
        with open(file_name, 'r') as file:
            api_key = file.read().strip()  # strip()을 사용하여 양쪽의 공백과 개행 문자를 제거합니다.

        return api_key
    except FileNotFoundError:
        print(f"Error: The file '{file_name}' was not found.")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


file_name = 'openai.key'
client = OpenAI(api_key=read_openai_key(file_name))

student_1_description = ("David Nguyen is a sophomore majoring in computer science at Stanford University. He is Asian "
                         "American and has a 3.8 GPA. David is known for his programming skills and is an active "
                         "member of the university's Robotics Club. He hopes to pursue a career in artificial "
                         "intelligence after graduating.")

# A simple prompt to extract information from "student_description" in a JSON format.
prompt1 = f'''
Please extract the following information from the given text and return it as a JSON object:

name
major
school
grades
club

This is the body of text to extract the information from:
{student_1_description}
'''

# Generating response back from gpt-3.5-turbo
openai_response = client.chat.completions.create(
    model='gpt-3.5-turbo',
    messages=[{'role': 'user', 'content': prompt1}]
)

print(openai_response.choices[0].message.content)
