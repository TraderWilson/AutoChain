// SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;

import "CarRegister.sol";

contract TitleTransfer {
    struct TransferRequest {
        string vin;
        address payable seller;
        address payable buyer;
        uint256 price;
        uint256 transferTimestamp;
        bool completed;
    }

    mapping(uint256 => TransferRequest) public transferRequests;
    uint256 public totalTransferRequests;

    event TransferInitiated(
        uint256 indexed requestId, 
        string indexed vin, 
        address payable indexed seller, 
        address payable buyer,
        uint256 price,
        uint256 transferTimestamp
    );

    event TransferCompleted(uint256 indexed requestId);

    modifier onlyCarOwner(string memory _vin, address carRegistryAddress) {
        CarRegistry carRegistry = CarRegistry(payable(carRegistryAddress));
        (address owner, , , , ,) = carRegistry.getCar(_vin);
        require(msg.sender == owner, "You are not the owner of this car");
        _;
    }

    function initiateTransfer (
        string memory _vin, 
        address payable _seller, 
        address payable _buyer, 
        uint256 _price, 
        uint256 _transferTimestamp,
        address carRegistryAddress
    ) public onlyCarOwner(_vin, carRegistryAddress) {

        totalTransferRequests++;

        transferRequests[totalTransferRequests] = TransferRequest(
            _vin, 
            _seller, 
            _buyer, 
            _price, 
            _transferTimestamp, 
            false
        );

        CarRegistry carRegistry = CarRegistry(payable(carRegistryAddress));

        carRegistry.updateCarOwner(_vin, _buyer);

        emit TransferInitiated(totalTransferRequests, _vin, _seller, _buyer, _price, _transferTimestamp);
    }


    function getTotalTransferRequests() public view returns (uint256) {
        return totalTransferRequests;
    }

    receive() external payable {
        revert("Direct transfers not allowed");
    }

}
