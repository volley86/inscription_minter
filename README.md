# An inscription mint script
# 铭文铸造脚本

> [!WARNING]
> 免责申明：由因使用脚本铸造铭文带来的任何损失，与本作者无关，请谨慎使用。

## 使用说明

1. 安装 python 环境及 pip

不知道的 google 下 ~

2. 安装 python 依赖包
```sh
pip install -r requirements.txt
```

3. 配置参数

编辑 `.env` 文件，修改如下配置：

```sh
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

4. 运行脚本

```sh
python mint.py
```

执行结果：

<img width="499" alt="image" src="https://github.com/seandong/inscription_minter/assets/758427/80af5816-1d0a-42ab-bb03-5cfc5f79e7bf">









