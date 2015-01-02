'''
Created on 19. mars 2014

@author: JohnArne
'''
from model import Model
from sklearn.linear_model import LogisticRegression

class ME(Model):
    """
    Subclass implementing the Maximum entropy classification model.
    """
    def __init__(self, tweets_train, tweets_targets, vect_options):
        self.classifier = LogisticRegression()
        extra_params = {'clf__C': (0.1, 0.3, 0.5, 0.7, 0.8, 1.0,),'clf__penalty': ('l1', 'l2')}
        super(ME, self).__init__(tweets_train, tweets_targets, vect_options, extra_params)