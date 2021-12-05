pragma solidity ^0.5.0;

import "truffle/Assert.sol";
import "truffle/DeployedAddresses.sol";
import "../contracts/Adoption.sol";

contract TestAdoption {
  // The address of the adoption contract to be tested
  Adoption adoption = Adoption(DeployedAddresses.Adoption());

  // The id of the student that will be used for testing
  uint expectedStudentId = 8;

  // The expected adopter of adopted student is this contract
  address expectedAdopter = address(this);

  // Testing the adopt() function
  function testUserCanAdoptStudent() public {
    uint returnedId = adoption.adopt(expectedStudentId);

    Assert.equal(returnedId, expectedStudentId, "Adoption of the expected student should match what is returned.");
  }

  // Testing retrieval of a single student's adopter
  function testGetAdopterAddressByStudentId() public {
    address adopter = adoption.adopters(expectedStudentId);

    Assert.equal(adopter, expectedAdopter, "Volunteer of the expected student should be this contract");
  }

  // Testing retrieval of all student adopters
  function testGetAdopterAddressByStudentIdInArray() public {
    // Store adopters in memory rather than contract's storage
    address[100] memory adopters = adoption.getAdopters();

    Assert.equal(adopters[expectedStudentId], expectedAdopter, "Volunteer of the expected student should be this contract");
  }

}
