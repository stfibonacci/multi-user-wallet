// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "@openzeppelin/contracts/token/ERC20/ERC20.sol";

import "../interfaces/yearn/YVault.sol";

contract YearnStrategy is ERC20 {
    address public wallet;
    address public manager;
    address public dai;
    address public yDai;

    constructor(
        address _wallet,
        address _dai,
        address _yDai
    ) ERC20("walletYearn DAI", "wyDAI") {
        wallet = _wallet;
        manager = msg.sender;
        dai = _dai;
        yDai = _yDai;
    }

    modifier onlyManager() {
        require(manager == msg.sender, "Only Manager");
        _;
    }
    modifier onlyWallet() {
        require(wallet == msg.sender, "Only Manager");
        _;
    }

    function mint(uint256 _amount) external onlyWallet {
        require(_amount > 0, "deposit must be greater than 0");
        uint256 _shares = (_amount * (1e18)) / getExchangeRate();
        _mint(msg.sender, _shares);

        IERC20(dai).transferFrom(msg.sender, address(this), _amount);
    }

    function redeemDai(uint256 _amount) external onlyWallet {
        uint256 _shares = (_amount * (1e18)) / getExchangeRate();
        _burn(msg.sender, _shares);

        // check contract balance
        uint256 strategyBalance = IERC20(dai).balanceOf(address(this));

        if (strategyBalance < _amount) {
            _withdrawSomeYearn(_amount - strategyBalance);
        }
        // transfer dai tokens out of this contract to the msg.sender
        IERC20(dai).transfer(msg.sender, _amount);
    }

    /////////////////// COMPOUND //////////////////

    function investToYearn(uint256 _amount) external onlyManager {
        IERC20(dai).approve(yDai, _amount);
        YVault(yDai).deposit(_amount);
    }

    function withdrawFromYearn(uint256 _amount) external onlyManager {
        YVault(yDai).withdraw(_amount);
    }

    function _withdrawSomeYearn(uint256 _amount) internal {
        uint256 b = YTokenBalance();
        uint256 bDai = balanceYTokenInDai();
        require(bDai >= _amount, "insufficient funds");
        uint256 amount = (b * _amount) / bDai;
        YVault(yDai).withdraw(amount);
    }

    // _amount parameter == dai

    function YTokenBalance() public view returns (uint256) {
        return IERC20(yDai).balanceOf(address(this));
    }

    function balanceYTokenInDai() public view returns (uint256) {
        uint256 price = YVault(yDai).pricePerShare();
        uint256 shares = IERC20(yDai).balanceOf(address(this));
        return (shares * price) / (1e18);
    }

    // total available dai balance in the strategy contract
    function balance() public view returns (uint256) {
        return IERC20(dai).balanceOf(address(this));
    }

    // Total strategy balance in DAI
    function strategyBalanceInDai() public view returns (uint256) {
        return balance() + balanceYTokenInDai();
    }

    // wallet dai balance in strategy contract
    function walletBalanceInDai(address _wallet) public view returns (uint256) {
        return (balanceOf(_wallet) * getExchangeRate()) / (1e18);
    }

    function getExchangeRate() public view returns (uint256) {
        if (totalSupply() == 0) return (1e18);
        return (strategyBalanceInDai() * (1e18)) / totalSupply();
    }
}
