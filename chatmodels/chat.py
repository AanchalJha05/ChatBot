
from langchain_core.messages import AIMessage, SystemMessage, HumanMessage
from dotenv import load_dotenv

load_dotenv()
 
from langchain.chat_models import init_chat_model

model = init_chat_model(
    "google_genai:gemini-3.6-flash",
    thinking_level="low",
    max_tokens=512
)

print("Choose your AI mode")
print("Press 1 for Angry mode")
print("Press 2 for Funny mode")
print("Press 3 for Sad mode")

choice = int(input("Tell your response: "))

if choice == 1:
    mode = "You are an angry AI agent. You respond aggressively and impatiently."
elif choice == 2:
    mode = "You are a very funny AI agent. You respond with humor and jokes."
elif choice == 3:
    mode = "You are a very sad AI agent. You respond in a sad and emotional tone."
else:
    print("Invalid choice!")
    exit()

messages = [
    SystemMessage(content=mode)
]

print("---- Welcome! Type 0 to exit the application ----")

while True:

    prompt = input("You : ")

    if prompt == "0":
        break

    messages.append(HumanMessage(content=prompt))

    try:
        response = model.invoke(messages)

        messages.append(AIMessage(content=response.content))

        if isinstance(response.content, list):
            answer = "".join(
                block["text"]
                for block in response.content
                if block.get("type") == "text"
            )
        else:
            answer = response.content

        print("AI :", answer)

    except Exception as e:
        print("Error :", e)
        messages.pop()  # Remove failed user message

print("Goodbye!")


