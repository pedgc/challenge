pragma solidity ^0.5.0;

contract TextImage {

  /* = = = = = = = VARIABLES & CONSTRUCTOR = = = = = = =*/
  //State variables -> Permanently saved in the contract
  string private solution;
  address private admin;
  address payable[] private winners;
  address payable[] private contesters;
  uint public prize;
  bool public status;
  bool public prizeHasBeenSent;
  string public name;
  mapping(address => uint256) public users;

  constructor () public{
    admin = msg.sender;
    prize = 0;
    status = false;
    prizeHasBeenSent = false;
    name = "Text Reading Contest";
  }

  modifier onlyAdmin {
    require(msg.sender == admin, "Only admin can call this function");
        _;
  }
  // - - - - Event - - - -
  event Notification(string _notif, address _sender);

/* = = = = = = = FUNCTIONS = = = = = = = */
// - - - - Getters & Setters - - - -
function setAdmin(address _newAdmin) public onlyAdmin{
  admin = _newAdmin;
  emit Notification("The admin has been changed correctly", msg.sender);
}
function setName(string memory _name) public onlyAdmin{
  name = _name;
  emit Notification("The name has been changed correctly", msg.sender);
}

function getSolution() public view onlyAdmin returns(string memory){
  return solution;
}
function getWinners() public view onlyAdmin returns(address payable[] memory){
  return winners;
}
function getAdmin() public view returns(address){
  return admin;
}
function getPrize() public view returns(uint){
  return prize;
}
function getContesters() public view returns(address payable[] memory){
  return contesters;
}
function getPrizeHasBeenSent() public view returns(bool){
  return prizeHasBeenSent;
}
function getStatus() public view returns(bool){
  return status;
}
function getName() public view returns(string memory){
  return name;
}

// - - - - - Admin - - - - -

  function createContest(string memory _solution) public payable onlyAdmin{
    require(msg.value > 0, "Prize can not be 0");

    solution = _solution;
    status = true;
    prize = msg.value;

    emit Notification("The contest has been created correctly", msg.sender);
  }

  function calculateWinners() public onlyAdmin{
    require(contesters.length >= 1, "We should have at least 1 contester");

    uint min = users[contesters[0]];
    uint256 i;

    // Obtain the minimum score
    for(i = 1; i < contesters.length; i++){
        if(users[contesters[i]] < min) {
            min = users[contesters[i]];
        }
    }

    // Obtain all contesters with minimum score
    for(i = 0; i < contesters.length; i++){
      if(users[contesters[i]] == min) {
          winners.push(contesters[i]);
      }
    }

    emit Notification("The winner/s has/have been calculated correctly", msg.sender);
  }

  function sendPrizeToWinners() public payable onlyAdmin{
    require(winners.length >= 1, "We should have at least 1 winner");

    uint prizePerWinner = prize/winners.length;
    uint i;

    for(i = 0; i < winners.length; i++){
      winners[i].transfer(prizePerWinner);
    }

    prizeHasBeenSent = true;
    emit Notification("The prize has been sent to the winner/s", msg.sender);
  }

  // - - - - - - - Reset Contest - - - - - - - -
  function resetContest() public onlyAdmin{
    require(prizeHasBeenSent == true, "You can not reset the contest without sending prize to winner/s");

    solution = "";
    prize = 0;
    delete winners;
    delete contesters;
    status = false;

    emit Notification("The contest has been reset correctly", msg.sender);
  }


// - - - - Participants - - - -
  function contest(string memory _resul) public{
    require(msg.sender != admin, "Admin is not allowed to be a contester");
    require(status, "The contest is not active");
    users[msg.sender] = obtainScore(_resul, solution);
    contesters.push(msg.sender);
  }

  //Explain about levehnstein distance
  function obtainScore(string memory _str1, string memory _str2) private pure returns(uint256){
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

    return (uint256(distance[length1][length2]));
  }

  function minimum(uint a, uint b, uint c) private pure returns (uint){
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

  function max(uint a, uint b) private pure returns (uint){
    uint resul;

    if(b > a){
      resul = b;
    } else {
      resul = a;
    }

    return (resul);
  }

}
