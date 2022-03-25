// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "../interfaces/wallet/IStrategy.sol";

contract MultiUserWallet is Ownable, ERC20 {
    //only whitelisted addresses can deposit to this wallet
    mapping(address => bool) public whitelistedAddresses;
    uint8 public numOfWhitelistedAddress;

    address public dai;
    // 0-comp 1-yearn 2-aave 3-curve
    IStrategy[] public strategies;

    constructor(address _dai) ERC20("wallet DAI", "wDAI") {
        dai = _dai;
    }

    function addToWhitelist(address _address) external onlyOwner {
        require(!whitelistedAddresses[_address], "user already whitelisted");
        whitelistedAddresses[_address] = true;
        numOfWhitelistedAddress += 1;
    }

    function removeFromWhitelist(address _address) external onlyOwner {
        require(whitelistedAddresses[_address], "user not whitelisted");
        whitelistedAddresses[_address] = false;
        numOfWhitelistedAddress -= 1;
    }

    function stakeTokens(uint256 _amount) external {
        require(_amount > 0, "deposit must be greater than 0");
        //require(whitelistedAddresses[msg.sender], "user already whitelisted");

        uint256 _shares = (_amount * (1e18)) / getExchangeRate();
        _mint(msg.sender, _shares);

        IERC20(dai).transferFrom(msg.sender, address(this), _amount);
    }

    function unstakeTokens(uint256 _shares) external {
        require(_shares > 0, "withdraw must be greater than 0");
        //require(_shares <= balanceOf(msg.sender), "insufficient balance");

        uint256 userBalance = (_shares * getExchangeRate()) / (1e18);

        _burn(msg.sender, _shares);

        // Check contract balance
        uint256 walletBalance = IERC20(dai).balanceOf(address(this));

        if (walletBalance < userBalance) {
            _withdrawFromStrategy(userBalance - walletBalance);
        }
        // transfer dai tokens out of this contract to the msg.sender
        IERC20(dai).transfer(msg.sender, userBalance);
    }

    function depositIntoStrategy(uint256 _strategyIndex, uint256 _amount)
        external
    {
        IStrategy strategy = strategies[_strategyIndex];
        require(
            address(strategy) != address(0),
            "strategy cannot be zero address"
        );

        IERC20(dai).approve(address(strategy), _amount);
        strategy.mint(_amount);
    }

    function migrateFromStrategy(uint256 _strategyIndex, uint256 _amount)
        external
    {
        IStrategy strategy = strategies[_strategyIndex];

        strategy.redeemDai(_amount);
    }

    //////////// withdraw logic from strategies if there is not enougH fund in the wallet //////////////
    function _withdrawFromStrategy(uint256 _amount) internal {
        uint256 missingAmount = _amount;
        uint256 strategyBalance;

        for (uint256 i = 0; i < strategies.length; i++) {
            IStrategy strategy = strategies[i];

            strategyBalance = strategy.strategyBalanceInDai();

            if (strategyBalance > 0) {
                if (_amount > strategyBalance) {
                    strategy.redeemDai(strategyBalance);
                    _amount = missingAmount - strategyBalance;
                } else {
                    strategy.redeemDai(_amount);
                }
            }

            // If we've pulled all we need, exit the loop.
            if (missingAmount == 0) break;
        }
    }

    function addStrategy(address _newaddress) external returns (IStrategy) {
        IStrategy strategy = IStrategy(_newaddress);
        strategies.push(strategy);
        return strategy;
    }

    function getStrategy(uint256 _strategyIndex)
        public
        view
        returns (IStrategy)
    {
        IStrategy strategy = strategies[_strategyIndex];
        return strategy;
    }

    function getStrategies() external view returns (IStrategy[] memory) {
        return strategies;
    }

    /////////////////   BALANCES   /////////////////

    // total available dai balance in the wallet
    function balance() public view returns (uint256) {
        return IERC20(dai).balanceOf(address(this));
    }

    // user balance in dai
    function userBalanceInDai() public view returns (uint256) {
        return ((balanceOf(msg.sender) * getExchangeRate()) / (1e18));
    }

    // Total wallet balance in DAI
    function walletBalanceInDai() public view returns (uint256) {
        uint256 strategyTotal;
        for (uint256 i = 0; i < strategies.length; i++) {
            IStrategy strategy = strategies[i];
            strategyTotal = strategyTotal + strategy.strategyBalanceInDai();
        }

        return strategyTotal + balance();
    }

    function getExchangeRate() public view returns (uint256) {
        if (totalSupply() == 0) return (1e18);
        return (walletBalanceInDai() * (1e18)) / totalSupply();
    }

    ///////////////////////////
}
