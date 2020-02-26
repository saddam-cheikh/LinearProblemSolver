#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 10 00:03:17 2020

@author: cheikh saddam

"""
import time
# Heuristique : deux fonctions pour choisir les indices
def funcLeavingIndex(l):
    m = 0
    while not l[m] and m < len(l):
        m += 1
    if m == len(l):
        return 0
    for i in range(len(l)):
        if l[i] and l[m] > l[i]:
            m = i
    return m

def funcEnteringIndex(l):
    return l.index(min(l))
            

class _Simplex(object):
   
    
    # attributs :
    # - entering: fonction qui prend en entrée une instance de LP et renvoie une
    #   variable entrante pour le pivot. 
    # - leaving: fonction qui prend en entrée une instance de LP, une variable
    #   entrante et renvoie une variable sortante.
    
    def __init__(self, leaving_index=None, entering_index=None):
        
        #Ici l'utilisateur peut faire le choix des fonctions de recherche d'indices 
        if not leaving_index:
            leaving_index = funcLeavingIndex

        if not entering_index:
            entering_index = funcEnteringIndex
        
        self.leaving = leaving_index
        self.entering = entering_index
    
    def __call__(self, lp):
      
        a = lp.table

        
        non_borne=True
        n = 0 #itérateur récursif
        cpt=0
        start_time = time.time()#début d'enregistrement du temps
        while any(a[0, :-1] < 0) :
            
            entering_choices = [i for i in map(lambda x: 0 if x > 0 else x,a[0, :-1])]
           
            e = self.entering(entering_choices) # on choisit l'indice de la plus petite valeur négative
                 
            leaving_choices = [None]*lp.shape[0]
            # On divise la dernière colonne par les coefficients de la colonne de l 'indice d'entrée
            for i in range(lp.shape[0]): 
                if a[i+1, e] > 0:
                    leaving_choices[i] = (a[i+1, -1]/a[i+1, e])
            if not [i for i in leaving_choices if i]:
                raise OverflowError("Linear program unbounded | check model and state.")
            else:
                # l'indice correspont à la valeur de la clé à partir du dictionnaire
                s = lp.basic_vars[self.leaving(leaving_choices)]
               
          
          
            lp.pivot(e, s)
            ####test de bornitude####
            for i in range(lp.shape[0]+lp.shape[1]):
                if any(a[:,i] >= 0):
                    cpt=cpt+1
            if cpt==lp.shape[0]+lp.shape[1]:
                non_borne=False
            cpt=0
            
            
            n += 1
        execution_time=time.time()-start_time # fin d'enregistrement du temps
        return lp, lp.basic_sol(), lp.table[0, -1], n, execution_time,non_borne

class Simplex(_Simplex):
    
    def  _phase_one(self,lp):
        
        if lp.basic_feasible:
            print("Le problème linéaire admet une solution de base", end="\n\n")
            return True
        
        gain_fun = np.copy(lp.table[0])

        lp.shape = (lp.shape[0], lp.shape[1] + 1)
        lp.table = np.insert(lp.table, 0, -1, axis=1)
        lp.table[0] = np.hstack((np.ones(1, dtype=float),
                                    np.zeros(lp.shape[1]+lp.shape[0], dtype=float)))
        
       
        for i in lp.basic_vars.keys():
            lp.basic_vars[i]=lp.basic_vars[i]+1
            
         

        l =   lp.basic_vars[np.argmin(lp.table[1:, -1])]
        lp.pivot(0, l)  

        if _Simplex.__call__(self, lp)[2] == 0:
            print(" ### Input linear program is thus feasible", end="\n\n")

            if 0 in lp.basic_vars.values():
                l = [c for c,v in lp.basic_vars.items() if v==0][0]

                e = 0
                while e < lp.shape[1] and lp.table[l, e] == 0:
                    # There is a at least an e with this property
                    # Unbounded otherwise
                    e += 1
                lp.pivot(e, l)  # 0 not basic anymore

            
            for i in lp.basic_vars.keys():
                lp.basic_vars[i]=lp.basic_vars[i]-1
            
            lp.table = lp.table[:, 1:]
            lp.shape = (lp.shape[0], lp.shape[1] - 1)

            lp.table[0] = gain_fun
            for i in lp.basic_vars.values():
                l = [c for c,v in lp.basic_vars.items() if v==i][0]
                lp.table[0, :] = lp.table[0, :] - \
                                      lp.table[0, i] * \
                                      lp.table[1 + l, :]
            lp.table[0, -1] = -lp.table[0, -1]

            return True

        else:
            return False
        
        
    def __call__(self, lp):
        simplex = _Simplex()
        
        if lp.basic_feasible:
            print("Le problème a une solution de base admissible")
            return simplex(lp)
        elif not lp.basic_feasible and lp.dual().basic_feasible:
            print("Le problème dual a une solution de base admissible")
            return simplex(lp.dual())
        elif self._phase_one(lp):
            print("Ni le problème ni son dual n'admettent de solutions admissibles mais le problème équivalent en admet")
            return simplex(lp)
        else:
            raise Exception("Linear program is not feasible.")
            
            
            
        
      
        

        
        


      