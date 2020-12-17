
# Adapted from:
#https://github.com/vt-ece4530-f17/challenge-ece4530-f17-0/blob/master/challenge.pdf

class MyCorrelator:
    def __init__(self, maxCores= 1):
        #FIXME:  update this once you can support multiple threads
        assert(maxCores== 1)

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

    def bulk_peakDetect (self, references, all_searches):
        all_maxIds = []
        for ridx,reference in enumerate(references):
            ref_maxIds = []
            for search in all_searches[ridx]:
                cor = self.myCorrelate(reference,search)
                maxIdx = self.peakDetect(cor)
                ref_maxIds.append(maxIdx)
            all_maxIds.append(ref_maxIds)
        return all_maxIds


