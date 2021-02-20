
# Adapted from:
#https://github.com/vt-ece4530-f17/challenge-ece4530-f17-0/blob/master/challenge.pdf
import numpy as np
import multiprocessing as mp
import time
import random

class MyCorrelator:
    def __init__(self, maxCores):
        #FIXME:  update this once you can support multiple threads
        self.maxCores = maxCores
        

    def myCorrelate(self,  ref, search):
        cor = [0] * ( 1 + len(search) - len(ref))
        for i in range(0, 1 + len(search) - len(ref)):
            for j in range(0, len(ref)):
                cor[i] = cor[i] + ref[j] * search[ (i+j) % len(search) ]
        return cor

    def peakDetect(self, search):
        maxVal=-1
        maxIdx = -1

        for idx,val in enumerate(search):
            if val > maxVal:
                maxVal = val
                maxIdx = idx

        return maxIdx

    
    def new_bulk_peakDetect(self, references, all_searches, i, q):
        all_maxIds = []
        for ridx,reference in enumerate(references):
            ref_maxIds = []
            for search in all_searches[ridx]:
                cor = self.myCorrelate(reference,search)
                maxIdx = self.peakDetect(cor)
                ref_maxIds.append(maxIdx)
            all_maxIds.append(ref_maxIds)
        q.put([i, all_maxIds])
        return   
    def bulk_peakDetect( self, references, all_searches):
        ctx = mp.get_context('fork')
        q = ctx.Queue()
        processval = []
        all_maxIds = []
        c = [None]*self.maxCores
        references = np.array_split(references, self.maxCores)
        all_searches = np.array_split(all_searches, self.maxCores)
        for i in range(self.maxCores):
            processval += [ctx.Process(target=self.new_bulk_peakDetect, args=(references[i],all_searches[i],i,q))]
        for i in processval:
            i.start()
        for i in range(self.maxCores):
            ret = q.get()
            c[ret[0]] = ret[1]
        for i in c:
            all_maxIds += i
        for i in processval:
            i.join()
        return all_maxIds

    