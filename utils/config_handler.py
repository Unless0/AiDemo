"""
配置文件：yaml
key: value
"""
import yaml
from utils.path_tool import get_abs_path


def load_rag_config(config_path: str = get_abs_path("config\\rag.yaml"), encoding: str = "utf-8"):
    with open(config_path, encoding=encoding) as f:
        config = yaml.load(f, Loader=yaml.FullLoader)
    return config


def load_chroma_config(config_path: str = get_abs_path("config\\chroma.yaml"), encoding: str = "utf-8"):
    with open(config_path, encoding=encoding) as f:
        config = yaml.load(f, Loader=yaml.FullLoader)
    return config


def load_prompts_config(config_path: str = get_abs_path("config\\prompts.yaml"), encoding: str = "utf-8"):
    with open(config_path, encoding=encoding) as f:
        config = yaml.load(f, Loader=yaml.FullLoader)
    return config


def load_agent_config(config_path: str = get_abs_path("config\\agent.yaml"), encoding: str = "utf-8"):
    with open(config_path, encoding=encoding) as f:
        config = yaml.load(f, Loader=yaml.FullLoader)
    return config


# 加载配置文件
rag_conf = load_rag_config()
chroma_conf = load_chroma_config()
prompts_conf = load_prompts_config()
agent_conf = load_agent_config()

if __name__ == '__main__':
    print(rag_conf["chat_model_name"])
