import sys
#sys.path.append("/home/jolly/MyPython") 

from fcm.statistics import DPMixtureModel, DPMixture
import unittest
from numpy import array, eye, all
import numpy as np
import numpy.random as npr
from numpy.random import multivariate_normal
from fcm.statistics.dp_cluster import DPMixture
from time import time

gen_mean = {
    0 : [0, 5],
    1 : [-5, 0],
    2 : [5,0]
}

gen_sd = {
    0 : [0.5, 0.5],
    1 : [.5, 1],
    2 : [1, .25]
}

gen_corr = {
    0 : 0.5,
    1 : -0.5,
    2 : 0
}

group_weights = [0.4, 0.3, 0.3]

#gen_mean = {
#    0 : [0, 5],
#    1 : [-10, 0],
#    2 : [-10, 10]
#}
#
#gen_sd = {
#    0 : [0.5, 0.5],
#    1 : [.5, 1],
#    2 : [1, .25]
#}
#
#gen_corr = {
#    0 : 0.5,
#    1 : -0.5,
#    2 : 0
#}
#
#group_weights = [0.6, 0.3, 0.1]

class DPMixtureModel_TestCase(unittest.TestCase):
    def generate_data(self,n=1e4, k=2, ncomps=3, seed=1):
        
        npr.seed(seed)
        data_concat = []
        labels_concat = []
    
        for j in xrange(ncomps):
            mean = gen_mean[j]
            sd = gen_sd[j]
            corr = gen_corr[j]
    
            cov = np.empty((k, k))
            cov.fill(corr)
            cov[np.diag_indices(k)] = 1
            cov *= np.outer(sd, sd)
    
            num = int(n * group_weights[j])
            rvs = multivariate_normal(mean, cov, size=num)
    
            data_concat.append(rvs)
            labels_concat.append(np.repeat(j, num))
    
        return (np.concatenate(labels_concat),
                np.concatenate(data_concat, axis=0))

    def testBEMFitting(self):
        print 'starting BEM'
        true, data = self.generate_data()
        m = data.mean(0)
        s = data.std(0)
#        true_mean = {}
#        for i in gen_mean:
#            true_mean[i] = (gen_mean[i]-m)/s
        
        model = DPMixtureModel(3,2000,100,1, type='BEM')
        model.seed = 1
        start = time()
        r = model.fit(data, verbose=False)
        print 'r', r.mus()
        end = time() - start
        
        diffs = {}
        for i in gen_mean:
            diffs[i] = np.min(np.abs(r.mus()-gen_mean[i]),0)
            #print i, gen_mean[i], diffs[i], np.vdot(diffs[i],diffs[i])
            assert( np.vdot(diffs[i],diffs[i]) < 1)
        print 'BEM fitting took %0.3f' % (end)
#        
    def testMCMCFitting(self):
        print "starting mcmc"
        true, data = self.generate_data()
        m = data.mean(0)
        s = data.std(0)
#        true_mean = {}
#        for i in gen_mean:
#            true_mean[i] = (gen_mean[i]-m)/s
        
        model = DPMixtureModel(3,100,100,1)
        model.seed = 1
        start = time()
        r = model.fit(data, verbose=10)
        end = time() - start
        
        diffs = {}
        #print 'r.mus:', r.mus()
        for i in gen_mean:
            diffs[i] = np.min(np.abs(r.mus()-gen_mean[i]),0)
            #print i, gen_mean[i], diffs[i], np.vdot(diffs[i],diffs[i])
            assert( np.vdot(diffs[i],diffs[i]) < 1)
        #print diffs
        print 'MCMC fitting took %0.3f' % (end)
        
    def testRefernce(self):
        print "starting mcmc"
        true, data = self.generate_data()
        m = data.mean(0)
        s = data.std(0)
#        true_mean = {}
#        for i in gen_mean:
#            true_mean[i] = (gen_mean[i]-m)/s
        
        model = DPMixtureModel(3,100,100,1)
        model.seed = 1
        model.load_ref(array(true))
        start = time()
        r = model.fit(data, verbose=True)
        end = time() - start
        
        diffs = {}
        #print 'r.mus:', r.mus()
        for i in gen_mean:
            #diffs[i] = np.min(np.abs(r.mus()-gen_mean[i]),0)
            diffs[i] = np.abs(r.mus()[i]-gen_mean[i])
            #print i, gen_mean[i],r.mus()[i], diffs[i], np.vdot(diffs[i],diffs[i])
            assert( np.vdot(diffs[i],diffs[i]) < 1)
        #print diffs
        print 'MCMC fitting took %0.3f' % (end)
        
        model.load_ref(r)
        start = time()
        r = model.fit(data, verbose=True)
        end = time() - start
        
        diffs = {}
        #print 'r.mus:', r.mus()
        for i in gen_mean:
            #diffs[i] = np.min(np.abs(r.mus()-gen_mean[i]),0)
            diffs[i] = np.abs(r.mus()[i]-gen_mean[i])
            #print i, gen_mean[i],r.mus()[i], diffs[i], np.vdot(diffs[i],diffs[i])
            assert( np.vdot(diffs[i],diffs[i]) < 1)
        #print diffs
        
    def setUp(self):
        self.mu = array([0,0])
        self.sig = eye(2)
        self.pnts = multivariate_normal(self.mu, self.sig, 1000)
        self.k = 16
        self.niter = 10
        self.model = DPMixtureModel(self.k,self.niter,0,1)
        

    def testModel(self):
        r = self.model.fit(self.pnts, verbose=False)
        assert(isinstance(r, DPMixture))
        mus = r.mus()
        assert(mus.shape == (16,2))
        
    def testModel_prior(self):
        self.model.load_mu(self.mu.reshape(1,2))
        self.model.load_sigma(self.sig.reshape(1,2,2))
        r = self.model.fit(self.pnts, verbose=False)
        assert(isinstance(r, DPMixture))
        mus = r.mus()
        assert(mus.shape == (16,2))
        
if __name__ == '__main__':
    unittest.main()