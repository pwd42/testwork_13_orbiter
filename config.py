import json

RPC_URLS = {
    "Arbitrum": "https://endpoints.omniatech.io/v1/arbitrum/one/public",
    "Optimism": "https://op-pokt.nodies.app",
    # "Base": "https://1rpc.io/base"
    "Base": "https://base-pokt.nodies.app",
    # "Base": "https://base.meowrpc.com"
    # "Base": "https://base.drpc.org"
    "ZkSync":"https://1rpc.io/zksync2-era",
    # "ZkSync":"https://endpoints.omniatech.io/v1/zksync-era/mainnet/public",
    "Scroll":"https://scroll.drpc.org"
}

EXPLORERS_URL = {
    "Arbitrum": "https://arbiscan.io/",
    "Optimism": "https://optimistic.etherscan.io/",
    "Base": "https://basescan.org/",
    "ZkSync":"https://era.zksync.network/",
    # "ZkSync": "https://explorer.zksync.io/"
    "Scroll":"https://scrollscan.com/"
}

CHAIN_ID_BY_NAME = {
    'Arbitrum': 42161,
    'Optimism': 10,
    'Base': 8453
}

ETH_MASK = "0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE"
ZERO_ADDRESS = "0x0000000000000000000000000000000000000000"

# ORBITER_CONTRACTS = {
#     42161: {
#         'router': "0x6a065083886EC63d274b8E1fE19aE2ddF498bFDd",
#         # 'LToken': "0x0D8F8e271DD3f2fC58e5716d3Ff7041dBe3F0688"
#     },
#     8453: {
#         'router': "0x13E46b2a3f8512eD4682a8Fb8B560589fE3C2172",
#         # 'LToken': "0x0D8F8e271DD3f2fC58e5716d3Ff7041dBe3F0688"
#     }
# }

ORBITER_IDENTIFICATION_CODE = {
    42161: 9002,
    8453: 9021
}

TOKENS_PER_CHAIN = {
    'Arbitrum': {
        "ETH": "0x82aF49447D8a07e3bd95BD0d56f35241523fBab1",
        # "WETH": "0x82aF49447D8a07e3bd95BD0d56f35241523fBab1"
        "USDC": "0xaf88d065e77c8cC2239327C5EDb3A432268e5831"
    },
    'Optimism': {
        "ETH": "0x4200000000000000000000000000000000000006",
        # "WETH": "0x4200000000000000000000000000000000000006",
        "USDC":"0x0b2C639c533813f4Aa9D7837CAf62653d097Ff85"
    },
    'Base': {
        "ETH" : "0x4200000000000000000000000000000000000006",
        # "ETH": "0x0000000000000000000000000000000000000000",
        # "WETH": "0x4200000000000000000000000000000000000006",
        "USDC": "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913"
    },
    'ZkSync': {
        "ETH": "0x000000000000000000000000000000000000800A",
        "WETH": "0x5aea5775959fbc2557cc8789bc1bf90a239d9a91",
        "USDC": "0x1d17CBcF0D6D143135aE902365D2E5e2A16538D4",
        "USDT": "0x493257fD37EDB34451f62EDf8D2a0C418852bA4C"
    },
    'Scroll': {
        "ETH": "0x5300000000000000000000000000000000000004",
        "WETH": "0x5300000000000000000000000000000000000004",
        "USDC": "0x06eFdBFf2a14a7c8E15944D1F4A48F9F95F663A4",
    }
}

with open('erc20_abi.json') as file:
    ERC20_ABI = json.load(file)




