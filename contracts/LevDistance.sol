pragma solidity ^0.5.0;

contract LevDistance {

  /* = = = = = = = VARIABLES & CONSTRUCTOR = = = = = = =*/
  //State variables -> Permanently saved in the contract
  string private solution;
  address private admin;
  address payable[] private winners;
  address payable[] private contesters;
  uint prize;
  mapping(address => uint256) public users;

  constructor () public{
    admin = msg.sender;
    prize = 0;
  }

  modifier onlyAdmin {
    require(msg.sender == admin, "Only admin can call this function");
        _;
  }

/* = = = = = = = FUNCTIONS = = = = = = = */
// - - - - Getters & Setters - - - -
function setAdmin(address _newAdmin) public onlyAdmin {
  admin = _newAdmin;
}
function setSolution(string memory _solution) public onlyAdmin{
  solution = _solution;
}
function setPrize() public payable onlyAdmin{
  require(msg.value > 0, "Prize can not be 0");
  prize = msg.value;
}

function getAdmin() public view returns(address){
  return admin;
}
function getSolution() public view onlyAdmin returns(string memory){
  return solution;
}
function getPrize() public view returns(uint){
  return prize;
}
function getWinners() public view onlyAdmin returns(address payable[] memory){
  return winners;
}

// - - - - - - - - - - - - - - - - -

// - - - - Events - - - -
event Winner(string _winner);

// - - - - - - - - - -

// - - - - Participants - - - -
  function contest(string memory _resul) public{
    users[msg.sender] = levDistance(_resul, solution);
    contesters.push(msg.sender);
  }

  function levDistance(string memory _str1, string memory _str2) private pure returns(uint256){
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

// - - - - - - - Winner & prize - - - - - - - -
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

  }

  function sendPrizeToWinners() public payable onlyAdmin{
    require(winners.length >= 1, "We should have at least 1 winner");

    uint prizePerWinner = prize/winners.length;
    uint i;

    for(i = 0; i < winners.length; i++){
      winners[i].transfer(prizePerWinner);
    }
    emit Winner("Finished sending prizes");
  }

  // - - - - - - - Reset Contest - - - - - - - -
  function resetContest() public onlyAdmin{
    solution = "";
    prize = 0;
    delete winners;
    delete contesters;
  }


}
