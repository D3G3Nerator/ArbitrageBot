from secondary import one_split_abi, one_split_address, tokens
from itertools import permutations
from termcolor import colored
from web3 import Web3
import requests, concurrent.futures

infura_url = "https://mainnet.infura.io/v3/f36750d69d314e3695b7fe230bb781af"
w3 = Web3(Web3.HTTPProvider(infura_url))
one_split_audit = w3.eth.contract(address=one_split_address, abi=one_split_abi)
url = "https://api.0x.org/sra/v4/orders"
gas_station_url = "https://ethgasstation.info/api/ethgasAPI.json"
gas_station_api_key = "ec0e871cf2a6134fc3a1f16eac14ba538d5975eaaf3cba6583ab3e3bb161"
gas_limit = 3000000
estimated_gas = 1700000

def to_eth(_wei, _token):
    return _wei / (10 ** tokens[_token]["decimals"])

def to_eth_str(_wei, _token):
    return f"{to_eth(_wei, _token)} {_token}"

def log_arb(taker_amount, taker_token, maker_amount, maker_token, expected_return, return_price, price, estimated_fee, profit):
    return f"""ARBITRAGE FOUND! INSTRUCTIONS:
1. Borrow {to_eth_str(taker_amount, taker_token)}
2. Buy {to_eth_str(maker_amount, maker_token)} FOR {to_eth_str(taker_amount, taker_token)} ({maker_token} Price: {price} {taker_token})
3. Sell {to_eth_str(maker_amount, maker_token)} FOR {to_eth_str(expected_return, taker_token)} ({maker_token} Price: {return_price} {taker_token})
Fees: {estimated_fee}
Profit: {to_eth_str(profit, taker_token)}
"""

def test_arbitrage(maker_token, taker_token, estimated_fee, order):
    # Skip Orders With Fees
    if order["takerTokenFeeAmount"] != "0" or order["feeRecipient"] != "0x0000000000000000000000000000000000000000":
        return

    # First Trade:
    maker_amount = int(order['makerAmount'])
    taker_amount = int(order['takerAmount'])
    price = to_eth(taker_amount, taker_token) / to_eth(maker_amount, maker_token) # price of bought token

    # Second Trade:
    expected_return = one_split_audit.functions.getExpectedReturn(
        tokens[maker_token]["address"], # from_token
        tokens[taker_token]["address"], # to_token
        maker_amount, # amount
        10, # parts
        0 # feature_flags
    ).call()[0]
    return_price = to_eth(expected_return, taker_token) / to_eth(maker_amount, maker_token) # price of sold token

    profit = expected_return - taker_amount - estimated_fee

    # Log Instructions if Profitable:
    if profit > 0:
        print(colored(log_arb(taker_amount, taker_token, maker_amount, maker_token, expected_return, return_price, price, estimated_fee, profit), "green"))

def test_pair(maker_token, taker_token, estimated_fee):
    parameters = {
        "makerToken": tokens[maker_token]["address"], # token I want
        "takerToken": tokens[taker_token]["address"], # token I have
        "page": 1,
        "perPage": 1000
    }
    request = requests.get(url, params=parameters).json()

    if not request["records"]:
        return

    orders = [order["order"] for order in request["records"]]
    with concurrent.futures.ThreadPoolExecutor() as executor2:
        threads2 = [executor2.submit(test_arbitrage, maker_token, taker_token, estimated_fee, order) for order in orders]


def execute():
    gas_price = requests.get(gas_station_url, params= {"api-key": gas_station_api_key}).json()["fastest"]
    print(f"Gas Price (fastest): {gas_price}")
    estimated_fee = estimated_gas * gas_price
    with concurrent.futures.ThreadPoolExecutor() as executor:
        threads = [executor.submit(test_pair, maker_token, taker_token, estimated_fee) for (maker_token, taker_token) in permutations(tokens, 2)]

    print("All Done!")

execute()