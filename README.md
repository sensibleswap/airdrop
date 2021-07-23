# 空投sensible ft脚本

## 安装
```npm i```

## 空投

### 1 生成mc的地址列表mc_balance.json
```
python3 ft.py gettoken mc
```

### 2 修改配置文件
```
cp ft_config_template.json ft_config.json
```
修改配置
```
{
    "network": "testnet",
    "wif": "",
    "codehash": "777e4dd291059c9f7a0fd563f7204576dcceb791",
    "genesis": "e616a7e2367f640485e8f9148a0320e4a71ab83f",
    "address_file": "mc_balance.json"
}
```
- network: mainnet or testnet
- wif: 私钥
- codehash: 要空投的ft的codehash
- genesis： 要空投的ft的genesis
- address_file: 空投的地址列表

### 3 运行
```
ts-node index.ts
```

## 发币

根据自己需要修改代码里
```
    let { txid, genesis, codehash, sensibleId } = await ft.genesis({
        genesisWif: config.wif,
        tokenName: "testnet coin",
        tokenSymbol: "test",
        decimalNum: 8,
      });
    const issueAmount = "1000000000000000"
```
然后运行
```
ts-node index.ts issue
```