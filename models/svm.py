'''
Created on 19. mars 2014

@author: JohnArne
'''
from model import Model

class SVM(Model):
    """
    Class implementing the Support Vector Machines classsification model.
    """
    
    def __init__(self):
        self.weights = []
        
        