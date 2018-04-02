import sys
from PyQt4 import QtGui


class Model(object):
    def __init__(self):
        self._update_funcs=[]
        # variable placeholders
        self.running = False
        self.changedValue=0
        #generate Transferred virtual Channel 0-3 BER label and assign init value  e.g. self.ch0BER
        berNameGeneration = ["self.ch" + str(x) + "BER" for x in range(4)]
        berinitValue = [0] * len(berNameGeneration)
        berNameDictionary = {k: v for k, v in zip(berNameGeneration, berinitValue)}
        # assign init value to widget
        for name in berNameDictionary.keys():
            exec(name+'='+ str(berNameDictionary[name]))
        ##############*******************************************************************
        # generate Channel 0-3 Error label and assign init value  e.g. self.Ch1totalError
        ErrorNameGeneration = ["self.Ch" + str(x) + "totalError" for x in range(4)]
        ErrinitValue = [0] * len(ErrorNameGeneration)
        errNameDictionary = {k: v for k, v in zip(ErrorNameGeneration, ErrinitValue)}

        self.timeElapsed=0
        # assign init value to widget
        for name in errNameDictionary.keys():
            exec (name + '=' + str(errNameDictionary[name]))
        self.transmittedBits=0


    # subscribe a view method for updating, subscribe by view
    def subscribe_update_func(self, func):
        if func not in self._update_funcs:
            self._update_funcs.append(func)

    # unsubscribe a view method for updating
    def unsubscribe_update_func(self, func):
        if func in self._update_funcs:
            self._update_funcs.remove(func)

    # update registered view methods
    def announce_update(self):
        for func in self._update_funcs:
            func()




if __name__ == '__main__':
     pass