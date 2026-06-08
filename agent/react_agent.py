"""
ReAct Agent
构建智能体
"""
from langchain.agents import create_agent
from model.factory import chat_model
from utils.prompt_loader import load_system_prompt
from agent.tools.agent_tools import (get_weather, rag_summarize, get_user_id, get_current_month, get_location_city,
                                     fill_context_for_report,fetch_external_data )
from agent.tools.middleware import monitor_tool, log_before_model, report_prompt_switch


class ReActAgent:
    def __init__(self):
        """
        Initialize the agent with necessary components including model, system prompt, tools, and middleware.
        This constructor sets up the agent with various capabilities for handling different tasks.
        """
        self.agent = create_agent(
            model=chat_model,  # Specify the chat model to be used by the agent
            system_prompt=load_system_prompt(),  # Load the system prompt that guides the agent's behavior
            tools=[get_weather, rag_summarize, get_user_id, get_current_month, get_location_city,  # List of tools the agent can use
                   fill_context_for_report,fetch_external_data],
            middleware=[monitor_tool, log_before_model, report_prompt_switch  # Middleware components for enhanced functionality
                        ]
        )

    def execute_stream(self, query: str):
        input_dict = {
            "messages": [
                {"role": "user", "content": query}
            ]
        }
        # 第三个参数context是上下文runtime中的信息，动态切换提示词的标记
        for chunk in self.agent.stream(input=input_dict, stream_mode="values", context={"report": False}):
            latest_message = chunk["messages"][-1]
            if latest_message.content:
                yield latest_message.content.strip() + "\n"


if __name__ == '__main__':
    agent = ReActAgent()
    for chunk in agent.execute_stream("给我生成我的使用报告"):
        print(chunk, end="", flush=True)
