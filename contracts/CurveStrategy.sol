// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "@openzeppelin/contracts/token/ERC20/ERC20.sol";

import "../interfaces/curve/ICurveProvider.sol";
import "../interfaces/curve/ICurveRegistry.sol";
import "../interfaces/curve/I3Pool.sol";

contract CurveStrategy is ERC20 {
    address public wallet;
    address public manager;
    address public dai;
    //curve
    address public curve3pool;
    //LP 3pool Curve (3CRV)
    address public curve3crv;

    constructor(
        address _wallet,
        address _dai,
        address _curve3pool,
        address _curve3crv
    ) ERC20("walletCurve DAI", "wcrvDAI") {
        wallet = _wallet;
        manager = msg.sender;
        dai = _dai;
        curve3pool = _curve3pool;
        curve3crv = _curve3crv;
    }

    modifier onlyManager() {
        require(msg.sender == manager, "Only Manager");
        _;
    }
    modifier onlyWallet() {
        require(msg.sender == wallet, "Only Manager");
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
            _withdrawSomeCurve3Pool(_amount - strategyBalance);
        }

        IERC20(dai).transfer(msg.sender, _amount);
    }

    /////////////////// COMPOUND //////////////////

    function investToCurve3Pool(uint256 _amount) external onlyManager {
        IERC20(dai).approve(curve3pool, _amount);
        I3Pool(curve3pool).add_liquidity([_amount, 0, 0], 0);
    }

    function withdrawFromCurve3Pool(uint256 _amount) external onlyManager {
        I3Pool(curve3pool).remove_liquidity_one_coin(_amount, 0, 0);
    }

    function _withdrawSomeCurve3Pool(uint256 _amount) internal {
        uint256 b = lpTokenBalance();
        uint256 bDai = balanceLpTokenInDai();
        require(bDai >= _amount, "insufficient funds");

        uint256 amount = (b * _amount) / bDai; //(b.mul(_amount)).div(bT).add(1);

        I3Pool(curve3pool).remove_liquidity_one_coin(amount, 0, 0);
    }

    // _amount parameter == dai

    function lpTokenBalance() public view returns (uint256) {
        return IERC20(curve3crv).balanceOf(address(this));
    }

    function balanceLpTokenInDai() public view returns (uint256) {
        uint256 virtual_price = I3Pool(curve3pool).get_virtual_price();
        uint256 shares = lpTokenBalance();
        //slippage 9999/10000
        return (shares * virtual_price * 9999) / (1e18 * 10000);
    }

    // total available dai balance in the strategy contract
    function balance() public view returns (uint256) {
        return IERC20(dai).balanceOf(address(this));
    }

    // Total strategy balance in DAI
    function strategyBalanceInDai() public view returns (uint256) {
        return balance() + balanceLpTokenInDai();
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
