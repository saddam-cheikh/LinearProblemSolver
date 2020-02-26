#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 18 12:20:02 2020

@author: cheikh saddam
"""
import pickle
import pandas as pd
def gen_LP(borne_sup,m,n,i):

    Ins={}
  

    a=np.random.randint(-borne_sup,borne_sup, size=(m, n))
    b=np.random.randint(-borne_sup,borne_sup, size=(m, 1))
    c=np.random.randint(-borne_sup, borne_sup, n)
    lp=LP(a,b,c)
   
    spx =Simplex()
    _spx=_Simplex()
    try:
            
        Ins["name"]=i
        Ins["LP"]=lp
        Ins["heuristique"]=1
        Ins["shape" ]=lp.shape
        Ins["basic_feasible"]=lp.basic_feasible
        Ins["feasible"]= spx._phase_one(lp)
        Ins["dual_basic_feasible"]=lp.dual().basic_feasible
        Ins["bounded"]=not _spx(lp)[5]
    except :
        print("Error")
    
    serial=pickle.dumps(Ins)
    
    return Ins

def gen_LP_PD(borne_sup,m,n,i):

    Ins={}
  

    a=np.random.randint(-borne_sup,borne_sup, size=(m, n))
    b=np.random.randint(-borne_sup,borne_sup, size=(m, 1))
    c=np.random.randint(-borne_sup, borne_sup, n)
    lp=LP(a,b,c)
   
    spx =Simplex()
    _spx=_Simplex()
    try:
            
        Ins["name"]=i
        Ins["LP"]=pickle.dumps(lp)
        Ins["heuristique"]=1
        Ins["shape" ]=pickle.dumps(lp.shape)
        Ins["basic_feasible"]=lp.basic_feasible
        Ins["feasible"]= spx._phase_one(lp)
        Ins["dual_basic_feasible"]=lp.dual().basic_feasible
        Ins["bounded"]=not _spx(lp)[5]
    except :
        print("Error")
    
    
    
    return Ins

def gen_LP_df(borne_sup,m,n,n_instance):

    
  
    df = pd.DataFrame(columns = ["name", "LP", "heuristique","shape","basic_feasible","feasible","dual_basic_feasible","bounded"])
    for i in range(1,n_instance):
        
        Ins={}
  

        a=np.random.randint(-borne_sup,borne_sup, size=(m, n))
        b=np.random.randint(-borne_sup,borne_sup, size=(m, 1))
        c=np.random.randint(-borne_sup, borne_sup, n)
        lp=LP(a,b,c)
   
        spx =Simplex()
        _spx=_Simplex()
        try:
            
            df.loc[i,"name"]=i
            df.loc[i,"LP"]=pickle.dumps(lp)
            df.loc[i,"heuristique"]=1
            df.loc[i,"shape" ]=lp.shape
            df.loc[i,"basic_feasible"]=lp.basic_feasible
            df.loc[i,"feasible"]= spx._phase_one(lp)
            df.loc[i,"dual_basic_feasible"]=lp.dual().basic_feasible
            df.loc[i,"bounded"]=not _spx(lp)[5]
        except :
            print("Error")
    
    
    return df



        
            
       
#pickle.loads(gen_LP(10,3,3,1))
          
       

        
    



