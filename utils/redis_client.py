# medical_agent/utils/redis_client.py
import redis
import json
from datetime import datetime
from typing import List, Dict, Any

class RedisClient:
    def __init__(self, host="localhost", port=6379, db=0, password=None):
        """初始化 Redis 连接"""
        self.redis_client = redis.Redis(
            host=host,
            port=port,
            db=db,
            password=password,
            decode_responses=True  # 自动解码为字符串
        )
        
    def save_chat_message(self, user_id: str, message: Dict[str, Any]):
        """保存聊天消息到 Redis"""
        # 生成唯一消息 ID（时间戳+随机数）
        message_id = f"{datetime.now().timestamp()}_{hash(json.dumps(message))}"
        
        # 添加时间戳
        message["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # 使用 Redis Hash 存储消息
        self.redis_client.hset(f"chat_history:{user_id}", message_id, json.dumps(message))
        
        # 保留最近 100 条消息，控制内存使用
        self._trim_chat_history(user_id, max_messages=100)
        
    def get_chat_history(self, user_id: str) -> List[Dict[str, Any]]:
        """获取用户的聊天历史"""
        messages = self.redis_client.hgetall(f"chat_history:{user_id}")
        # 按时间戳排序（键的前缀是时间戳）
        sorted_messages = sorted(messages.items(), key=lambda x: float(x[0].split('_')[0]))
        return [json.loads(msg) for _, msg in sorted_messages]
    
    def clear_chat_history(self, user_id: str):
        """清空用户的聊天历史"""
        self.redis_client.delete(f"chat_history:{user_id}")
    
    def _trim_chat_history(self, user_id: str, max_messages: int = 100):
        """修剪聊天历史，保留最近的消息"""
        messages = self.redis_client.hgetall(f"chat_history:{user_id}")
        if len(messages) > max_messages:
            # 按时间排序，删除最旧的消息
            sorted_message_ids = sorted(messages.keys(), key=lambda x: float(x.split('_')[0]))
            messages_to_delete = sorted_message_ids[:len(messages) - max_messages]
            for msg_id in messages_to_delete:
                self.redis_client.hdel(f"chat_history:{user_id}", msg_id)