if MODE == "INITIALIZATION":
    CACHE["WAVES"] = []

elif MODE == "RUNNING":
    #CACHE["WAVES"] =[]
    data = INPUT["Data In"]
    print("--------------------")
    print(CACHE["WAVES"])
    print("--------------------")
    if (len(CACHE["WAVES"])==5):
        # if(data == "beta" or data == "gamma"):
        #     OUTPUT["Data Out"] = True
        countG = 0
        countElse = 0
        for i in CACHE["WAVES"]:
            if i == 'gamma':
                countG+=1
            if i != 'gamma':
                countElse+=1

        if (countG>countElse):
            OUTPUT["Data Out"] = True
        else:
            print("#33333################")
            OUTPUT["Data Out"] = False
        CACHE["WAVES"]=[]

    else:
        CACHE["WAVES"].append(data)


elif MODE == "DESTRUCTION":
    del CACHE["WAVES"]