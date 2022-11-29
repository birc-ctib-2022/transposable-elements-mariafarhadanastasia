
active_list=[]

def list_test(n):
    return (['-']*n) #sketch of how to initiate an empty genome of n lenght



list_test(26)


#listt=list_test(100)

active_TEs=[] #making empty list for now for the active TEs. will be list of list with [ID,start,end] of each TE.

def Te_ID_generator(active_TEs): #function for making IDs for TEs so they all get a different number.
    return max([item[0] for item in active_TEs])+1 #may need an insurance against reuse of "names"/ID numbers. but so far works.dr

active_TE_test_list=[[3,2,3],[4,5,6],[5,6,7]]

#print(Te_ID_generator(active_TE_test_list))

def get_start_end(active_list,te):#function that is needed later for copying and getting the position of a certain TE.
    for i in range(0,len(active_list)):
        if active_list[i][0]==te:
            start=active_list[i][1]
            end=active_list[i][2]
    return start, end

#print(get_start_end(active_TE_test_list,3))


def insert_te(genome,i,active_list,n,k=1,l=1):
    ID_new_TE=Te_ID_generator(active_list)
    #i is position, n is length, k and l are "accumulators"
    in_existing_te=False
    if type(genome[i])==int:
        in_existing_te=True #cheking if the new TE is overlapping an old TE in the genome sequnece.
    if in_existing_te==True:
        te_for_inactivation=genome[i] #remove old TE from active list
        for o in range(0,len(active_list)-1): #in doubt about the -1.
            if active_list[o][0]==te_for_inactivation:
                del active_list[o]
        if type(genome[i+n+k])==te_for_inactivation: #if to the side of the new TE there are rests of old TE they should be set to X.
             genome[i+n+k]="X"#is this correct THINK AOBUT IT!??!?!?!?!?!??!
             k+=1
        if type(genome[i-1])==te_for_inactivation: #the other side
             genome[i-1]="X"
             l+l
    genome[i:i]=[ID_new_TE]*n #insert the new TE
    active_TEs.append([ID_new_TE,i,i+n]) #put in the new TE in the active list
    for m in range(0,len(active_list)):#update positions of TE's that are later in the genome than the new TE in the active list
        if active_list[m][1]>=i:
            active_list[m][1]=active_list[m][1]+n
            active_list[m][2]=active_list[m][2]+n
    return genome, active_list


const_gen=['-','-','A','A','A','A','-','-','A']
active_TE_test_list=[[3,2,3],[4,5,6],[5,6,7]]
print(insert_te(const_gen,2,active_TE_test_list,18))
print(active_TEs)


def copy_te(genome,te,active_list, offset):
     start,end=get_start_end(active_list,te)
     genome[start+offset:start+offset]=genome[start:end]#the actual copying
     for p in range(0,len(active_list)):
        if active_list[p][1]>=start:
            active_list[p][1]=active_list[p][1]+abs(start-end)#updating in the active_liste
            active_list[p][2]=active_list[p][2]+abs(start-end)
     return genome, active_list






    


