// SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;

interface IStrategy {
    function mint(uint256) external;

    function redeemDai(uint256) external;

    function balanceOf() external view returns (uint256);

    function walletBalanceInDai(address) external view returns (uint256);

    function strategyBalanceInDai() external view returns (uint256);
}
