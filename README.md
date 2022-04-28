# Main concerns right now:

1) When do we want to verify/update if the user is still subscribed?
2) When do we want to verify if the creator has respected his update schedule?
3) Do we want to do the previous two on the backend (just view the values for free, calculate and then do the changes in the    

# Run instructions
- Build the docker image:

> docker build -t subscription-contract

- When it is finished, you can run it:

> docker run subscription-contract

- Now you can test particular events like:
1) The creation of a new Data Set (test_CreateDS.py)
2) Test the functions within an existing Data Set (test_DSfunctions.py)
3) Test subbing to a DS (test_SubToDS.py)
4) Test the upgradeability of the DataSetFactory contract (test_UpgradeDS.py)
- You can write your own scrippt (maybe within a main() function in "deploy.py") and run it, but to do this, you need to rebuild the docker image.