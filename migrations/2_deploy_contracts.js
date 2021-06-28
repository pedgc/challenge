// Artifacts are information about our contract such as its deployed address and
//   Application Binary Interface (ABI). The ABI is a JavaScript object defining
//   how to interact with the contract including its variables, functions and
//   their parameters.
var Challenge = artifacts.require("Challenge");
var LevDistance = artifacts.require("LevDistance");
var DogsOrCats = artifacts.require("DogsOrCats");

module.exports = function(deployer) {
  // deployer.deploy(Challenge);
  deployer.deploy(LevDistance);
  deployer.deploy(DogsOrCats);
};
