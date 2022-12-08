# -*- coding: utf-8 -*-
# @Time    : 12/6/22 12:02 PM
# @FileName: chat.py
# @Software: PyCharm
# @Github    ：sudoskys

# 基于 Completion 上层
from openai_async import Completion


class Chatbot(object):
    def __init__(self, api_key, conversation_id):
        """
        chatGPT 的实现由上下文实现，所以我会做一个存储器来获得上下文
        :param api_key:
        :param conversation_id: 独立ID,每个场景需要独一个
        """
        self._api_key = api_key
        self.conversation_id = conversation_id
        self._start_sequence = "\nGirl:"
        self._restart_sequence = "\nHuman: "

    def record_ai(self, prompt, response):
        REPLY = []
        Choice = response.get("choices")
        if Choice:
            for item in Choice:
                _text = item.get("text")
                REPLY.append(_text)
        if not REPLY:
            REPLY = ["(Ai Say Nothing)"]
        return REPLY

    def get_hash(self):
        import hashlib
        my_string = str(self.conversation_id)
        # 使用 hashlib 模块中的 sha256 算法创建一个散列对象
        hash_object = hashlib.sha256(my_string.encode())
        return hash_object.hexdigest()

    async def get_chat_response(self, prompt: str, max_tokens: int = 150, model: str = "text-davinci-003",
                                character: list = None, head: str = None) -> dict:
        """
        异步的，得到对话上下文
        :param head: 预设技巧
        :param max_tokens: 限制返回字符数量
        :param model: 模型选择
        :param prompt: 提示词
        :param character: 性格提示词，列表字符串
        :return:
        """
        if head is None:
            head = f"\nHuman: 你好，你是谁？\nAI: 我是由OpenAI创造的人工智能。我怎么帮你?"
        if character is None:
            character = ["helpful", "creative", "clever", "friendly", "lovely"]
        _character = ",".join(character)
        _now = f"{self._restart_sequence}{prompt}."
        # 构建 prompt 上下文，由上下文桶提供支持
        _head = f"The following is a conversation with chatGPT Ai assistant. The assistant is {_character}."
        _head = f"{_head}\n{head}\n"
        # 截断器
        _old_list = []
        total_length = 0
        cutoff_index = -1
        for i in reversed(range(len(_old_list))):
            string_length = len(_old_list[i])
            total_length += string_length
            # 检查总长度是否超过了限制
            if total_length > 3333 * 4:
                cutoff_index = i
                break
        _old_list = _old_list[:cutoff_index]
        _old_prompt = '\n'.join(_old_list)  # 首个不带 \n
        _prompt = f"{_head}{_old_prompt}{_now}\n{self._start_sequence}"
        _prompt = _prompt[:3800 * 4]
        response = await Completion(api_key=self._api_key).create(
            model=model,
            prompt=_prompt,
            temperature=0.9,
            max_tokens=max_tokens,
            top_p=1,
            n=1,
            frequency_penalty=0,
            presence_penalty=0.6,
            user=str(self.get_hash()),
            stop=["Human:", "AI:"],
        )
        self.record_ai(prompt=prompt, response=response)
        return response
