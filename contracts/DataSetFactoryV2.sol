//SPDX-License-Identifier: SayNode
pragma solidity 0.8.13;

import "./DataSet.sol";//SC to be replicated
import "OpenZeppelin/openzeppelin-contracts@4.4.2/contracts/access/Ownable.sol";//Garantee only the DS creator can change its parameters
import "OpenZeppelin/openzeppelin-contracts@4.4.2/contracts/token/ERC20/IERC20.sol";//To interact with ERC20
import "OpenZeppelin/openzeppelin-contracts@4.4.2/contracts/security/ReentrancyGuard.sol";//Avoid double buying creation
import "OpenZeppelin/openzeppelin-contracts@4.4.2/contracts/proxy/utils/Initializable.sol";//https://docs.openzeppelin.com/upgrades-plugins/1.x/proxies

contract DataSetFactoryV2 is ReentrancyGuard, Ownable, Initializable{

    //
    //VARIABLES
    //

        //Minimum amount to stake
        uint256 public stakeAmount=20*10**18;

        //Token Contract address placeholder
        IERC20 public DHN;
        address DHNAddress;

        //Creator arrays
        address[] public creators;

        //Quick way to see if the creator is new or not
        //Front end use: Used to search DSs by cretaor
        mapping(address => bool) public creatorExists;

        //Creator address to the array of his created DS smart contract addresses
        //Front end use: Used to search DSs by cretaor
        mapping(address => DataSet[]) public addressToSC;

        //Mapping of a DS name to the corresponding DataSet smart contract
        //Front end use: Used to search DSs by its name
        mapping(string => DataSet) public nameToSC;

        //Quick way to see if the DataSet contract address is new or not
        //Front end use: Used to search DSs and see if they exist or not
        //Complements the previous two mappings
        mapping(address => bool) public contractExists;

     //
    //CONSTRUCTOR->As this contract is acessed by proxy, the constructor must be replaced by a function that is only called once
    //             This this function must be called whenever the proxy links to this logic contract
    //
 
        
    //
    //MODIFIERS
    //
    modifier onlyChildContracts(){
        require(contractExists[msg.sender]==true);//msg.sender here is the DataSet. sol contract
        _;
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
                uint256 _updateFrequency, //Dataset update frequency
                uint256 penalty //how much staked DHN the creator looses for missing a deadline. 
                                //Dependes on the upload freq, so for now it is always the same but in the long run we will
                                //do it with a conditional
            ) public payable nonReentrant
        {
                

                //Creator must have the same or more DHN tokens than the required amount
                require(DHN.balanceOf(msg.sender)>= stakeAmount, "Not enough DHN tokens");

                //REQUIRE THE URL TO NOT EXIST YET --TO DO

                //Creates a new SC dor the new DataSet
                DataSet dataset = new DataSet(address(this), DHNAddress, _DSname, _URL, _category, _shortDesc, msg.sender, 
                                            _DSprice, _updateFrequency, stakeAmount, penalty);
                //Must send the stake DHN tokens from this contract to the newly created child
                DHN.transferFrom(msg.sender, payable(address(dataset)), stakeAmount);
                // or payable(address(dataset)).call{value:  stakeAmount}("");

                //Update this mapping to say that this contract address still exists
                contractExists[address(dataset)]=true;

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

        function deleteChild(address _DS_address) external view onlyChildContracts(){//will delete the Data Set of a creator because 
                                                                        //he selfdestructed the corresponding DataSet.sol
            contractExists[_DS_address]==false;
        }

        //This function only exists in this contract and not in DataSetFactory.sol
        function upgradeFunction() public pure returns(string memory){
            return "The contract was upgraded";
        }
    
}