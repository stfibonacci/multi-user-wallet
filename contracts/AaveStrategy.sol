// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "@openzeppelin/contracts/token/ERC20/ERC20.sol";

import "../interfaces/aave/ILendingPoolAddressesProvider.sol";
import "../interfaces/aave/IProtocolDataProvider.sol";
import "../interfaces/aave/ILendingPool.sol";
import "../interfaces/aave/IAToken.sol";

contract AaveStrategy is ERC20 {
    address public wallet;
    address public manager;
    address public dai;
    address public lendingPoolAddressesProvider;
    address public aaveLendingPool;
    address public aDai;
    address public aave;
    address public protocolDataProvider;

    constructor(
        address _wallet,
        address _dai,
        address _lendingPoolAddressesProviderAddress,
        address _protocolDataProvider,
        address _aDaiAddress,
        address _aave
    ) ERC20("walletAave DAI", "waDAI") {
        wallet = _wallet;
        manager = msg.sender;
        dai = _dai;
        lendingPoolAddressesProvider = _lendingPoolAddressesProviderAddress;
        protocolDataProvider = _protocolDataProvider;
        aDai = _aDaiAddress;
        aave = _aave;
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
            _withdrawSomeAave(_amount - strategyBalance);
        }
        // transfer dai tokens out of this contract to the msg.sender
        IERC20(dai).transfer(msg.sender, _amount);
    }

    /////////////////// AAVE //////////////////

    function getLendingPoolAddress() public view returns (address) {
        return
            ILendingPoolAddressesProvider(lendingPoolAddressesProvider)
                .getLendingPool();
    }

    function investToAave(uint256 _amount) external onlyManager {
        IERC20(dai).approve(getLendingPoolAddress(), type(uint256).max);
        ILendingPool(getLendingPoolAddress()).deposit(
            dai,
            _amount,
            address(this),
            0
        );
    }

    function _withdrawFromAave(uint256 _amount) external onlyManager {
        //AToken(aDai).redeem(_amount);
        ILendingPool(getLendingPoolAddress()).withdraw(
            dai,
            _amount,
            address(this)
        );
    }

    function _withdrawSomeAave(uint256 _amount) internal {
        //AToken(aDai).redeem(_amount);
        ILendingPool(getLendingPoolAddress()).withdraw(
            dai,
            _amount,
            address(this)
        );
    }

    function _withdrawFromAaveAll() public {
        //AToken(aDai).redeem(_amount);
        ILendingPool(getLendingPoolAddress()).withdraw(
            dai,
            type(uint256).max,
            address(this)
        );
    }

    function getATokenAddress() public view returns (address) {
        (address _aToken, , ) = IProtocolDataProvider(protocolDataProvider)
            .getReserveTokensAddresses(dai);

        return _aToken;
    }

    // _amount parameter == dai
    //balanceATokenInDai == aTokenBalance

    function aTokenBalance() public view returns (uint256) {
        return IAToken(getATokenAddress()).balanceOf(address(this));
    }

    function aaveTokenBalance() public view returns (uint256) {
        return IERC20(aave).balanceOf(address(this));
    }

    // total available dai balance in the strategy contract
    function balance() public view returns (uint256) {
        return IERC20(dai).balanceOf(address(this));
    }

    // Total strategy balance in DAI
    function strategyBalanceInDai() public view returns (uint256) {
        return balance() + aTokenBalance();
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
