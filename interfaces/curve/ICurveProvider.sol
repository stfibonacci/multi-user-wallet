// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

interface ICurveProvider {
    function get_registry() external view returns (address);
}
