'''
Created on 24. nov. 2014

@author: JohnArne
'''
import utils
from models.nb import NB

if __name__ == '__main__':
    nb = NB(utils.get_pickles())
    nb.set_feature_set('A')
    nb.train_on_feature_set()