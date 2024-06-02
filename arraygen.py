import random
import time

if MODE == "INITIALIZATION":
    pass

elif MODE == "RUNNING":
    OUTPUT["Data Out"] = random.choice(["delta", "theta", "alpha", "beta", "gamma"])
    time.sleep(1)

elif MODE == "DESTRUCTION":
    pass

PROCESS()