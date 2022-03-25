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
    wallet.addStrategy(comp_strategy, {"from": alice})
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
    print(f"{amount / decimal} deposited into comp strategy")
    print(f"wallet dai balance is {wallet.balance()/ decimal} ")
    print(f"wallet wcDAI balance is {comp_strategy.balanceOf(wallet)/ decimal} ")
    print(f"strategy dai balance is {comp_strategy.balance()/ decimal} ")
    print(f"wcDAI total supply is {comp_strategy.totalSupply()/ decimal}")
    comp_strategy_exhange_rate = comp_strategy.getExchangeRate()
    print(f"comp strategy exhange rate is {comp_strategy_exhange_rate / decimal}")

    invest_to_comp_amout = comp_strategy.balance()
    comp_strategy._investToCompound(invest_to_comp_amout, {"from": alice})
    print("after depoisiting into compound")
    print(f"c token balance of strategy is {comp_strategy.CTokenBalance() / decimal}")
    print(f"dai token in compound is {comp_strategy.balanceCTokenInDai() / decimal}")
    print(f"exhange rate is: {comp_strategy.getExchangeRate()/ decimal}")
    print(f"strategy dai balance is {comp_strategy.balance() / decimal}")
    print(
        f"total strategy dai balance is {comp_strategy.strategyBalanceInDai() / decimal}"
    )

    alice_unstake_amount = wallet.balanceOf(alice)
    wallet.unstakeTokens(alice_unstake_amount, {"from": alice})
    print(f"alice balance is {dai.balanceOf(alice)/ decimal}")

    cToken_balance = comp_strategy.CTokenBalance()
    comp_strategy._withdrawCompound(cToken_balance, {"from": alice})
    print("after withdraw from comp")
    print(f"c token balance of strategy is {comp_strategy.CTokenBalance()/ decimal}")
    print(f"dai token in compound is {comp_strategy.balanceCTokenInDai()/ decimal}")
    print(f"exhange rate is {comp_strategy.getExchangeRate()/ decimal}")
    print(f"strategy dai balance is {comp_strategy.balance()/decimal}")
    print(
        f"total strategy dai balance is {comp_strategy.strategyBalanceInDai()/decimal}"
    )

    print("migrating funds from strategy ....")
    amount_with_profit = comp_strategy.walletBalanceInDai(wallet)
    print(f"wallet dai balance is before migration {wallet.balance()/ decimal} ")
    wallet.migrateFromStrategy(0, amount_with_profit, {"from": alice})
    print(f"{amount_with_profit / decimal} withdraw from comp strategy")
    print(f"wallet dai balance is after migration{wallet.balance()/ decimal} ")
    print(f"wallet wcDAI balance is {comp_strategy.balanceOf(wallet)/ decimal} ")
    print(f"strategy dai balance is {comp_strategy.balance()/ decimal} ")
    print(f"wcDAI total supply is {comp_strategy.totalSupply()/decimal}")
    comp_strategy_exhange_rate = comp_strategy.getExchangeRate()
    print(f"comp strategy exhange rate is {comp_strategy_exhange_rate/ decimal}")

    bob_unstake_amount = wallet.balanceOf(bob)
    wallet.unstakeTokens(bob_unstake_amount, {"from": bob})
    print(f"bob balance is {dai.balanceOf(bob)/ decimal}")


def main():
    add_strategy()
