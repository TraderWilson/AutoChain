// SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;

contract CarRegistry {
    struct Car {
        address payable owner;
        string make;
        string model;
        uint16 year;
        string plate_number;
        string vin;
        string imageHash; // Added field for image IPFS hash
    }

    struct OwnershipHistory {
        address owner;
        uint256 timestamp;
    }

    mapping(string => Car) public cars;
    mapping(string => bool) public registeredPlateNumbers;
    mapping(string => OwnershipHistory[]) public carOwnershipHistory;
    uint256 public totalCars;

    event CarRegistered(
        string indexed vin,
        address indexed owner, 
        string make, 
        string model, 
        uint16 year, 
        string plate_number,
        string imageHash // Added imageHash to the event
    );

    event UpdateCarOwner(
        string indexed vin,
        address indexed old_owner,
        address indexed new_owner
    );

    function registerCar(string memory _vin, string memory _make, string memory _model, uint16 _year, string memory _plate_number, string memory _imageHash) public {
        require(cars[_vin].owner == address(0), "The car with this VIN already registered");
        totalCars++;
        cars[_vin] = Car(payable(msg.sender), _make, _model, _year, _plate_number, _vin, _imageHash);
        registeredPlateNumbers[_plate_number] = true;

        // Add initial ownership record
        carOwnershipHistory[_vin].push(OwnershipHistory({
            owner: msg.sender,
            timestamp: block.timestamp
        }));

        emit CarRegistered(_vin, msg.sender, _make, _model, _year, _plate_number, _imageHash);
    }

    function getCar(string memory _vin) public view returns (address payable owner, string memory make, string memory model, uint16 year, string memory plate_number, string memory imageHash) {
        Car storage car = cars[_vin];
        return (car.owner, car.make, car.model, car.year, car.plate_number, car.imageHash);
    }

    function updateCarOwner(string memory _vin, address payable _newOwner) public {
        require(cars[_vin].owner != address(0), "Car with this VIN does not exist");
        address oldOwner = cars[_vin].owner;
        cars[_vin].owner = _newOwner;

        // Record the ownership change
        carOwnershipHistory[_vin].push(OwnershipHistory({
            owner: _newOwner,
            timestamp: block.timestamp
        }));

        emit UpdateCarOwner(_vin, oldOwner, _newOwner);
    }

    function getCarOwnershipHistory(string memory _vin) public view returns (OwnershipHistory[] memory) {
        return carOwnershipHistory[_vin];
    }

    receive() external payable {
        revert("Direct transfers not allowed");
    }

}
