import asyncio
import logging

from client import Client
from orbiter import Orbiter
from config import CHAIN_ID_BY_NAME

def init_logger():
    """
    Инициализация логгера
    """
    logging.basicConfig(filename='myapp.log',level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
    logger = logging.getLogger(__name__)
    return logger

def print_available_chains() -> None:
    """
    Вывод доступных сетей согласно настройке в файле config.py
    """
    print(f"\nAvailable chains in app: {[CHAIN_ID_BY_NAME]}\n")

async def init_chain_by_input(logger, value_in_out: str) -> int:
    """
    Указание пользователем сети блокчейна
    """
    while True:
        chain_id = None

        try:
            chain_id = int(input(f"Enter blockchain id for bridge {value_in_out}: "))
        except ValueError as exc:
            print("Blockchain id not integer! Please try again!\n")
            logger.warning(exc)

        if chain_id in CHAIN_ID_BY_NAME.values():
            logger.info("Blockchain correctly!")
            return chain_id
        else:
            print("Blockchain not correctly! Please try again!\n")
            logger.warning("input blockchain not correctly!")

def init_pk_by_input(logger, chain_name) -> str:
    """
    Указание пользователем приватного ключа
    """
    while True:
        pk = input("Enter private key: ")
        try:
            client = Client(pk, chain_name)
            if client.validate_address() and (len(pk) == 66 or len(pk) == 64):
                logger.info("Private  key correctly")
                return pk
            else:
                print("Private key not correctly!")
                logger.warning(f"input private key {pk} not correctly!")
        except Exception as exc:
            print("Private key not correctly!")
            logger.warning(exc)

async def print_balance(client : Client, name_token : str = None) -> None:
    """
    Вывод баланса токена
    """
    decimals =  await client.get_decimals(token_name=name_token)
    balance = client.from_wei_custom(await client.get_balance(name_token), decimals)
    print(f"\nBalance {name_token} token: {balance}  {name_token}")

async def init_amount_in_token_by_input(client: Client, name_code_token_in :str, logger) -> int:
    """
    Указание пользователем кол-ва входного токена для обмена
    """
    while True:
        try:
            amount_input = input(f"\nEnter value of  token for bridge {name_code_token_in} (format example-\"0.1\") or enter \"ALL\" for full balance: ")

            if amount_input == 'ALL':
                if name_code_token_in != client.name_native_token and (await client.get_balance("ETH") > (await client.w3.eth.gas_price) * 4):
                    amount_input_token_for_swap_in_wei = await client.get_balance(name_code_token_in)
                    logger.info(f"check_balance_for_swap_by_ALL {amount_input_token_for_swap_in_wei} {name_code_token_in} is True")
                    return amount_input_token_for_swap_in_wei
                elif name_code_token_in == client.name_native_token and ((await client.get_balance(name_code_token_in) - (await client.w3.eth.gas_price) * 4) > 0):
                    amount_input_token_for_swap_in_wei = (await client.get_balance(name_code_token_in)) - (await client.w3.eth.gas_price) * 4
                    return amount_input_token_for_swap_in_wei

                print("\nNot enough balance for this amount! Please change amount!\n")

            amount_input_token_for_swap = float(amount_input)
            decimals = await client.get_decimals(token_name=name_code_token_in)
            amount_input_token_for_swap_in_wei = client.to_wei_custom(amount_input_token_for_swap, decimals)
            if await check_balance_for_swap(client, logger, amount_input_token_for_swap_in_wei, name_code_token_in):
                logger.info(f"check_balance_for_swap_by_amount for {amount_input_token_for_swap} is True")
                return amount_input_token_for_swap_in_wei
            else:
                print("\nNot enough balance for this amount! Please change amount!\n")
                logger.warning("Balance not enough for input amount nft!")
        except ValueError:
            print("Amount not number! Please try again!\n")
            logger.warning("input amount of token not correctly!")

async def check_balance_for_swap(client : Client, logger, amount_token_for_swap_in_wei, name_code_token_in) -> bool:
    """
    Проверка баланса на возможность транзакции с учетом указанного  пользователем кол-ва токена
    """
    gas_price_wei = (await client.w3.eth.gas_price) * 4
    logger.info(f"gas_estimate: {gas_price_wei} WEI")

    logger.info(f"client balance swap token {name_code_token_in}: {await client.get_balance(name_code_token_in)} WEI")
    logger.info(f"client balance native token ETH: {await client.w3.eth.get_balance(client.address)} WEI")

    if name_code_token_in != client.name_native_token:
        if (await client.get_balance(name_code_token_in) >= amount_token_for_swap_in_wei and
                (await client.w3.eth.get_balance(client.address) > gas_price_wei)):
            return True

    if name_code_token_in == client.name_native_token:
        if await client.get_balance(name_code_token_in) > (gas_price_wei + amount_token_for_swap_in_wei):
            return True

    return False

def set_slippage_by_input(logger):
    while True:
        try:
            amount_slippage = float(input(f"\nEnter value of slippage for swap in %(format example-\"0.5, 1, 2, 3,...\"): "))
            logger.info(f"gas_estimate: {amount_slippage} %")
            return amount_slippage
        except ValueError:
            print("Amount not number! Please try again!\n")
            logger.warning("input amount slippage not correctly!")


# 0xb
async def main():
    logger = init_logger()

    # ввод пользователем сетей для бриджа
    print_available_chains()
    chain_id_in = await init_chain_by_input(logger, "IN")
    chain_id_out = await init_chain_by_input(logger, "OUT")

    chain_name_client = None
    for k,v in CHAIN_ID_BY_NAME.items():
        if chain_id_in == v:
            chain_name_client = k

    # ввод пользователем приватного ключа
    pk = init_pk_by_input(logger, chain_name_client)
    client = Client(pk, chain_name_client, logger)

    # вывод текущего баланса
    await print_balance(client, "ETH")

    # ввод кол-ва входящих монет
    amount_in_wei = await init_amount_in_token_by_input(client, "ETH", logger)

    # инициализация клиента
    dapp_client = Orbiter(client, logger)

    print("Выполнение транзакции бриджа ... ")
    await  dapp_client.bridge_eth(chain_id_in, chain_id_out, amount_in_wei)
    print("Транзакция бриджа закончена")

if __name__ == "__main__":
    asyncio.run(main())
