pragma solidity ^0.5.0;

contract TextImage {

  /* = = = = = = = VARIABLES & CONSTRUCTOR = = = = = = =*/
  string private solution;                    // Correct answer of the contest
  address private admin;                      // Address of the contract Owner
  address payable[] private winners;          // List of the winners of the contest
  address payable[] private contesters;       // List of the contesters
  uint private prize;                         // Prize amount (in Wei)
  bool private status;                        // The contest is Active or Inactive
  bool private prizeHasBeenSent;              // To check if the prize has been sent to winners
  string private name;                        // Contest name
  mapping(address => uint256) private users;  // All users of all contests

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
function getSolution() public view onlyAdmin returns(string memory){
  return solution;
}
function getWinners() public view returns(address payable[] memory){
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
    require(!status, "You can not create a contest while there is an ongoing one");

    solution = _solution;
    status = true;
    prize = msg.value;

    emit Notification("The contest has been created correctly", msg.sender);
  }

  function calculateWinners() public onlyAdmin{
    require(contesters.length >= 1, "We should have at least 1 contester");

    delete winners;
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
    require(prizeHasBeenSent == false, "The prize has already been sent");

    uint prizePerWinner = prize/winners.length;
    uint i;

    for(i = 0; i < winners.length; i++){
      winners[i].transfer(prizePerWinner);
    }

    prizeHasBeenSent = true;
    emit Notification("The prize has been sent to the winner/s", msg.sender);
  }

  function expelWinner(address _winner) public onlyAdmin{
    require(winners.length >= 1, "We should have at least 1 winner");
    require(prizeHasBeenSent == false, "Too late, the prize has already been sent");

    uint i;
    bool flag = true;

    for(i = 0; (i < winners.length) && flag; i++){
      if(winners[i] == _winner) {
        delete winners[i];
        winners[i] = winners[winners.length - 1];
        winners.length--;
        flag = false;
        emit Notification("The winner has been expelled", msg.sender);
      }
    }
  }

  function resetContest() public onlyAdmin{
    require(prizeHasBeenSent == true, "You can not reset the contest without sending prize to winner/s");

    solution = "";
    prize = 0;
    delete winners;
    delete contesters;
    status = false;
    prizeHasBeenSent = false;

    emit Notification("The contest has been reset correctly", msg.sender);
  }

// - - - - Contesters - - - -
  function contest(string memory _resul) public{
    require(msg.sender != admin, "Admin is not allowed to be a contester");
    require(winners.length == 0, "Contest period is over. Winners have been selected");
    require(status, "The contest is not active");

    users[msg.sender] = obtainScore(_resul, solution);
    if(isFirstAttempt(msg.sender)){
      contesters.push(msg.sender);
    }

    emit Notification("Your solution has been sent", msg.sender);
  }

  // The lower the score, the better:
  // To obtain the score, the 'Levenshtein distance' algorithm is used. It obtains
  // the minimum number of modifications that must be made to a chain so that it
  // is equal to the other. Solidity limitations:
  //   1. The maximun length can not be variable. In this scenario -> 200 characters
  //   2. As we are comparing bytes (not characters), just 32B characters are allowed
  function obtainScore(string memory _str1, string memory _str2) private pure returns(uint256){
    uint length1 = bytes(_str1).length;
    uint length2 = bytes(_str2).length;
    uint n = max(length1, length2) + 1;
    uint[200][] memory distance = new uint[200][](n);
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

  function isFirstAttempt(address) private view returns(bool){
    bool resul = true;

    for(uint i=0; i<contesters.length && resul; i++){
      if(contesters[i] == msg.sender){
        resul = false;
      }
    }

    return resul;
  }

}
