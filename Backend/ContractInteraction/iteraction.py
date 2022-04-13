from solcx import compile_standard, install_solc
import json
#Read the code in the contract
with open("./contracts/DataSetFactory.sol", "r") as file:
    simple_storage_file = file.read()

# We add these two lines that we forgot from the video!
print("Installing...")
install_solc("0.8.13")

# Solidity source code
compiled_sol = compile_standard(#gets the contract info in json format
    {
        "language": "Solidity",
        "sources": {"SimpleStorage.sol": {"content": simple_storage_file}},
        "settings": {
            "outputSelection": {
                "*": {
                    "*": ["abi", "metadata", "evm.bytecode", "evm.bytecode.sourceMap"]#info we want
                }
            }
        },
    },
    solc_version="0.8.13",
)
#Write the deployed contract json into a file
with open("compiled_code.json", "w") as file:
    json.dump(compiled_sol, file)

#Get bytecode from the json ouput of compiled_sol
bytecode = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["evm"][
    "bytecode"
]["object"]

#Get bytecode from the json ouput of compiled_sol
abi = json.loads(
    compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["metadata"]
)["output"]["abi"]
