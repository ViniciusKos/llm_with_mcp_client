import gradio as gr
from langchain.messages import AIMessage, AIMessageChunk, HumanMessage
from agent import main

agent = None


async def get_agent():
    global agent
    if agent is None:
        agent = await main()
    return agent


async def predict(message, history):
    try:
        ag = await get_agent()
        history_langchain_format = []

        for msg in history:
            if msg["role"] == "user":
                history_langchain_format.append(
                    HumanMessage(content=msg["content"])
                )
            elif msg["role"] == "assistant":
                history_langchain_format.append(
                    AIMessage(content=msg["content"])
                )

        history_langchain_format.append(HumanMessage(content=message))

        response = ""
        async for mode, data in ag.astream(
            {"messages": history_langchain_format},
            stream_mode=["messages", "debug", "updates"],
        ):
            if mode == "updates":
                for step, step_data in data.items():
                    if step == "tools":
                        for tool_msg in step_data["messages"]:
                            response += f"\n> Calling the tool: 🔧 **{tool_msg.name}**: \n\n"
                        yield response
            elif mode == "messages":
                token, metadata = data
                if isinstance(token, AIMessageChunk) and token.text:
                    response += token.text
                    yield response

    except Exception as e:
        yield f"An error occurred while processing your request: {e}"


demo = gr.ChatInterface(
    predict,
    chatbot=gr.Chatbot(
        resizable=True,
        height="85vh",
        autoscroll=True,
        value=[
            {
                "role": "assistant",
                "content": """Hello! I'm your assistant"""
            }
        ],
    ),
    api_name="chat",
)


if __name__ == "__main__":
    demo.launch()