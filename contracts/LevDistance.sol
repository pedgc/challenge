pragma solidity ^0.5.0;

contract LevDistance {

  /* = = = = = = = VARIABLES & CONSTRUCTOR = = = = = = =*/
  //State variables -> Permanently saved in the contract
  string private solution;
  address private admin;
  address private winner;
  address[] private contesters;
  mapping(address => uint256) public users;

  constructor () public{
    admin = msg.sender;
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

function getSolution() public onlyAdmin returns(string memory){
  return solution;
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
  function setWinner() public onlyAdmin{
    uint min = users[contesters[0]];
    address _winner = contesters[0];
    uint256 i;

    for(i = 1; i < contesters.length; i++){
        if(users[contesters[i]] < min) {
            min = users[contesters[i]];
            _winner = contesters[i];
        }
    }

    winner = _winner;
  }

  function getWinner() public view onlyAdmin returns(address){
    return winner;
  }
}
