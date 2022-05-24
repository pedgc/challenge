// Artifacts are information about our contract such as its deployed address and
//   Application Binary Interface (ABI). The ABI is a JavaScript object defining
//   how to interact with the contract including its variables, functions and
//   their parameters.
var TextImage = artifacts.require("TextImage");
var DogsOrCats = artifacts.require("DogsOrCats");

module.exports = function(deployer) {
  deployer.deploy(TextImage);
  deployer.deploy(DogsOrCats);
};
