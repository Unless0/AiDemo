import time

from agent.react_agent import ReActAgent
import streamlit as st

# 启动命令 ：streamlit run app.py


# 标题
st.title("智能客服")
st.divider()

if "agent" not in st.session_state:
    st.session_state["agent"] = ReActAgent()

if "messages" not in st.session_state:
    st.session_state["messages"] = []

if st.session_state["messages"]:
    # 回显历史对话
    for message in st.session_state["messages"]:
        st.chat_message(message["role"]).write(message["content"])
# 用户输入
user_input = st.chat_input()
if user_input:
    st.chat_message("user").write(user_input)
    # 添加用户的提问
    st.session_state["messages"].append({"role": "user", "content": user_input})

    response_messages = []
    # 等待
    with st.spinner("Is thinking..."):
        # 获取回答
        res_stream = st.session_state["agent"].execute_stream(user_input)


        def capture(generator, cache_list):
            for chunk in generator:
                cache_list.append(chunk)
                # 流式输出一个字符
                for char in chunk:
                    time.sleep(0.01)
                    yield char


        st.chat_message("assistant").write_stream(capture(res_stream, response_messages))
        # 添加回答
        st.session_state["messages"].append({"role": "assistant", "content": response_messages[-1]})
        # 刷新页面
        st.rerun()
