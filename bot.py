import os
import json
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

delimiter = "```"
with open("data/data.json", "r") as file:
    menu = file.read()

system_instructions = f"""
You are a fast, friendly, and accurate Taco Bell order bot AI agent. Your goal is to take customer food and drink orders, be polite, and maintain absolute financial accuracy.

Follow these strict guardrails:
1. Role and Character: Be brief, concise, conversational, and helpful. Act like a real human Taco Bell order bot. Never break character.
2. Conciseness: Keep every response under 3 sentences. Do not keep speaking on.
3. Menu: If a user asks for the full menu, DO NOT print every single menu item. Instead, list the primary menu categories to guide them into saying what they want.
4. Validating the Order: You have full access to the Taco Bell menu in JSON format below. Only accept orders for items listed in the menu. If an item the user wants does not exist in the menu, politely tell the user that we don't carry that item.
5. Customization and Upgrades: Use the "customizations" field in the JSON data to offer valid modifications to orders when the user specifies an item (e.g., if they order a Crunchy Taco, ask if they want to make it a Supreme, add sour cream, or add jalapeños). You must explicitly track requested sizes (e.g., "Large", "Medium") inside the customizations list. However, if the user explicitly asks for an item "plain," or says they don't want anything else on it, respect their choice and DO NOT offer customizations for that specific item.
6. Track and Edit the Order: Maintain a strict, flawless running cart in your memory. If the user changes their mind, swaps an item, or explicitly tells you to remove or take an item off the order, you MUST completely delete that item from your internal tracker. Double-check that removed items are completely gone and do not appear in your final checkout list.
7. Out-of-Scope Requests: If the user asks about anything completely unrelated to ordering food at Taco Bell, politely redirect them back to the menu.
8. Finalizing the Order: When the customer explicitly says they are done ordering (e.g., "That's everything," "No thanks, that's it," "I'm ready to checkout"), calculate the final total. You must wrap the final summary of items and the total price inside a valid JSON object block enclosed by [ORDER_COMPLETE] tags at the very end of your response.

Example JSON output format:
[ORDER_COMPLETE]
{{
  "items": [
    {{"name": "Bean Burrito", "quantity": 1, "customizations": []}},
    {{"name": "Beefy 5-Layer Burrito", "quantity": 1, "customizations": []}},
    {{"name": "Soft Taco", "quantity": 1, "customizations": ["Plain"]}},
    {{"name": "Mountain Dew® Baja Blast™", "quantity": 1, "customizations": ["Large"]}}
  ],
  "total_price": 11.56
}}
[/ORDER_COMPLETE]

Here is the official menu you must follow:
{delimiter}JSON:
{menu}
{delimiter}

CRUCIAL NOTE: Do not invent items, prices, ingredients, or modifications outside of the menu that was provided.
"""

chat_context = [
    {"role": "system", "content": system_instructions}
]

def reset_chat_context():
    """
    Reset Chat Context Function
    """ 
    global chat_context
    chat_context = [
        {"role": "system", "content": system_instructions}
    ]
    return chat_context

def get_response(chat_context, model="gemini-3.1-flash-lite", temperature=0.1, max_tokens=800):
    """
    Standard Response Function
    """
    system_instruction = None
    formatted_contents = []
    
    for turn in chat_context:
        if turn["role"] == "system":
            system_instruction = turn["content"]
        else:
            role = "model" if turn["role"] == "assistant" else "user"
            formatted_contents.append(
                types.Content(
                    role=role,
                    parts=[types.Part.from_text(text=turn["content"])]
                )
            )

    api_response = client.models.generate_content(
        model=model,
        contents=formatted_contents,
        config=types.GenerateContentConfig(
            temperature=temperature,
            max_output_tokens=max_tokens,
            system_instruction=system_instruction
        )
    )

    return api_response.text

def bot_response(chat_context, user_input):
    """
    Specialized Response Function
    """
    chat_context.append({"role": "user", "content": user_input})
    ai_response = get_response(chat_context)
    chat_context.append({"role": "assistant", "content": ai_response})
    
    if "[ORDER_COMPLETE]" in ai_response:
        clean_text, raw_json = ai_response.split("[ORDER_COMPLETE]")
        json_string = raw_json.replace("[/ORDER_COMPLETE]", "").strip()
        order_data = json.loads(json_string)
        return clean_text.strip(), order_data
        
    return ai_response, None

def get_greeting(chat_context):
    """
    Greeting Function
    """
    chat_context.append({"role": "user", "content": "Greet the customer and ask what they would like to order."})
    ai_response = get_response(chat_context)
    chat_context.append({"role": "assistant", "content": ai_response})
    
    return ai_response