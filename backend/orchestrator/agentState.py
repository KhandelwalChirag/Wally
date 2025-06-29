from pydantic import BaseModel

class agentState (BaseModel):
    Budget : float
    isRecipie : bool
    recipe : str
    Items : list[str]
    cart : list[{str , float}] # string will be of datatype which can be used to build the actual Walmart Cart.

