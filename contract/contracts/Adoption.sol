pragma solidity ^0.5.0;

contract Adoption {
  address[100] public adopters;

  // Adopting a student
  function adopt(uint studentId) public returns (uint) {
    require(studentId >= 0 && studentId <= 99);

    adopters[studentId] = msg.sender;

    return studentId;
  }

  // Retrieving the adopters
  function getAdopters() public view returns (address[100] memory) {
    return adopters;
  }

}
