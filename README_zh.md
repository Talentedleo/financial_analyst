# 金融分析 AI 代理系统

> 基于 Google ADK + LiteLLM + MiniMax 的多代理股票分析系统，提供知名投资大师的分析视角

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.12-blue.svg)](https://www.python.org/)
[![Google ADK](https://img.shields.io/badge/Google%20ADK-Latest-green.svg)](https://adk.dev/)
[![MiniMax](https://img.shields.io/badge/MiniMax-M2.7--highspeed-red.svg)](https://www.minimax.chat/)
[![Language: English](https://img.shields.io/badge/-English-blue?style=flat-square)](README.md)

---

## 功能特性

- **直接专家路由**：无需协调层，直接调用专家代理
- **ADK Skills**：每位专家使用 Google 官方 SkillToolset 实现投资理念
- **实时数据**：Finnhub（免费）+ Yahoo Finance（高级）提供市场数据
- **投资大师视角**：11 位投资大师（巴菲特、芒格、伍德、林奇等）
- **推送通知**：集成 Bark 实现 iOS 推送通知
- **REST API**：基于 FastAPI，支持会话管理

---

## 环境要求

- **Python 3.12+**（Google ADK 要求）

---

## 快速开始

### 1. 安装 Python 3.12

```bash
brew install python@3.12
```

### 2. 创建虚拟环境

```bash
cd ~/Desktop/sandbox/financial_analyst
python3.12 -m venv venv
source venv/bin/activate
```

### 3. 安装依赖

```bash
pip install -r requirements.txt
```

### 4. 配置环境变量

```bash
cp .env.example .env
# 编辑 .env 填入你的 API keys
```

### 5. 运行测试

```bash
python tests/test_main.py
```

### 6. 启动 API 服务

```bash
python main.py
```

---

## API 接口

| 接口 | 方法 | 描述 |
|------|------|------|
| `/` | GET | API 信息 |
| `/health` | GET | 健康检查 |
| `/agents` | GET | 查看可用专家代理 |
| `/analyze` | POST | 使用专家视角分析股票 |
| `/search` | POST | 搜索股票数据 |
| `/clear-session` | POST | 清除对话会话 |

### 请求示例

```bash
# Warren Buffett 分析
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -H "X-API-Key: sk-1234" \
  -d '{"question": "NVDA值得购买吗？", "style": "warren_buffett"}'

# Charlie Munger 分析
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -H "X-API-Key: sk-1234" \
  -d '{"question": "AAPL怎么样？", "style": "charlie_munger"}'

# Cathie Wood 分析
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -H "X-API-Key: sk-1234" \
  -d '{"question": "TSLA值得买吗？", "style": "cathie_wood"}'
```

### 专家代理

| style 参数 | 专家 | 投资理念 |
|------------|------|----------|
| `warren_buffett` | Warren Buffett | 价值投资、护城河分析 |
| `cathie_wood` | Cathie Wood | 颠覆性创新、高增长 |
| `charlie_munger` | Charlie Munger | 多元思维模型 |
| `greg_abel` | Greg Abel | 运营卓越、伯克希尔视角 |
| `peter_lynch` | Peter Lynch | 成长投资、知道自己拥有什么 |
| `benjamin_graham` | Benjamin Graham | 安全边际、防守型投资 |
| `phil_fisher` | Phil Fisher | 成长股、闲聊法 |
| `michael_burry` | Michael Burry | 逆向投资、泡沫识别 |
| `bill_ackman` | Bill Ackman | 激进投资、高置信度 |
| `stanley_druckenmiller` | Stanley Druckenmiller | 宏观投资、集中押注 |
| `aswath_damodaran` | Aswath Damodaran | 估值、叙事投资 |

---

## 架构

```
用户提问
    ↓
┌─────────────────────────────────────┐
│          直接专家代理                  │
│   （根据 style 参数选择）              │
├─────────────────────────────────────┤
│  - 读取 ADK SkillToolset           │
│  - 获取实时数据                      │
│  - 运用投资框架分析                  │
│  - 第一人称回答                      │
└─────────────────────────────────────┘
    ↓
┌─────────────────────────────────────┐
│          数据服务                     │
├──────────────┬──────────────────────┤
│   Finnhub   │   Yahoo Finance      │
│ (行情/新闻)  │     (K线数据)        │
└──────────────┴──────────────────────┘
    ↓
LiteLlm → MiniMax-M2.7-highspeed
    ↓
JSON 响应 + Bark 推送通知
```

---

## 项目结构

```
financial_analyst/
├── main.py                    # 入口文件
├── requirements.txt           # 依赖包
├── .env.example             # 环境变量模板
├── agents/
│   ├── __init__.py
│   └── experts/
│       ├── __init__.py
│       └── factory.py       # 动态专家代理工厂
├── tools/
│   ├── __init__.py
│   ├── stock_tools.py       # 行情、搜索、K线
│   ├── news_tools.py        # 公司和市场新闻
│   ├── fundamentals_tools.py # 资料、同行、财务
│   └── bark_tools.py        # iOS 推送通知
├── services/
│   ├── __init__.py
│   ├── llm_service.py      # LLM 服务（MiniMax）
│   ├── data_service.py      # Finnhub + yfinance
│   └── skill_loader.py      # Skill 加载工具
├── skills/                   # ADK Skills（11 位专家）
│   ├── warren_buffett/
│   ├── cathie_wood/
│   ├── charlie_munger/
│   ├── greg_abel/
│   ├── peter_lynch/
│   ├── benjamin_graham/
│   ├── phil_fisher/
│   ├── michael_burry/
│   ├── bill_ackman/
│   ├── stanley_druckenmiller/
│   └── aswath_damodaran/
├── api/
│   ├── __init__.py
│   └── routes.py            # FastAPI 路由
└── tests/
    └── test_main.py         # 测试套件（22 个测试）
```

---

## 专家代理

每位专家代理执行以下流程：
1. 读取 ADK SkillToolset 学习投资理念
2. 使用工具获取实时数据
3. 运用 Skill 的框架进行分析
4. 以第一人称回答，问题使用什么语言就用什么语言回答

### ADK Skills

使用 Google 官方 `load_skill_from_dir` 和 `SkillToolset` 加载：

```python
from google.adk.skills import load_skill_from_dir
from google.adk.tools.skill_toolset import SkillToolset

skill = load_skill_from_dir(Path("skills/warren_buffett"))
skill_toolset = SkillToolset(skills=[skill])

Agent(..., tools=[..., skill_toolset])
```

---

## 数据来源

### Finnhub（免费）

| 功能 | 描述 |
|------|------|
| 股票行情 | 实时价格、涨跌幅、成交量 |
| 公司新闻 | 公司相关新闻 |
| 市场新闻 | 财经新闻 |
| 公司资料 | 业务信息、行业 |
| 股票搜索 | 按名称/代码搜索 |
| 财务指标 | 营收、P/E、ROE 等 |

### Yahoo Finance（yfinance）

| 功能 | 描述 |
|------|------|
| K线数据 | 历史 OHLCV 数据 |

---

## 推送通知（Bark）

```bash
# 在 .env 中配置
BARK_DEVICE_KEY=你的设备密钥
BARK_SERVER_URL=https://api.day.app
```

---

## 测试结果

```
Total: 22 | Passed: 22 | Failed: 0 (100.0%)
```

---

## 参考资料

- [Google ADK](https://github.com/google/adk-python)
- [LiteLLM](https://docs.litellm.ai/)
- [MiniMax](https://www.minimax.chat/)
- [Finnhub API](https://finnhub.io/)
- [Yahoo Finance (yfinance)](https://github.com/ranaroussi/yfinance)
- [Bark](https://github.com/Finb/Bark)

---

## License

MIT License
