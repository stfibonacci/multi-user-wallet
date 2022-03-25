from brownie import (
    MultiUserWallet,
    CompStrategy,
    YearnStrategy,
    AaveStrategy,
    CurveStrategy,
    accounts,
    Contract,
)
from brownie_tokens import MintableForkToken
import pytest


@pytest.fixture(scope="module")
def wallet():
    dai_address = "0x6b175474e89094c44da98b954eedeac495271d0f"

    wallet = MultiUserWallet.deploy(
        dai_address,
        {"from": accounts[0]},
    )

    return wallet


@pytest.fixture(scope="module")
def comp_strategy(wallet):
    dai_address = "0x6b175474e89094c44da98b954eedeac495271d0f"
    cDai_address = "0x5d3a536e4d6dbd6114cc1ead35777bab948e3643"
    comp_address = "0xc00e94cb662c3520282e6f5717214004a7f26888"

    comp_strategy = CompStrategy.deploy(
        wallet,
        dai_address,
        cDai_address,
        comp_address,
        {"from": accounts[0]},
    )
    return comp_strategy


@pytest.fixture(scope="module")
def yearn_strategy(wallet):
    dai_address = "0x6b175474e89094c44da98b954eedeac495271d0f"
    yDai_address = "0xdA816459F1AB5631232FE5e97a05BBBb94970c95"

    yearn_strategy = YearnStrategy.deploy(
        wallet,
        dai_address,
        yDai_address,
        {"from": accounts[0]},
    )
    return yearn_strategy


@pytest.fixture(scope="module")
def aave_strategy(wallet):
    dai_address = "0x6b175474e89094c44da98b954eedeac495271d0f"
    lending_pool_addresses_provider = "0xB53C1a33016B2DC2fF3653530bfF1848a515c8c5"
    protocol_data_provider_address = "0x057835Ad21a177dbdd3090bB1CAE03EaCF78Fc6d"
    aDai_address = "0xfC1E690f61EFd961294b3e1Ce3313fBD8aa4f85d"
    aave_address = "0x7Fc66500c84A76Ad7e9c93437bFc5Ac33E2DDaE9"

    aave_strategy = AaveStrategy.deploy(
        wallet,
        dai_address,
        lending_pool_addresses_provider,
        protocol_data_provider_address,
        aDai_address,
        aave_address,
        {"from": accounts[0]},
    )
    return aave_strategy


@pytest.fixture(scope="module")
def curve_strategy(wallet):
    dai_address = "0x6b175474e89094c44da98b954eedeac495271d0f"
    # curve_Provider_Address = "0x0000000022D53366457F9d5E68Ec105046FC4383"
    curve_3_pool_Address = "0xbEbc44782C7dB0a1A60Cb6fe97d0b483032FF1C7"
    curve_3crv_Address = "0x6c3F90f043a72FA612cbac8115EE7e52BDe6E490"

    curve_strategy = CurveStrategy.deploy(
        wallet,
        dai_address,
        curve_3_pool_Address,
        curve_3crv_Address,
        {"from": accounts[0]},
    )

    return curve_strategy


@pytest.fixture(scope="module")
def alice():
    return accounts[0]


@pytest.fixture(scope="module")
def bob():
    return accounts[1]


@pytest.fixture(scope="module")
def decimal():
    return 10 * 18


@pytest.fixture(scope="module")
def a_amount(decimal):
    return 100_000 * decimal


@pytest.fixture(scope="module")
def b_amount(decimal):
    return 50_000 * decimal


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
