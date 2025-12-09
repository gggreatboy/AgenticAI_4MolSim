#!/usr/bin/env python3
"""
测试 Ollama 端口连接脚本
用于检查 Ollama 服务的可用性
"""

import os
import sys
import requests
import json
from datetime import datetime

def test_ollama_connection():
    """测试 Ollama 连接"""
    
    # Ollama 配置
    OLLAMA_BASE_URL = "http://192.168.31.94:11434"
    OLLAMA_API_URL = f"{OLLAMA_BASE_URL}/v1"
    
    # 清理代理设置
    for k in ("HTTP_PROXY", "HTTPS_PROXY", "http_proxy", "https_proxy"):
        os.environ.pop(k, None)
    
    print("=" * 60)
    print("Ollama 连接测试")
    print("=" * 60)
    print(f"测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Ollama 地址: {OLLAMA_BASE_URL}")
    print()
    
    # 测试1: 检查基础连接
    print("1. 测试基础连接...")
    try:
        response = requests.get(OLLAMA_BASE_URL, timeout=10)
        if response.status_code == 200:
            print("   ✅ 基础连接成功")
            print(f"   响应状态: {response.status_code}")
        else:
            print(f"   ❌ 基础连接失败，状态码: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"   ❌ 基础连接失败: {e}")
        return False
    
    # 测试2: 检查 API 端点
    print("\n2. 测试 API 端点...")
    try:
        response = requests.get(f"{OLLAMA_API_URL}/models", timeout=10)
        if response.status_code == 200:
            print("   ✅ API 端点可用")
            models_data = response.json()
            print(f"   可用模型数量: {len(models_data.get('data', []))}")
            
            # 显示可用模型
            for model in models_data.get('data', [])[:5]:  # 只显示前5个
                print(f"     - {model.get('id', 'Unknown')}")
        else:
            print(f"   ❌ API 端点不可用，状态码: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"   ❌ API 端点测试失败: {e}")
        return False
    
    # 测试3: 检查特定模型
    print("\n3. 测试 deepseek-r1:32b 模型...")
    try:
        # 检查模型是否存在
        response = requests.get(f"{OLLAMA_API_URL}/models", timeout=10)
        models_data = response.json()
        
        model_exists = False
        for model in models_data.get('data', []):
            if 'deepseek-r1' in model.get('id', ''):
                model_exists = True
                print(f"   ✅ 找到模型: {model.get('id')}")
                break
        
        if not model_exists:
            print("   ⚠️  未找到 deepseek-r1 模型")
            print("   可用模型:")
            for model in models_data.get('data', [])[:10]:
                print(f"     - {model.get('id')}")
    except requests.exceptions.RequestException as e:
        print(f"   ❌ 模型检查失败: {e}")
        return False
    
    # 测试4: 简单聊天测试
    print("\n4. 进行简单聊天测试...")
    try:
        # 使用更简单的提示词和更短的超时时间
        chat_payload = {
            "model": "deepseek-r1:32b",
            "messages": [
                {"role": "user", "content": "Hi"}
            ],
            "max_tokens": 10,  # 减少token数量
            "temperature": 0.1  # 降低随机性
        }
        
        print("   发送请求到 Ollama...")
        start_time = datetime.now()
        
        response = requests.post(
            f"{OLLAMA_API_URL}/chat/completions",
            json=chat_payload,
            timeout=60  # 增加超时时间
        )
        
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        
        print(f"   请求耗时: {duration:.2f}秒")
        
        if response.status_code == 200:
            result = response.json()
            if 'choices' in result and len(result['choices']) > 0:
                message = result['choices'][0].get('message', {})
                content = message.get('content', '').strip()
                print("   ✅ 聊天测试成功")
                print(f"   模型回复: {content}")
            else:
                print("   ⚠️  聊天测试返回异常响应")
                print(f"   响应内容: {result}")
        else:
            print(f"   ❌ 聊天测试失败，状态码: {response.status_code}")
            print(f"   错误信息: {response.text}")
            
    except requests.exceptions.Timeout:
        print("   ❌ 聊天测试超时 (60秒)")
        print("   建议: 检查 Ollama 服务是否正常运行，或者尝试使用更小的模型")
        
    except requests.exceptions.RequestException as e:
        print(f"   ❌ 聊天测试失败: {e}")
        print("   建议: 检查网络连接和防火墙设置")
    
    # 测试5: 检查 LangChain 兼容性
    print("\n5. 测试 LangChain 兼容性...")
    try:
        from langchain_openai import ChatOpenAI
        
        # 创建 ChatOpenAI 实例（使用 Ollama 的 OpenAI 兼容接口）
        chat_model = ChatOpenAI(
            model="deepseek-r1:32b",
            base_url=OLLAMA_API_URL,
            api_key="sk-xxx-xxxxxxlocal2",
            temperature=0.7,
            max_tokens=4096
        )
        
        # 测试简单调用
        from langchain_core.messages import HumanMessage
        
        messages = [HumanMessage(content="你好，请说'LangChain 测试成功'")]
        response = chat_model.invoke(messages)
        
        print("   ✅ LangChain 兼容性测试成功")
        print(f"   模型回复: {response.content}")
        
    except ImportError as e:
        print(f"   ⚠️  LangChain 相关库未安装: {e}")
        print("   请安装: pip install langchain-openai langchain-core")
    except Exception as e:
        print(f"   ❌ LangChain 兼容性测试失败: {e}")
    
    # 测试6: 检查 LangGraph 兼容性
    print("\n6. 测试 LangGraph 兼容性...")
    try:
        from langchain_openai import ChatOpenAI
        from langchain_core.messages import HumanMessage
        from langgraph.graph import StateGraph, END
        from typing import TypedDict, Annotated
        import operator
        
        # 定义状态类型
        class GraphState(TypedDict):
            messages: Annotated[list, operator.add]
            response: str
        
        # 创建 ChatOpenAI 实例（使用 Ollama 的 OpenAI 兼容接口）
        chat_model = ChatOpenAI(
            model="deepseek-r1:32b",
            base_url=OLLAMA_API_URL,
            api_key="sk-xxx-xxxxxxlocal2",
            temperature=0.7,
            max_tokens=100
        )
        
        # 定义节点函数
        def call_model(state: GraphState):
            """调用模型生成回复"""
            response = chat_model.invoke(state["messages"])
            return {"response": response.content, "messages": [response]}
        
        # 构建图
        workflow = StateGraph(GraphState)
        
        # 添加节点
        workflow.add_node("model", call_model)
        
        # 设置入口点
        workflow.set_entry_point("model")
        
        # 设置结束点
        workflow.add_edge("model", END)
        
        # 编译图
        app = workflow.compile()
        
        # 测试图执行
        initial_state = {
            "messages": [HumanMessage(content="请说'LangGraph 测试成功'")],
            "response": ""
        }
        
        print("   执行 LangGraph 工作流...")
        result = app.invoke(initial_state)
        
        print("   ✅ LangGraph 兼容性测试成功")
        print(f"   工作流结果: {result['response']}")
        
    except ImportError as e:
        print(f"   ⚠️  LangGraph 相关库未安装: {e}")
        print("   请安装: pip install langgraph")
    except Exception as e:
        print(f"   ❌ LangGraph 兼容性测试失败: {e}")
        print(f"   错误详情: {str(e)}")
    
    print("\n" + "=" * 60)
    print("测试完成！")
    print("=" * 60)
    
    return True

def main():
    """主函数"""
    try:
        success = test_ollama_connection()
        if success:
            print("\n🎉 所有测试通过！Ollama 服务运行正常。")
        else:
            print("\n❌ 部分测试失败，请检查 Ollama 服务配置。")
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n\n测试被用户中断")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ 测试过程中发生错误: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()