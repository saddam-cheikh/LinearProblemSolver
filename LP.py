#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan  9 14:04:16 2020

@author: cheikh saddam
"""
import pandas as pd
import numpy as np


class LP(object):
    #Les attributs :
    #  - shape : un couple d’entiers (m, n) où m représente le nombre de contraintes
    #   (hors contraintes de positivités) et n le nombre de variables du programme
    #  linéaire.
    #  - basic_sol : la solution de base du programme linéaire LP donné comme
    #   un numpy array
    #  - basic_feasible : un booléen à True si le programme linéaire a une
    #   solution de base admissible et à False sinon
    #  - basic_vars : un dictionnaire dont les clés sont {1, . . . , m} et les valeurs
    #   prises dans {0, . . . , n − 1} (les indices des variables du programme)
    #  - table : un objet numpy.array (ou mieux un pandas.DataFrame avec
    #   colonnes nommées) de taille (m + 1, n + m + 1).

    def __init__(self, a, b, c, v=0):
        
        if not all(isinstance(i, np.ndarray) for i in (a, b, c)):
            raise TypeError("Arguments of numpy type array expected")
        # On teste si on a les bonnes dimensions
        if a.shape != (b.shape[0], c.shape[0]):
            raise TypeError("Arguments are not of coherent dimensions")
        # On récupère les m et n à partir de la dimension de la matrice a 
        m, n = a.shape
        self.shape = (m,n)
        self.basic_vars={} # Le dictionnaire est vide au départ
        # Remplissage du dictionnaire  
        for i in range(self.shape[0]):
            self.basic_vars[i]= self.shape[1]+i
        
        # On construit la table taille (m + 1, n + m + 1) initialisée à des zéros
        self.table = np.zeros((m+1, n+m+1), dtype=float)
        self.table[0, :] = np.hstack((-c, np.zeros(self.shape[0], dtype=float), np.array(v)))
        self.table[1:, :] = np.hstack((a, np.eye(self.shape[0], dtype=float), b))
        self.basic_feasible=all(self.basic_sol() >= 0) 
        
        

    def basic_feasible_(self):
        return self.basic_feasible
    def basic_vars_(self):
        return basic_vars
    def table_(self):
        return self.table
  
    def basic_sol(self):
        vect = np.zeros(self.shape[0]+self.shape[1], dtype=float)
        for i in range(self.shape[0]):
            vect[self.basic_vars[i]] = self.table[i+1, -1]
        return vect
        
    
    def pivot(self,e,s):
        if (e not in self.basic_vars.values() and s in self.basic_vars.values())==False :
     
            raise TypeError("Error")
        
        a = self.table
        k=[c for c,v in self.basic_vars.items() if v==s][0]
        
        pivot = a[k+1, e]

        if pivot == 0:
            raise ValueError("Cannot pivot with given leaving and entering variables.")

        a[k+1, :] = a[k+1, :]/pivot

        for i in range(self.shape[0]):
            if i != k:
                a[i+1, :] = a[i+1, :] - a[i+1,e]*a[k+1, :]
        
        a[0, :] = a[0, :] - a[0, e]*a[k+1, :]
                

        self.basic_vars[k] = e
        
   
    
    def dual(self):
        
        a1=self.table[1:,:self.shape[1]].transpose()
        b1=self.table[0,:self.shape[1]].reshape((self.shape[1],1))
        c1=self.table[1:,-1]
        lp = LP(-a1,-b1, c1)
        return lp
        
        
        
    
        
    
    
   
        
    
          
    
        
 
        
    
    
        
       
       

    