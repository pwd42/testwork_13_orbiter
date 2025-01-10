from aiohttp import ClientSession
from client import Client
from config import ZERO_ADDRESS, ORBITER_IDENTIFICATION_CODE


class Orbiter:
    def __init__(self, client: Client, logger = None):
        self.client = client
        self.logger = logger

    @staticmethod
    async def make_request(
            method: str = 'GET', url: str = None, params: dict = None, headers: dict = None, json: dict = None
    ):
        async with ClientSession() as session:
            async with session.request(method=method, url=url, params=params, headers=headers, json=json) as response:
                if response.status in [200, 201]:
                    return await response.json()
                raise RuntimeError(f"Bad request to OpenOcean API. Response status: {response.status}")

    async def get_bridge_data(self, src_chain_id: int, dst_chain_id: int):
        url = "https://api.orbiter.finance/sdk/routers/v2"
        headers = {
            "accept": "application/json",
            "content-type": "application/json"
        }

        response = await self.make_request('GET', url=url, headers=headers)

        bridge_data_all = response['result']
        bridge_data = []

        for entry in bridge_data_all:
            if entry["srcChain"] == str(src_chain_id) and entry["tgtChain"] == str(dst_chain_id)\
                    and entry["srcToken"] == ZERO_ADDRESS and entry["tgtToken"] == ZERO_ADDRESS:
                bridge_data.append(entry)
        self.logger.info(f"bridge_data[0] - {bridge_data[0]}")

        return bridge_data[0]

    async def bridge_eth(self, src_chain_id: int, dst_chain_id: int, amount: int):
        bridge_data = await self.get_bridge_data(src_chain_id, dst_chain_id)
        # to = ORBITER_CONTRACTS[dst_chain_id]["router"]
        to = bridge_data['endpoint']
        value = amount + ORBITER_IDENTIFICATION_CODE[dst_chain_id]

        transaction = await self.client.prepare_tx(value=value) | {
            'to': self.client.w3.to_checksum_address(to),
            'data': "0x",
            'gas': 600000
        }
        self.logger.info(f"transaction bridge - {transaction}")

        result = await self.client.send_transaction(transaction)

        return result
