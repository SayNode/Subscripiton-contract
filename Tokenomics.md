# Tokenomics
1) Creator must stake A amount of DHN tokens in order to create a new data set. This tokens are staked directly in that DS contract
2) Every time the creator misses an upload schedule, he incurs in a penalty of value B. This penalty is taken by the Dohrnii organization, directly from the staked tokens in the corresponding DS contract. This penalties will help the Foundation pay for the operation. But how do we now if the update schedule has been broken without spending a lot of gas (constantly checking within the contract)?
    - **+**:
    - 
3) Subscribers must choose their sub time option (ex: *[1 day, 1 week, 1 month]*), if more than one are provided, and pay the equivalent amount in DHN tokens (ex: *[1 day = C DHN , 1 week = D DHN , 1 month = E DHN]*). This payment is locked to both parties (creator and subscriber) until one of 3 situations happens:
    - **A. The subscription time ends**: if the subscription time has ended, the subscriber has had the product he has payed for, so the creator can now withdraw that subscribers payment. EXPLICAR COMO
    - **B. The Data set is eliminated by the creator**: this can happen because the creator decided to trigger the selfdestruct function, for whatever reason. EXPLICAR COMO
    - **C. The Data set is eliminated due to zero stake**: because the creator has missed so many update schedules that the penalties have depleted all of his initially staked DHN tokens (aka his staked tokens become 0). EXPLICAR COMO