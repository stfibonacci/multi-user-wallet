from brownie import Wallet, accounts, Contract
from brownie_tokens import MintableForkToken
import pytest


@pytest.fixture(scope="module")
def wallet():
    dai_address = "0x6b175474e89094c44da98b954eedeac495271d0f"
    cDai_address = "0x5d3a536e4d6dbd6114cc1ead35777bab948e3643"
    yDai_address = "0xdA816459F1AB5631232FE5e97a05BBBb94970c95"
    lending_pool_addresses_provider = "0xB53C1a33016B2DC2fF3653530bfF1848a515c8c5"
    aDai_address = "0xfC1E690f61EFd961294b3e1Ce3313fBD8aa4f85d"
    aave_address = "0x7Fc66500c84A76Ad7e9c93437bFc5Ac33E2DDaE9"
    comp_address = "0xc00e94cb662c3520282e6f5717214004a7f26888"
    protocol_data_provider_address = "0x057835Ad21a177dbdd3090bB1CAE03EaCF78Fc6d"
    curve_Provider_Address = "0x0000000022D53366457F9d5E68Ec105046FC4383"
    usdc_Address = "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48"
    wallet = Wallet.deploy(
        dai_address,
        cDai_address,
        yDai_address,
        lending_pool_addresses_provider,
        aDai_address,
        aave_address,
        comp_address,
        protocol_data_provider_address,
        curve_Provider_Address,
        usdc_Address,
        {"from": accounts[0]},
    )
    print(f"Wallet deployed at {wallet}")
    return wallet


@pytest.fixture(scope="module")
def alice():
    return accounts[0]


@pytest.fixture(scope="module")
def bob():
    return accounts[1]


@pytest.fixture(scope="module")
def a_amount():
    return 100_000 * 10 * 18


@pytest.fixture(scope="module")
def b_amount():
    return 50_000 * 10 * 18


def load_contract(addr):
    try:
        cont = Contract(addr)
    except ValueError:
        cont = Contract.from_explorer(addr)
    return cont


@pytest.fixture(scope="module")
def dai():
    dai_address = "0x6b175474e89094c44da98b954eedeac495271d0f"
    dai = MintableForkToken(dai_address)
    return dai


@pytest.fixture(scope="module")
def mint_dai(alice, bob, dai, a_amount, b_amount):

    dai._mint_for_testing(alice, a_amount)
    dai._mint_for_testing(bob, b_amount)
