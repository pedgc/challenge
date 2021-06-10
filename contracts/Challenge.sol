pragma solidity ^0.5.0;

contract Challenge {

  /* = = = = = = TO DO = = = = = = = */
  /*
    * Learn how to optimize gas costs
    * See how to "froze" the money while betting
    * Calculate the levenshtein distance
      - Make it work for any string length
    * Transform this into a modular architecture
  */

  /* = = = = = = = VARIABLES & CONSTRUCTOR = = = = = = =*/
  //State variables -> Permanently saved in the contract
  address payable public admin;
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

// function getUsersCount() public view returns(uint) {
//   return users.length;
// }

// - - - - - - - - - -

// - - - - Future Modifications - - - -
function setAdmin(address payable _newAdmin) public onlyAdmin {
  admin = _newAdmin;
}
// - - - - - - - - - -

// - - - - Events - - - -
event Winner(string _winner); // Not able to obtain info inside a string
event Winner1();
event Winner2();

// - - - - Core - - - -
  function checkUser(address _userAddress, uint _amount) private{
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


  function gameLev(address _pl1, address _pl2, uint _bet, string memory _pl1Resul, string memory _pl2Resul, string memory _resul) public onlyAdmin{
    checkUser(_pl1, _bet);
    checkUser(_pl2, _bet);

    uint pl1Score = levDistance(_pl1Resul, _resul);
    uint pl2Score = levDistance(_pl2Resul, _resul);

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

// - - - - - - - - - -

// - - - - Testing Functions - - - -
  function levDistance(string memory _str1, string memory _str2) public pure returns(uint){
    uint length1 = bytes(_str1).length;
    uint length2 = bytes(_str2).length;
    uint n = max(length1, length2) + 1;
    uint[20][] memory distance = new uint[20][](n);
    bytes memory str1 = bytes(_str1);
    bytes memory str2 = bytes(_str2);

    for(uint i=0; i<=length1; i++){
      distance[i][0]=i;
    }
    for(uint j=0; j<=length2; j++){
      distance[0][j]=j;
    }
    for(uint i=1; i<=length1; i++){
      for(uint j=1; j<=length2; j++){
        uint aux = 1;
        if (str1[i-1] == str2[j-1]){
          aux = 0;
        }
        distance[i][j]= minimum(distance[i-1][j] + 1, distance[i][j-1] + 1, distance[i-1][j-1] + aux);
      }
    }

    return (distance[length1][length2]);
  }

  function minimum(uint a, uint b, uint c) public pure returns (uint){
    uint smallest;
    if (a <= b && a <= c) {
      smallest = a;
    } else if (b <= c && b <= a) {
      smallest = b;
    } else {
      smallest = c;
    }

    return (smallest);
  }

  function max(uint a, uint b) public pure returns (uint){
    uint resul;

    if(b > a){
      resul = b;
    } else {
      resul = a;
    }

    return (resul);
  }
}
