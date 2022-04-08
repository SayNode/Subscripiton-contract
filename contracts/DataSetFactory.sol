//SPDX-License-Identifier: SayNode
pragma solidity 0.8.13;

import "./DataSet.sol";//SC to be replicated
import "@openzeppelin/contracts/access/Ownable.sol";//Garantee only the DS creator can change its parameters
import "@openzeppelin/contracts/token/ERC20/IERC20.sol";//To interact with ERC20
import "@openzeppelin/contracts/security/ReentrancyGuard.sol";//Avoid double buying creation

contract DataSetFactory is ReentrancyGuard, Ownable{

    //
    //VARIABLES
    //

        //Minimum amount to stake
        uint256 stakeAmount;

        //Token Contract address placeholder
        IERC20 public DHN;
        address DHNAddress;

        //Creator arrays
        address[] public creators;

        //Quick way to see if the creator is new or not
        mapping(address => bool) public creatorExists;

        //Creator address to the array of his created DS smart contract addresses
        mapping(address => DataSet[]) public addressToSC;

        //Mapping of a DS name to the corresponding DataSet smart contract
        mapping(string => DataSet) public nameToSC;

    //
    //CONSTRUCTOR
    //
        //Establish the DHN token contract for later use
        constructor(address _DHNAddress){
            DHNAddress = _DHNAddress;
            DHN = IERC20(_DHNAddress);
        }

    //
    //FUNCTIONS
    //

        //Create a new DataSet (which requires the creation of a new DataSet.sol SC)
        function createDS(
                string memory _DSname,//Dataset name
                string memory _URL,//IPFS url link
                string memory _category,//Dataset category
                string memory _shortDesc,//Dataset short description
                uint256 _DSprice,//Dataset price
                uint256 _updateFrequency //Dataset update frequency
            ) public payable nonReentrant
        {
                

                //Creator must have the same or more DHN tokens than the required amount
                require(DHN.balanceOf(msg.sender)>= stakeAmount);
                
                //Stake in this contract
                DHN.approve(address(this), stakeAmount);

                //Creates a new SC dor the new DataSet
                DataSet dataset = new DataSet(address(this), DHNAddress, _DSname, _URL, _category, _shortDesc, msg.sender, 
                                            _DSprice, _updateFrequency, stakeAmount);
                //Must send the stake DHN tokens from this contract to the newly created child
                DHN.transferFrom(msg.sender, dataset, stakeAmount);//TO DO- see what dataset has (how to isolate the address)

                //Maps the new DS name to its contract address
                nameToSC[_DSname]=dataset;
                //Maps the new DS contract address to its creator address
                addressToSC[msg.sender].push(dataset);

                if(!creatorExists[msg.sender]){//if it is a new creator
                    creators.push(msg.sender);//add creator address to the array of creators
                    creatorExists[msg.sender] = true;
                }
        }

        //Change the minimum amount of DHN tokens that is needed to create a Data set contract
        function changeStakeAmount(uint _stakeAmount) public onlyOwner{

            stakeAmount = _stakeAmount;

        }
        function deleteDS() public {//will delete the Data Set of a creator because he selfdestructed the corresponding DataSet.sol
                                    //is used as an interface in DataSet.sol
            //TO DO

        }
    
}