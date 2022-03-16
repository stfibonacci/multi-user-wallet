from brownie import (
    MultiUserWallet,
    CompStrategy,
    YearnStrategy,
    AaveStrategy,
    CurveStrategy,
    accounts,
)
from brownie_tokens import MintableForkToken


def deploy_multi_user_wallet():

    dai_address = "0x6b175474e89094c44da98b954eedeac495271d0f"
    cDai_address = "0x5d3a536e4d6dbd6114cc1ead35777bab948e3643"
    comp_address = "0xc00e94cb662c3520282e6f5717214004a7f26888"
    yDai_address = "0xdA816459F1AB5631232FE5e97a05BBBb94970c95"
    lending_pool_addresses_provider = "0xB53C1a33016B2DC2fF3653530bfF1848a515c8c5"
    protocol_data_provider_address = "0x057835Ad21a177dbdd3090bB1CAE03EaCF78Fc6d"
    aDai_address = "0xfC1E690f61EFd961294b3e1Ce3313fBD8aa4f85d"
    aave_address = "0x7Fc66500c84A76Ad7e9c93437bFc5Ac33E2DDaE9"
    # curve_Provider_Address = "0x0000000022D53366457F9d5E68Ec105046FC4383"
    curve_3_pool_Address = "0xbEbc44782C7dB0a1A60Cb6fe97d0b483032FF1C7"
    curve_3crv_Address = "0x6c3F90f043a72FA612cbac8115EE7e52BDe6E490"

    wallet = MultiUserWallet.deploy(
        dai_address,
        {"from": accounts[0]},
    )
    comp_strategy = CompStrategy.deploy(
        wallet,
        dai_address,
        cDai_address,
        comp_address,
        {"from": accounts[0]},
    )

    yearn_strategy = YearnStrategy.deploy(
        wallet,
        dai_address,
        yDai_address,
        {"from": accounts[0]},
    )

    aave_strategy = AaveStrategy.deploy(
        wallet,
        dai_address,
        lending_pool_addresses_provider,
        protocol_data_provider_address,
        aDai_address,
        aave_address,
        {"from": accounts[0]},
    )

    curve_strategy = CurveStrategy.deploy(
        wallet,
        dai_address,
        curve_3_pool_Address,
        curve_3crv_Address,
        {"from": accounts[0]},
    )

    return wallet, comp_strategy, yearn_strategy, aave_strategy, curve_strategy


def mint_test_Dai():
    decimal = 10 ** 18
    a_amount = 100_000 * decimal
    b_amount = 50_000 * decimal

    alice = accounts[0]
    bob = accounts[1]
    dai_address = "0x6b175474e89094c44da98b954eedeac495271d0f"
    dai = MintableForkToken(dai_address)
    dai._mint_for_testing(alice, a_amount)
    dai._mint_for_testing(bob, b_amount)
    return dai, alice, bob, a_amount, b_amount, decimal


def main():
    deploy_multi_user_wallet()
    mint_test_Dai()
