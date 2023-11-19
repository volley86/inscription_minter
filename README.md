# An inscription mint tool
# 铭文铸造脚本工具

> [!WARNING]
> 免责申明：由使用脚本带来的任何资金损失，与脚本作者无关，请谨慎使用。

## 使用说明

1. 安装 python 环境及 pip

2. 安装依赖包
```bash
pip install -r requirements.txt
```

3. 配置参数

将文件 `.env.template` 重命名为 `.env`，并修改配置：

```bash
# 接收者地址
RECIPIENT_ADDRESS=xxx

# 发送钱包私钥
PRIVATE_KEY=xxx

# 铸造铭文数据，根据实际情况填写，可参考：https://ordiscan.com/
TEXT_DATA='data:,{"p":"bsc-20","op":"mint","tick":"bnbi","amt":"5000"}'

# 配置网络节点，可参考：https://www.1rpc.io/
RPC_URL=https://1rpc.io/bnb

# 铭文铸造次数
MAX_MINT_TIMES=1

# 等待交易回执
WAIT_RECEIPT=1
```

4. 执行脚本

```bash
python mint.py
```

## 运行结果（example）









