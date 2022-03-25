from brownie import accounts
import pytest


def test_exchange_rate(wallet):
    decimal = 1e18
    exchange_rate = wallet.getExchangeRate() / decimal
    assert exchange_rate == 1


def test_total_supply(wallet):
    assert wallet.totalSupply() == 0


def test_add_to_whitelist(wallet, alice, bob):
    wallet.addToWhitelist(alice, {"from": alice})
    wallet.addToWhitelist(bob, {"from": alice})
    wallet.addToWhitelist(accounts[2], {"from": alice})
    assert wallet.numOfWhitelistedAddress() == 3


def test_remove_from_whitelist(wallet, alice):
    wallet.removeFromWhitelist(accounts[2], {"from": alice})
    assert wallet.numOfWhitelistedAddress() == 2


def test_not_whitelisted(wallet):
    assert wallet.whitelistedAddresses(accounts[3]) == False


def test_Stake(wallet, alice, bob, dai, a_amount, b_amount, mint_dai):
    dai.approve(wallet, a_amount, {"from": alice})
    wallet.stakeTokens(a_amount, {"from": alice})
    dai.approve(wallet, b_amount, {"from": bob})
    wallet.stakeTokens(b_amount, {"from": bob})
    assert wallet.balance() == a_amount + b_amount


def test_add_comp(wallet, comp_strategy, alice):
    wallet.addStrategy(comp_strategy, {"from": alice})
    assert wallet.getStrategy(0) == comp_strategy


def test_add_yearn(wallet, yearn_strategy, alice):
    wallet.addStrategy(yearn_strategy, {"from": alice})
    assert wallet.getStrategy(1) == yearn_strategy


def test_add_aave(wallet, aave_strategy, alice):
    wallet.addStrategy(aave_strategy, {"from": alice})
    assert wallet.getStrategy(2) == aave_strategy


def test_add_curve(wallet, curve_strategy, alice):
    wallet.addStrategy(curve_strategy, {"from": alice})
    assert wallet.getStrategy(3) == curve_strategy


@pytest.mark.skip(reason="no way of currently testing this")
def test_deposit_comp_strat(wallet, comp_strategy, alice, decimal):
    amount = 30_000 * decimal
    wallet.depositIntoStrategy(0, amount, {"from": alice})
    assert comp_strategy.balance() == amount


def test_deposit_yearn_strat(wallet, yearn_strategy, alice, decimal):
    amount = 30_000 * decimal
    wallet.depositIntoStrategy(1, amount, {"from": alice})
    assert yearn_strategy.balance() == amount


def test_deposit_aave_strat(wallet, aave_strategy, alice, decimal):
    amount = 30_000 * decimal
    wallet.depositIntoStrategy(2, amount, {"from": alice})
    assert aave_strategy.balance() == amount


def test_deposit_curve_strat(wallet, curve_strategy, alice, decimal):
    amount = 30_000 * decimal
    wallet.depositIntoStrategy(3, amount, {"from": alice})
    assert curve_strategy.balance() == amount


@pytest.mark.skip(reason="no way of currently testing this")
def test_invest_to_comp(comp_strategy, alice):
    amount = comp_strategy.balance()
    comp_strategy._investToCompound(amount, {"from": alice})
    assert comp_strategy.CTokenBalance() > 0


def test_invest_to_yearn(yearn_strategy, alice):
    amount = yearn_strategy.balance()
    yearn_strategy.investToYearn(amount, {"from": alice})
    assert yearn_strategy.YTokenBalance() > 0


def test_invest_to_aave(aave_strategy, alice):
    amount = aave_strategy.balance()
    aave_strategy.investToAave(amount, {"from": alice})
    assert aave_strategy.aTokenBalance() > 0


def test_invest_to_curve(curve_strategy, alice):
    amount = curve_strategy.balance()
    curve_strategy.investToCurve3Pool(amount, {"from": alice})
    assert curve_strategy.lpTokenBalance() > 0


def test_alice_unstake(wallet, alice):
    alice_wDai_balance = wallet.balanceOf(alice)
    wallet.unstakeTokens(alice_wDai_balance, {"from": alice})
    assert wallet.balanceOf(alice) == 0


def test_bob_unstake(wallet, bob):
    bob_wDai_balance = wallet.balanceOf(bob)
    wallet.unstakeTokens(bob_wDai_balance, {"from": bob})
    assert wallet.balanceOf(bob) == 0
