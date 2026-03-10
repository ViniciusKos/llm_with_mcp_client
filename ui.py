import gradio as gr
from langchain.messages import AIMessage, HumanMessage  
from test import main

agent = None

async def get_agent():
    global agent
    if agent is None:
        agent = await main()
    return agent

async def predict(message, history):
    ag = await get_agent()
    history_langchain_format = []
    for msg in history:
        if msg["role"] == "user":
            history_langchain_format.append(HumanMessage(content=msg["content"]))
        elif msg["role"] == "assistant":
            history_langchain_format.append(AIMessage(content=msg["content"]))
    history_langchain_format.append(HumanMessage(content=message))
    gpt_response = await ag.ainvoke({"messages": history_langchain_format})
    return gpt_response["messages"][-1].content


demo = gr.ChatInterface(
    predict,
    api_name="chat")

if __name__ == "__main__":
    demo.launch()