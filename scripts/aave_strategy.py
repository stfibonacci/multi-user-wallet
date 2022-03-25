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
    wallet.addStrategy(aave_strategy, {"from": alice})
    print("strategy added")

    wallet_exhange_rate = wallet.getExchangeRate()
    print(f"wallet exhange rate is {wallet_exhange_rate}")

    wallet.addToWhitelist(alice, {"from": alice})
    wallet.addToWhitelist(bob, {"from": alice})

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
    print(f"{amount / decimal} deposited into aave strategy")
    print(f"wallet dai balance is {wallet.balance()/ decimal} ")
    print(f"wallet waDAI balance is {aave_strategy.balanceOf(wallet)/ decimal} ")
    print(f"strategy dai balance is {aave_strategy.balance()/ decimal} ")
    print(f"waDAI total supply is {aave_strategy.totalSupply()/ decimal}")
    aave_strategy_exhange_rate = aave_strategy.getExchangeRate()
    print(f"aave strategy exhange rate is {aave_strategy_exhange_rate / decimal}")

    invest_to_aave_amout = aave_strategy.balance()
    aave_strategy.investToAave(invest_to_aave_amout, {"from": alice})
    print("after depoisiting into aave")
    print(f"a token balance of strategy is {aave_strategy.aTokenBalance() / decimal}")
    print(f"dai token in aave is {aave_strategy.aTokenBalance() / decimal}")
    print(f"exhange rate is: {aave_strategy.getExchangeRate()/ decimal}")
    print(f"strategy dai balance is {aave_strategy.balance() / decimal}")
    print(
        f"total strategy dai balance is {aave_strategy.strategyBalanceInDai() / decimal}"
    )

    alice_unstake_amount = wallet.balanceOf(alice)
    wallet.unstakeTokens(alice_unstake_amount, {"from": alice})
    # wallet.unstakeTokens(bob_balance, {"from": bob})
    print(f"alice balance is {dai.balanceOf(alice)/ decimal}")
    # print(f"bob balance is {dai.balanceOf(bob)/ decimal}")


def main():
    add_strategy()
