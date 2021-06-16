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
    // contracts["levDistance"] = address(0xF06739343c62C29259e03a04DaF0CC0d59E1DF3a);
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
      //emit Winner1();
    }
    else{
      users[_pl2].balance += _bet;
      users[_pl1].balance -= _bet;
      emit Winner("Player 2");
      //emit Winner2();
    }
  }

  //= = = = = = INTERACTIONS WITH OTHER CONTRACTS = = = = = = =
  function setContract(string memory _contractName, address _contractAddress) public{
    // address addr = stringToAddress(bytes(_contractAddress));
    contracts[_contractName] = _contractAddress;
    // address addr = 0x3D5a900559b31aAAD3B74A3E76F0F16B4eD985aB;
    // contracts[_contractName] = addr;
    emit Winner("LevDistance: Ending setContract");
  }

  function getContractAddr(string memory _contractName) public returns(address){
    // address addr = stringToAddress(bytes(_contractAddress));
    emit Winner("LevDistance: In getContractAddr");
    return contracts[_contractName];
  }

  //- - - - - LevDistance - - - - -
  function obtainLevDistance(string memory _str1, string memory _str2, string memory _contractName) public payable returns(uint){
    // emit Winner("LevDistance: In obtainLevDistance");
    LevDistanceInterface LevDistanceContract = LevDistanceInterface(contracts["levDistance"]);
    uint score = LevDistanceContract.levDistance(_str1, _str2);
    // emit Winner("LevDistance: After the call to LevDistanceContract");
    //
    return score;
    // return 1;
  }

  function gameLev(address _pl1, address _pl2, uint _bet, string memory _pl1Resul, string memory _pl2Resul, string memory _resul, string memory _contractName) public{
    // emit Winner("LevDistance: In Gamelev");

    checkUser(_pl1, _bet);
    checkUser(_pl2, _bet);

    uint pl1Score = obtainLevDistance(_pl1Resul, _resul, _contractName);
    uint pl2Score = obtainLevDistance(_pl2Resul, _resul, _contractName);

    // emit Winner("LevDistance: Ending Gamelev");

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

// // - - - - - - - - - -
//
// // - - - - Testing Functions - - - -
//   function levDistance(string memory _str1, string memory _str2) public pure returns(uint){
//     uint length1 = bytes(_str1).length;
//     uint length2 = bytes(_str2).length;
//     uint n = max(length1, length2) + 1;
//     uint[20][] memory distance = new uint[20][](n);
//     bytes memory str1 = bytes(_str1);
//     bytes memory str2 = bytes(_str2);
//
//     for(uint i=0; i<=length1; i++){
//       distance[i][0]=i;
//     }
//     for(uint j=0; j<=length2; j++){
//       distance[0][j]=j;
//     }
//     for(uint i=1; i<=length1; i++){
//       for(uint j=1; j<=length2; j++){
//         uint aux = 1;
//         if (str1[i-1] == str2[j-1]){
//           aux = 0;
//         }
//         distance[i][j]= minimum(distance[i-1][j] + 1, distance[i][j-1] + 1, distance[i-1][j-1] + aux);
//       }
//     }
//
//     return (distance[length1][length2]);
//   }
//
//   function minimum(uint a, uint b, uint c) public pure returns (uint){
//     uint smallest;
//     if (a <= b && a <= c) {
//       smallest = a;
//     } else if (b <= c && b <= a) {
//       smallest = b;
//     } else {
//       smallest = c;
//     }
//
//     return (smallest);
//   }
//
//   function max(uint a, uint b) public pure returns (uint){
//     uint resul;
//
//     if(b > a){
//       resul = b;
//     } else {
//       resul = a;
//     }
//
//     return (resul);
//   }
}
