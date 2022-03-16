// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "@openzeppelin/contracts/token/ERC20/ERC20.sol";

import "../interfaces/compound/cToken.sol";

contract CompStrategy is ERC20 {
    address public wallet;
    address public manager;
    address public dai;
    address public cDai;
    address public compToken;

    constructor(
        address _wallet,
        address _dai,
        address _cDai,
        address _compToken
    ) ERC20("walletComp DAI", "wcDAI") {
        wallet = _wallet;
        manager = msg.sender;
        dai = _dai;
        cDai = _cDai;
        compToken = _compToken;
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
            _withdrawSomeCompound(_amount - strategyBalance);
        }
        // transfer dai tokens out of this contract to the msg.sender
        IERC20(dai).transfer(msg.sender, _amount);
    }

    /////////////////// COMPOUND //////////////////

    function _investToCompound(uint256 _amount) external onlyManager {
        IERC20(dai).approve(cDai, _amount);
        cToken(cDai).mint(_amount);
    }

    function _withdrawCompound(uint256 _amount) external onlyManager {
        cToken(cDai).redeem(_amount);
    }

    function _withdrawSomeCompound(uint256 _amount) internal {
        uint256 b = CTokenBalance();
        uint256 bDai = balanceCTokenInDai();
        require(bDai >= _amount, "insufficient funds");
        uint256 amount = (b * _amount) / bDai;
        cToken(cDai).redeem(amount);
    }

    // _amount parameter == dai

    function CTokenBalance() public view returns (uint256) {
        return IERC20(cDai).balanceOf(address(this));
    }

    function balanceCTokenInDai() public view returns (uint256) {
        uint256 b = CTokenBalance();
        if (b > 0) {
            b = (CTokenBalance() * cToken(cDai).exchangeRateStored()) / (1e18);
        }
        return b;
    }

    function compTokenBalance() public view returns (uint256) {
        return IERC20(compToken).balanceOf(address(this));
    }

    // total available dai balance in the strategy contract
    function balance() public view returns (uint256) {
        return IERC20(dai).balanceOf(address(this));
    }

    // Total strategy balance in DAI
    function strategyBalanceInDai() public view returns (uint256) {
        return balance() + balanceCTokenInDai();
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
