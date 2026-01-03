"""
ReAct Agent 实现 - 纯 HTTP 实现
支持多轮对话、Tool Call、多模态（图片）
"""

import json
import requests
from typing import Optional

from .base import Tool, ToolResult, AgentConfig


class ReActAgent:
    """
    ReAct Agent 实现
    
    循环流程:
    1. 发送消息给 LLM（带 tools）
    2. 如果 LLM 返回 tool_calls，执行工具
    3. 将工具结果作为 tool message 加入历史
    4. 重复直到 LLM 返回纯文本或达到最大迭代次数
    """
    
    def __init__(self, config: AgentConfig, system_prompt: str = ""):
        self.config = config
        self.system_prompt = system_prompt
        self.tools: dict[str, Tool] = {}
        self.messages: list[dict] = []
        
        # 初始化系统提示
        if system_prompt:
            self.messages.append({
                "role": "system",
                "content": system_prompt
            })
    
    def register_tool(self, tool: Tool) -> None:
        """注册工具"""
        self.tools[tool.name] = tool
        print(f"[Agent] 注册工具: {tool.name}")
    
    def _get_tools_schema(self) -> list[dict]:
        """获取 OpenAI 格式的 tools schema"""
        return [
            {
                "type": "function",
                "function": {
                    "name": tool.name,
                    "description": tool.description,
                    "parameters": tool.parameters
                }
            }
            for tool in self.tools.values()
        ]
    
    def _trim_old_screenshots(self, max_screenshots: int = 5) -> list[dict]:
        """
        返回消息列表，只保留最近 N 张截图，更早的截图被移除
        
        Args:
            max_screenshots: 最多保留的截图数量
            
        Returns:
            处理后的消息列表（不修改原始 self.messages）
        """
        # 找出所有包含图片的消息索引
        image_indices = []
        for i, msg in enumerate(self.messages):
            content = msg.get("content")
            if isinstance(content, list):
                for item in content:
                    if item.get("type") == "image_url":
                        image_indices.append(i)
                        break
        
        # 如果图片数量不超过限制，直接返回原消息
        if len(image_indices) <= max_screenshots:
            return self.messages
        
        # 需要移除的图片消息索引（保留最近的 max_screenshots 张）
        indices_to_remove = set(image_indices[:-max_screenshots])
        
        # 构建新消息列表，移除旧图片
        trimmed_messages = []
        for i, msg in enumerate(self.messages):
            if i in indices_to_remove:
                # 移除图片，但保留文本部分
                content = msg.get("content")
                if isinstance(content, list):
                    text_parts = [item.get("text", "") for item in content if item.get("type") == "text"]
                    if text_parts:
                        trimmed_messages.append({
                            "role": msg["role"],
                            "content": "[截图已省略] " + " ".join(text_parts)
                        })
                # 如果没有文本部分，直接跳过该消息
            else:
                trimmed_messages.append(msg)
        
        return trimmed_messages
    
    def _call_llm(self) -> dict:
        """调用 LLM API"""
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.config.api_key}"
        }
        
        # 只保留最近 5 张截图
        messages_to_send = self._trim_old_screenshots(max_screenshots=5)
        
        payload = {
            "model": self.config.model,
            "stream": False,
            "messages": messages_to_send,
        }
        
        # 如果有工具，添加 tools 参数
        if self.tools:
            payload["tools"] = self._get_tools_schema()
            payload["tool_choice"] = "auto"
        
        response = requests.post(
            self.config.api_url,
            headers=headers,
            json=payload,
            timeout=self.config.timeout
        )
        
        result = response.json()
        
        if "error" in result:
            raise RuntimeError(f"API 错误: {result['error']}")
        
        return result["choices"][0]["message"]
    
    def _execute_tool(self, name: str, arguments: dict) -> ToolResult:
        """执行工具"""
        if name not in self.tools:
            return ToolResult(text=f"错误: 未知工具 '{name}'")
        
        tool = self.tools[name]
        try:
            result = tool.func(**arguments)
            if isinstance(result, ToolResult):
                return result
            else:
                return ToolResult(text=str(result))
        except Exception as e:
            return ToolResult(text=f"工具执行错误: {e}")
    
    def run(self, user_input: str, image_base64: Optional[str] = None) -> str:
        """
        运行 Agent
        
        Args:
            user_input: 用户输入文本
            image_base64: 可选的图片 base64 编码
            
        Returns:
            Agent 最终回复
        """
        # 构建用户消息
        if image_base64:
            user_content = [
                {"type": "text", "text": user_input},
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/png;base64,{image_base64}"
                    }
                }
            ]
        else:
            user_content = user_input
        
        self.messages.append({
            "role": "user",
            "content": user_content
        })
        
        print(f"\n[User] {user_input}")
        if image_base64:
            print(f"[User] (附带图片，长度: {len(image_base64)})")
        
        # ReAct 循环
        for iteration in range(1, self.config.max_iterations + 1):
            print(f"\n--- 迭代 {iteration}/{self.config.max_iterations} ---")
            
            # 调用 LLM
            message = self._call_llm()
            
            # 检查是否有 tool_calls
            if message.get("tool_calls"):
                # 将 assistant 消息加入历史
                self.messages.append({
                    "role": "assistant",
                    "content": message.get("content"),
                    "tool_calls": message["tool_calls"]
                })
                
                # 处理每个 tool call
                for tool_call in message["tool_calls"]:
                    tool_id = tool_call["id"]
                    tool_name = tool_call["function"]["name"]
                    tool_args_str = tool_call["function"].get("arguments", "{}")
                    
                    try:
                        tool_args = json.loads(tool_args_str)
                    except json.JSONDecodeError:
                        tool_args = {}
                    
                    print(f"[Tool Call] {tool_name}({tool_args})")
                    
                    # 执行工具
                    result = self._execute_tool(tool_name, tool_args)
                    print(f"[Tool Result] {result.text[:100]}..." if len(result.text) > 100 else f"[Tool Result] {result.text}")
                    
                    # 将工具结果加入历史（纯文本）
                    tool_response_text = result.text
                    if result.image_base64:
                        tool_response_text += " 截图已生成，用户将上传截图。"
                        print(f"[Tool Result] (图片将作为 user message 发送，长度: {len(result.image_base64)})")
                    
                    self.messages.append({
                        "role": "tool",
                        "tool_call_id": tool_id,
                        "content": tool_response_text
                    })
                    
                    # 如果有图片，作为 user message 发送
                    if result.image_base64:
                        self.messages.append({
                            "role": "user",
                            "content": [
                                {"type": "text", "text": "这是刚才操作后的屏幕截图，请根据截图继续操作："},
                                {
                                    "type": "image_url",
                                    "image_url": {
                                        "url": f"data:image/png;base64,{result.image_base64}"
                                    }
                                }
                            ]
                        })
                        print("[User] (上传截图)")
            else:
                # 没有 tool_calls，返回最终回复
                final_reply = message.get("content", "")
                self.messages.append({
                    "role": "assistant",
                    "content": final_reply
                })
                print(f"\n[Assistant] {final_reply}")
                return final_reply
        
        # 达到最大迭代次数
        return "[Agent] 达到最大迭代次数，停止执行"
    
    def reset(self) -> None:
        """重置对话历史"""
        self.messages = []
        if self.system_prompt:
            self.messages.append({
                "role": "system",
                "content": self.system_prompt
            })
        print("[Agent] 对话历史已重置")
