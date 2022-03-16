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
    wallet.addStrategy(yearn_strategy, {"from": alice})
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
    print(f"{amount / decimal} deposited into yearn strategy")
    print(f"wallet dai balance is {wallet.balance()/ decimal} ")
    print(f"wallet wyDAI balance is {yearn_strategy.balanceOf(wallet)/ decimal} ")
    print(f"strategy dai balance is {yearn_strategy.balance()/ decimal} ")
    print(f"wyDAI total supply is {yearn_strategy.totalSupply()/ decimal}")
    yearn_strategy_exhange_rate = yearn_strategy.getExchangeRate()
    print(f"yearn strategy exhange rate is {yearn_strategy_exhange_rate / decimal}")

    invest_to_yearn_amout = yearn_strategy.balance()
    yearn_strategy.investToYearn(invest_to_yearn_amout, {"from": alice})
    print("after depoisiting into yearn")
    print(f"y token balance of strategy is {yearn_strategy.YTokenBalance() / decimal}")
    print(f"dai token in yearn is {yearn_strategy.balanceYTokenInDai() / decimal}")
    print(f"exhange rate is: {yearn_strategy.getExchangeRate()/ decimal}")
    print(f"strategy dai balance is {yearn_strategy.balance() / decimal}")
    print(
        f"total strategy dai balance is {yearn_strategy.strategyBalanceInDai() / decimal}"
    )

    alice_unstake_amount = wallet.balanceOf(alice)
    wallet.unstakeTokens(alice_unstake_amount, {"from": alice})
    # wallet.unstakeTokens(bob_balance, {"from": bob})
    print(f"alice balance is {dai.balanceOf(alice)/ decimal}")
    # print(f"bob balance is {dai.balanceOf(bob)/ decimal}")


def main():
    add_strategy()
