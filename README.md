# WeChatGPTBot

微信ChatGPT Bot

## Usage

### Step1 配置chatgpt和openai

更改config.py

OPENAI_KEY: 从https://openai.com/api/ 申请token

AUTHORIZATION: 登录chatgpt，把cookie中的__Secure-next-auth.session-token填这


### Step2 申请token

申请paimon的token
https://wechaty.readthedocs.io/zh_CN/latest/introduction/use-paimon-protocol/
https://wechaty.js.org/docs/puppet-services/paimon

### Step3

export WECHATY_PUPPET_SERVICE_TOKEN=puppet_paimon_xx && python3 main.py

给bot发chat:xxx即可