//SPDX-License-Identifier: SayNode
pragma solidity 0.8.13;

import "./DataSet.sol";
import "@openzeppelin/contracts/security/ReentrancyGuard.sol";//Avoid double buying creation

contract DataSetFactory is ReentrancyGuard{

    //Owner of this contract
    address public owner;

    //Creator arrays
    address[] public creators;
    /*struct Creator{
        bool creatorExists;
        DataSet[] SCaddress;
    }
    mapping(address => Creator) public addressToCreator;
    */
    mapping(address => bool) public creatorExists;

    //Creator address to the array of his created DS smart contract addresses
    mapping(address => DataSet[]) public addressToSC;

    //Mapping of a DS name to the corresponding DataSet smart contract
    mapping(string => DataSet) public nameToSC;

    //Constructor
    constructor(){
        owner = msg.sender;
    }

    //Create a new DataSet (which requires the creation of a new DataSet.sol SC)
    function createDS(
            string memory _DSname,//Dataset name
            string memory _URL,//IPFS url link
            string memory _category,//Dataset category
            string memory _shortDesc,//Dataset short description
            uint256 _DSprice,//Dataset price
            uint256 _updateFrequency //Dataset update frequency
        ) public nonReentrant
    {
            //MUST REQUIRE THE CREATOR TO DEPOSIT/STAKE SOME DHN TOKENS IN THIS CONTRACT
            //Creates a new SC dor the new DataSet
            DataSet dataset = new DataSet(_DSname, _URL, _category, _shortDesc, msg.sender, _DSprice, _updateFrequency);
            //Maps the new DS name to its contract address
            nameToSC[_DSname]=dataset;
            //Maps the new DS contract address to its creator address
            addressToSC[msg.sender].push(dataset);

            if(!creatorExists[msg.sender]){//if it is a new creator
                creators.push(msg.sender);//add creatopr address to the array of creators
                creatorExists[msg.sender] = true;
            }
    }
    
}