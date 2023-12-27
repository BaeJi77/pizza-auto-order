from openai import OpenAI


def read_openai_key(file_path):
    # 파일을 열고 내용을 읽은 후 출력합니다.
    try:
        with open(file_path, 'r') as file:
            api_key = file.read().strip()  # strip()을 사용하여 양쪽의 공백과 개행 문자를 제거합니다.

        return api_key
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


def get_openai_client():
    file_name = 'openai.key'
    return OpenAI(api_key=read_openai_key(file_name))


role = f'''
너는 pizza 주문을 해주는 bot이야. 유저가 요구하는 것을 파악해서 어떤 피자를 주문할지 정해주는 역할이야. 유저가 추천해달라고하면 그것에 맞춰서 잘 추천해줄 수 있을 정도로 피자에 대한 지식을 가지고 있어.
'''

pizza_menu = f'''
# Pizzas

| Pizza Type     | Large   | Medium  | Small   |
| -------------- | ------- | ------- | ------- |
| Pepperoni Pizza| 15,000원| 12,000원| 8,000원 |
| Cheese Pizza   | 13,000원| 11,000원| 7,000원 |
| Eggplant Pizza | 14,000원| 11,000원| 8,000원 |

# Sides

| Side Item      | Large   | Small   |         |
| -------------- | ------- | ------- | ------- |
| French Fries   | 5,000원 | 4,000원 |         |
| Greek Salad    |         |         | 9,000원 |

# Toppings

| Topping        | Price   |
| -------------- | ------- |
| Extra Cheese   | 2,000원 |
| Mushrooms      | 2,000원 |
| Sausage        | 3,000원 |
| Canadian Bacon | 4,000원 |
| AI Sauce       | 2,000원 |
| Bell Peppers   | 1,000원 |

# Beverages

| Beverage       | Large   | Medium  | Small   |
| -------------- | ------- | ------- | ------- |
| Cola           | 3,000원 | 2,000원 | 1,000원 |
| Sprite         | 3,000원 | 2,000원 | 1,000원 |
| Bottled Water  |         |         | 5,000원 |
'''

output_role = f'''
- 유저가 원하는 메뉴가 없다고 판단되면 해당 메뉴가 없다고 말해줘.
'''

system_prompt = f'''
# role
{role}

# pizza menu
{pizza_menu}

# output role
{output_role}
'''


def get_openai_response(client, user_request):
    # Generating response back from gpt-3.5-turbo
    return client.chat.completions.create(
        model='gpt-3.5-turbo',
        messages=[
            {'role': 'system', 'content': system_prompt},
            {'role': 'user', 'content': user_request}
        ]
    )


def order_pizza():
    return


user_request = f'''
나는 불고기 피자를 먹고 싶어. 알아서 주문해줘.
'''

if __name__ == '__main__':
    client = get_openai_client()

    response = get_openai_response(client, user_request)

    print(response.choices[0].message.content)
