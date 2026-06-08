"""
中间件
"""
from typing import Callable

from langchain.agents import AgentState
from langchain.agents.middleware import wrap_tool_call, before_model, dynamic_prompt, ModelRequest
from langchain_core.messages import ToolMessage
from langchain.tools.tool_node import ToolCallRequest
from langgraph.runtime import Runtime
from langgraph.types import Command
from utils.logger_handler import logger
from utils.prompt_loader import load_system_prompt, load_rag_prompt, load_report_prompt


@wrap_tool_call
def monitor_tool(request: ToolCallRequest,
                 handler: Callable[[ToolCallRequest], ToolMessage | Command]) -> ToolMessage | Command:
    """
    工具调用监控
    :param request: 请求的数据
    :param handler: 执行的函数本身
    :return:
    """
    print(request)
    logger.info(f"[monitor_tool]调用工具：{request.tool_call['name']}")
    logger.info(f"[monitor_tool]传入参数：{request.tool_call['args']}")
    try:
        response = handler(request)
        logger.info(f"[monitor_tool]调用结果：{response.name}")

        # 只要模型调用了fill_context_for_report工具，就会进行标记
        if request.tool_call['name'] == 'fill_context_for_report':
            request.runtime.context['report'] = True

        return response
    except Exception as e:
        logger.error(f"[monitor_tool]工具{request.tool_call['name']}调用失败，原因：{str(e)}")
        raise e


@before_model
def log_before_model(state: AgentState, runtime: Runtime) -> None:
    """
    state:整个agent智能体中的状态记录
    runtime:记录整个智能体中的运行时的上下文信息
    模型调用前日志
    :return:
    """
    logger.info(f"[log_before_model]模型调用前日志：带有{len(state['messages'])}条上下文信息")

    logger.debug(
        f"[log_before_model]类型名称：{type(state['messages'][-1].name)}|消息内容：{state['messages'][-1].content.strip()}")
    return None


# dynamic_prompt 每一次生成提示词之前，调用此函数
# 动态切换提示词
@dynamic_prompt
def report_prompt_switch(request: ModelRequest):
    """
    报告生成提示词切换
    :return:
    """
    # 获取上下文中的标记，默认为False
    is_report = request.runtime.context.get('report', False)
    # True ,则是需要生成报告的场景，返回报告生成提示词
    if is_report:
        return load_report_prompt()

    return load_system_prompt()
