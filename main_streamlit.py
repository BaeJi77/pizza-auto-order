import json

import requests
import streamlit as st
from openai import OpenAI

from dto import OrderDTO

st.title("auto order pizza")

role = f'''
너는 pizza 주문을 해주는 bot이야. 유저가 요구하는 것을 파악해서 어떤 피자를 주문할지 정해주는 역할이야. 유저가 추천해달라고하면 그것에 맞춰서 잘 추천해줄 수 있을 정도로 피자에 대한 지식을 가지고 있어. 유저가 피자와 관련되지 않은 내용에 대해서는 피자 주문만을 처리할 수 있다고 할 수 있어.
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

input_role = f'''
- 반드시 pizza 하나는 주문해야 됩니다.
- 토핑은 반드시 pizza와 같이 연결되어서 주문되어야 됩니다.
- 배달과 픽업을 나눠서 요청할 수 있습니다.
  - 배달인 경우 이름, 주소, 연락처를 알아야됩니다.
  - 픽업인 경우 소요시간을 말해줘야 됩니다.
'''

output_role = f'''
- 유저가 원하는 메뉴가 없다고 판단되면 해당 메뉴가 없다고 말해줘.
- 메뉴 선택시와 주문을 진행하는 중간 중간에 가격에 대해서 알려줘.
'''

system_prompt = f'''
# role
{role}

# pizza menu
{pizza_menu}

# input role
{input_role}

# output role
{output_role}
'''

pizza_order_functions = [
    {
        "name": "order_pizza",
        "description": "고객의 주문에 따라 피자와 관련 상품을 주문합니다.",
        "parameters": {
            "type": "object",
            "properties": {
                "pizzas": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "type": {
                                "type": "string",
                                "description": "피자 종류, e.g. Margherita, Pepperoni"
                            },
                            "size": {
                                "type": "string",
                                "description": "피자 크기, e.g. Small, Medium, Large"
                            }
                        },
                        "required": ["type", "size"]
                    }
                },
                "sides": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "item": {
                                "type": "string",
                                "description": "사이드 메뉴 아이템, e.g. Garlic Bread, Chicken Wings"
                            },
                            "size": {
                                "type": "string",
                                "description": "사이드 메뉴 크기, e.g. Small, Large",
                                "default": "Medium"
                            }
                        },
                        "required": ["item"]
                    }
                },
                "toppings": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "topping": {
                                "type": "string",
                                "description": "추가 토핑, e.g. Extra Cheese, Mushrooms"
                            }
                        }
                    }
                },
                "beverages": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "beverage": {
                                "type": "string",
                                "description": "음료, e.g. Coke, Sprite"
                            },
                            "size": {
                                "type": "string",
                                "description": "음료 크기, e.g. 500ml, 1L",
                                "default": "500ml"
                            }
                        }
                    }
                },
                "total_price": {
                    "type": "integer",
                    "description": "주문의 총 가격, 0 이상이어야 합니다.",
                    "minimum": 0
                }
            },
            "required": ["pizzas", "total_price"]
        }
    }
]


def order_pizza(order: OrderDTO):
    url = "http://localhost:8000/order"

    # POST 요청을 보내고 응답을 받습니다.
    res = requests.post(url, json=order)

    # 응답 데이터를 확인합니다.
    if res.status_code == 200:
        print("Order was successful!")
        return res.json()  # JSON 응답을 파싱하여 반환합니다.
    else:
        print("Order failed with status code:", res.status_code)
        return None


client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": system_prompt}
    ]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        for response in client.chat.completions.create(
                model=st.session_state["openai_model"],
                messages=[
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ],
                functions=pizza_order_functions,
                function_call='auto',
                stream=True,
        ):
            # json_response = json.loads()
            print(response.choices[0])
            full_response += (response.choices[0].delta.content or "")
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)
    st.session_state.messages.append({"role": "assistant", "content": full_response})
