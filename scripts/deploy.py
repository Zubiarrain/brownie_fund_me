from brownie import FundMe, MockV3Aggregator, network, config
from scripts.helpful_scripts import *


def deploy_fund_me():
    account = get_account()
    # pass the price feed address to our fudme contract

    # I can say if we're not on a develpment network (like ganache) we call the usd/eth price from a var from the config file where we can have eth/usd prices for different networks (rinkeby, kovan, etc)
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIROMENTS:
        price_feed_address = config["networks"][network.show_active()][
            "eth_usd_price_feed"
        ]
    # If we're on a develpment network we deploy a mock (from helpful_scripts) and we set the price_feed as the value we set on de last mock we deployed
    else:
        deploy_mocks()
        price_feed_address = MockV3Aggregator[-1].address
        # If I want to save the deployment information I have to add ganache to the networks using the code: brownie networks add Ethereum ganche-local host=http://127.0.0.1:7545 chainid=1337

    # publish_source=True allows me to publish my contract and interact with it with etherscan. But, if we're on a development network we don't need this, so we call a verify var from de config file
    # I need to have the ETHERSCAN_TOKEN in my .env
    fund_me = FundMe.deploy(
        price_feed_address,
        {"from": account},
        publish_source=config["networks"][network.show_active()].get("verify"),
    )
    print(f"Contract deployed to {fund_me.address}")
    return fund_me


def main():
    deploy_fund_me()
