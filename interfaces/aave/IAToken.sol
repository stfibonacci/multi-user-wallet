// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

interface IAToken {
    function balanceOf(address _user) external view returns (uint256);

    function redeem(uint256 _amount) external;
}
