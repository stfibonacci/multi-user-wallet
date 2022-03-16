from brownie import accounts
from scripts.deploy import deploy_multi_user_wallet, mint_test_Dai


def add_strategy():
    (
        wallet,
        comp_strategy,
        yearn_strategy,
        aave_strategy,
        curve_strategy,
    ) = deploy_multi_user_wallet()
    dai, alice, bob, a_amount, b_amount, decimal = mint_test_Dai()
    wallet.addStrategy(curve_strategy, {"from": alice})
    print("strategy added")

    wallet_exhange_rate = wallet.getExchangeRate()
    print(f"wallet exhange rate is {wallet_exhange_rate}")

    dai.approve(wallet, a_amount, {"from": alice})
    print("alice dai approved")
    dai.approve(wallet, b_amount, {"from": bob})
    print("bob dai approved")
    wallet.stakeTokens(a_amount, {"from": alice})
    print("alice deposited to the vault")
    wallet.stakeTokens(b_amount, {"from": bob})
    print("bob deposited to the vault")
    alice_balance = wallet.balanceOf(alice)
    print(f"alice wToken balance is {alice_balance/ decimal}")
    bob_balance = wallet.balanceOf(bob)
    print(f"alice wToken balance is {bob_balance / decimal}")
    print(
        f"exhange rate after alice and bob depist : {wallet.getExchangeRate()/decimal}"
    )
    print(f"wallet dai balance is {wallet.balance()/ decimal} ")

    print("depositing into strategy ....")
    amount = wallet.balance()
    wallet.depositIntoStrategy(0, amount, {"from": alice})
    print(f"{amount / decimal} deposited into curve strategy")
    print(f"wallet dai balance is {wallet.balance()/ decimal} ")
    print(f"wallet wcrvDAI balance is {curve_strategy.balanceOf(wallet)/ decimal} ")
    print(f"strategy dai balance is {curve_strategy.balance()/ decimal} ")
    print(f"wcrvDAI total supply is {curve_strategy.totalSupply()/ decimal}")
    curve_strategy_exhange_rate = curve_strategy.getExchangeRate()
    print(f"curve strategy exhange rate is {curve_strategy_exhange_rate / decimal}")

    invest_to_curve_amout = curve_strategy.balance()
    curve_strategy.investToCurve3Pool(invest_to_curve_amout, {"from": alice})
    print("after depoisiting into curve 3 pool")
    print(
        f"3crv lp token balance of strategy is {curve_strategy.lpTokenBalance() / decimal}"
    )
    print(f"dai token in curve is {curve_strategy.balanceLpTokenInDai() / decimal}")
    print(f"strategy exhange rate is: {curve_strategy.getExchangeRate()/ decimal}")
    print(f"wallet exhange rate is: {wallet.getExchangeRate()/ decimal}")
    print(f"strategy dai balance is {curve_strategy.balance() / decimal}")
    print(
        f"total strategy dai balance is {curve_strategy.strategyBalanceInDai() / decimal}"
    )

    alice_unstake_amount = wallet.balanceOf(alice)
    wallet.unstakeTokens(alice_unstake_amount, {"from": alice})
    print(f"alice balance is {dai.balanceOf(alice)/ decimal}")

    c3rvToken_balance = curve_strategy.lpTokenBalance()
    curve_strategy.withdrawFromCurve3Pool(c3rvToken_balance, {"from": alice})
    print("after withdraw from curve 3pool")
    print(
        f"3rv lp token balance of strategy is {curve_strategy.lpTokenBalance()/ decimal}"
    )
    print(
        f"dai token in curve 3pool is {curve_strategy.balanceLpTokenInDai()/ decimal}"
    )
    print(f"exhange rate is {curve_strategy.getExchangeRate()/ decimal}")
    print(f"strategy dai balance is {curve_strategy.balance()/decimal}")
    print(
        f"total strategy dai balance is {curve_strategy.strategyBalanceInDai()/decimal}"
    )

    print("migrating funds from strategy ....")
    amount_with_profit = curve_strategy.walletBalanceInDai(wallet)
    print(f"wallet dai balance is before migration {wallet.balance()/ decimal} ")
    wallet.migrateFromStrategy(0, amount_with_profit, {"from": alice})
    print(f"{amount_with_profit / decimal} withdraw from curve strategy")
    print(f"wallet dai balance is after migration{wallet.balance()/ decimal} ")
    print(f"wallet wcrvDAI balance is {curve_strategy.balanceOf(wallet)/ decimal} ")
    print(f"strategy dai balance is {curve_strategy.balance()/ decimal} ")
    print(f"wcrvDAI total supply is {curve_strategy.totalSupply()/decimal}")
    curve_strategy_exhange_rate = curve_strategy.getExchangeRate()
    print(f"curve strategy exhange rate is {curve_strategy_exhange_rate/ decimal}")

    wallet.unstakeTokens(bob_balance, {"from": bob})
    print(f"bob balance is {dai.balanceOf(bob)/ decimal}")


def main():
    add_strategy()
