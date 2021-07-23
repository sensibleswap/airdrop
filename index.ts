import fs = require('fs')
import { SensibleFT } from "sensible-sdk"
const bsv = require('bsv')

let ft
let config

async function sleep(delay: number) {
    await new Promise(resolve => setTimeout(resolve, delay));
}

async function init() {
    config = JSON.parse(fs.readFileSync('ft_config.json').toString())
    const { signers, signerSelecteds } = await SensibleFT.selectSigners();
    ft = new SensibleFT({
        network: config.network, //mainnet or testnet
        purse: config.wif, //the wif of a bsv address to offer transaction fees
        feeb: 0.5,
        signers,
        signerSelecteds,
    });
}

async function airdrop() {
    const path = config.address_file
    const balanceData = JSON.parse(fs.readFileSync(path).toString())


    let receivers = []
    let count = 0
    let airdropAmount = 10000
    for (const k of Object.keys(balanceData) ) {
        if (k !== 'sum') {
            const address = bsv.Address.fromPublicKeyHash(bsv.Address(k).hashBuffer, config.network).toString()
            receivers.push({
                address,
                //amount: String(balanceData[k])
                amount: airdropAmount,
            })
        }
        count += 1
        if (count >= 99) {
            let { txid } = await ft.transfer({ 
                senderWif: config.wif,
                receivers,
                codehash: config.codehash,
                genesis: config.genesis,
            })
            console.log('transfer txid:', txid)
            count = 0
            receivers = []
            // wait 3s for the utxo update
            await sleep(3000)
        }
    }

    if (receivers.length > 0) {
        let { txid } = await ft.transfer({ 
            senderWif: config.wif,
            receivers,
            codehash: config.codehash,
            genesis: config.genesis,
        })
        console.log('transfer txid:', txid)
    }
}

async function issue() {
    let { txid, genesis, codehash, sensibleId } = await ft.genesis({
        genesisWif: config.wif,
        tokenName: "testnet coin",
        tokenSymbol: "test",
        decimalNum: 8,
      });

    console.log(genesis, codehash, sensibleId)

    let { txid2 } = await ft.issue({
        genesis: genesis,
        codehash: codehash,
        sensibleId: sensibleId,
        genesisWif: config.wif,
        receiverAddress: config.address,
        tokenAmount: "100000000000",
        allowIncreaseIssues: false, //if true then you can issue again
      });
      console.log("genesis ", txid, ", token ", txid2)
}

async function main() {
    await init()
    //await issue()
    await airdrop()
}

main()