pragma solidity ^0.5.0;

contract DogsOrCats {

  /* = = = = = = = VARIABLES & CONSTRUCTOR = = = = = = =*/
  //State variables -> Permanently saved in the contract
  uint[] private solution;
  address private admin;
  address payable[] private winners;
  address payable[] private contesters;
  uint private prize;
  bool private status;
  bool private prizeHasBeenSent;
  string private name;
  mapping(address => uint256) private users;

  constructor () public{
    admin = msg.sender;
    prize = 0;
    status = false;
    prizeHasBeenSent = false;
    name = "Cats or Dogs Contest";
  }

  modifier onlyAdmin {
    require(msg.sender == admin, "Only admin can call this function");
        _;
  }

/* = = = = = = = FUNCTIONS = = = = = = = */
// - - - - Getters & Setters - - - -
function setAdmin(address _newAdmin) public onlyAdmin{
  admin = _newAdmin;
}
function setName(string memory _name) public onlyAdmin{
  name = _name;
}

function getWinners() public view onlyAdmin returns(address payable[] memory){
  return winners;
}
function getSolution() public view onlyAdmin returns(uint[] memory){
  return solution;
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

// - - - - - - - - - - - - - - - - -

// - - - - Events - - - -
event Notification(string _notif, address _sender);

// - - - - - Admin - - - - -

  function createContest(uint[] memory _solution) public payable onlyAdmin{
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

    delete solution;
    prize = 0;
    delete winners;
    delete contesters;
    status = false;

    emit Notification("The contest has been reset correctly", msg.sender);
  }


// - - - - Participants - - - -
  function contest(uint[] memory _resul) public{
    require(msg.sender != admin, "Admin is not allowed to be a contester");
    require(_resul.length == solution.length, "The dataset length is not correct");
    require(status, "The contest is not active");
    users[msg.sender] = obtainScore(_resul);
    contesters.push(msg.sender);
  }

  function obtainScore(uint[] memory _resul) private view returns(uint256){

    uint score = 0;
    uint length = solution.length;

    for(uint i=0; i<length; i++){
      if (_resul[i] != solution[i]){
        score++;
      }
    }

    return score;
  }

}
