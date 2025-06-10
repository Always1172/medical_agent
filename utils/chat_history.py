# medical_agent/utils/chat_history.py
from .redis_client import RedisClient
import os

class ChatHistory:
    def __init__(self, user_id="default_user"):
        """初始化聊天记录管理，使用 Redis 存储"""
        # 从环境变量获取 Redis 配置，默认本地开发配置
        redis_host = os.getenv("REDIS_HOST", "localhost")
        redis_port = int(os.getenv("REDIS_PORT", 6379))
        redis_db = int(os.getenv("REDIS_DB", 0))
        redis_password = os.getenv("REDIS_PASSWORD", None)
        
        self.redis_client = RedisClient(
            host=redis_host,
            port=redis_port,
            db=redis_db,
            password=redis_password
        )
        self.user_id = user_id
        
    def save_message(self, user_input, response, tool_used=None):
        """保存新的聊天消息"""
        message = {
            "user_input": user_input,
            "response": response,
            "tool_used": tool_used
        }
        self.redis_client.save_chat_message(self.user_id, message)
        
    def get_history(self):
        """获取所有聊天记录"""
        return self.redis_client.get_chat_history(self.user_id)
    
    def clear_history(self):
        """清空聊天记录"""
        self.redis_client.clear_chat_history(self.user_id)