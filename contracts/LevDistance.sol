pragma solidity ^0.5.0;

contract LevDistance {

  /* = = = = = = = VARIABLES & CONSTRUCTOR = = = = = = =*/
  //State variables -> Permanently saved in the contract
  address public admin;

  constructor () public{
    admin = msg.sender;
  }

  modifier onlyAdmin {
    require(msg.sender == admin, "Only admin can call this function");
        _;
  }

/* = = = = = = = FUNCTIONS = = = = = = = */
// - - - - Getters - - - -

// - - - - - - - - - -

// - - - - Future Modifications - - - -
function setAdmin(address _newAdmin) public onlyAdmin {
  admin = _newAdmin;
}
// - - - - - - - - - -

// - - - - Events - - - -

// - - - - Core - - - -

  function levDistance(string memory _str1, string memory _str2) public payable returns(uint){
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
    // uint a = 1;
    // return a;
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
