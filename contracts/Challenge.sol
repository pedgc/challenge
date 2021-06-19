pragma solidity ^0.5.0;

/* = = = = = = = INTERFACES = = = = = = = = = = */
contract LevDistanceInterface{
  function levDistance(string memory _str1, string memory _str2) public payable returns(uint);
}

contract Challenge {

  /* = = = = = = TO DO = = = = = = = */
  /*
    * Learn how to optimize gas costs
    * See how to "froze" the money while betting
    * Calculate the levenshtein distance
      - Make it work for any string length
    * Transform this into a modular architecture
    * GUI
  */

  /* = = = = = = = VARIABLES & CONSTRUCTOR = = = = = = =*/
  //State variables -> Permanently saved in the contract
  address payable public admin;
  mapping(string => address) public contracts;
  mapping(address => User) public users;

  struct User {
        uint balance;        // Current amount of ETH of the user in our platform
        address userAddress; // Address of the user
  }

  constructor () public{
    admin = msg.sender;
  }

  modifier onlyAdmin {
    require(msg.sender == admin, "Only admin can call this function");
        _;
  }

/* = = = = = = = FUNCTIONS = = = = = = = */
// - - - - Getters - - - -
function getUser(address _userAddress) public view returns(uint, address){
  return (users[_userAddress].balance, users[_userAddress].userAddress);
}

function getBalance(address _userAddress) public view returns(uint){
  return (users[_userAddress].balance);
}

function getBalanceContract() public view onlyAdmin returns(uint){
  return address(this).balance;
}

// - - - - - - - - - -

// - - - - Future Modifications - - - -
function setAdmin(address payable _newAdmin) public onlyAdmin {
  admin = _newAdmin;
}
// - - - - - - - - - -

// - - - - Events - - - -
event Winner(string _winner);

// - - - - Core - - - -
  function checkUser(address _userAddress, uint _amount) private view{
    require(users[_userAddress].userAddress != address(0), "The user does not exists");
    require(users[_userAddress].balance >= _amount, "The user does not have the requested amount");
  }

  // Deposit and Withdraw for Admin
  function depositAdmin() public payable onlyAdmin{}

  function withdrawAdmin(uint _amount) public payable onlyAdmin{
    require(address(this).balance >= _amount, "The requested amount is not available");
    admin.transfer(_amount);
  }

  //Deposit and Withdraw for Users
  function deposit() public payable{
    // Create user if it does not exists
    if (users[msg.sender].userAddress == address(0)){
      users[msg.sender] = User(0, msg.sender);
    }

    users[msg.sender].balance += msg.value;
  }

  function withdraw(uint _amount) public {
    checkUser(msg.sender, _amount);

    msg.sender.transfer(_amount);
    users[msg.sender].balance -= _amount;
  }

// - - - - - - Games - - - - - -
  function game(address _pl1, address _pl2, uint _bet, uint _resul) public onlyAdmin{
    checkUser(_pl1, _bet);
    checkUser(_pl2, _bet);

    if ((_resul % 2) == 0){
      users[_pl1].balance += _bet;
      users[_pl2].balance -= _bet;
      emit Winner("Player 1");
    }
    else{
      users[_pl2].balance += _bet;
      users[_pl1].balance -= _bet;
      emit Winner("Player 2");
    }
  }

  //= = = = = = INTERACTIONS WITH OTHER CONTRACTS = = = = = = =
  function setContract(string memory _contractName, address _contractAddress) public onlyAdmin{
    contracts[_contractName] = _contractAddress;
  }

  function getContractAddr(string memory _contractName) public onlyAdmin returns(address){
    return contracts[_contractName];
  }

  //- - - - - LevDistance - - - - -
  function obtainLevDistance(string memory _str1, string memory _str2, string memory _contractName) public payable returns(uint){
    LevDistanceInterface LevDistanceContract = LevDistanceInterface(contracts["levDistance"]);
    uint score = LevDistanceContract.levDistance(_str1, _str2);

    return score;
  }

  function gameLev(address _pl1, address _pl2, uint _bet, string memory _pl1Resul, string memory _pl2Resul, string memory _resul, string memory _contractName) public{

    checkUser(_pl1, _bet);
    checkUser(_pl2, _bet);

    uint pl1Score = obtainLevDistance(_pl1Resul, _resul, _contractName);
    uint pl2Score = obtainLevDistance(_pl2Resul, _resul, _contractName);

    if (pl1Score < pl2Score){
      users[_pl1].balance += _bet;
      users[_pl2].balance -= _bet;
      emit Winner("LevDistance: Player 1");
    }
    else if (pl1Score > pl2Score){
      users[_pl2].balance += _bet;
      users[_pl1].balance -= _bet;
      emit Winner("LevDistance: Player 2");
    }
    else{
      emit Winner("LevDistance: Draw");
    }
  }
}
