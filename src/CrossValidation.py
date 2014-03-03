'''
Created on Feb 9, 2014

@author: Jas
'''
from scipy import optimize
from sage.all import *

def drange(L, A):
    L.sort()
    i = 0
    iMax = len(L)
    r = L[i]
    while r < A:
        i += 1
        r = L[i]
    i -= 1
    return [L[j] for j in range(i,iMax)]
        
def EigenInverse(Q,La, L,M):
    '''
    InputsL
    Q - Eigenvector Matrix -> eigenmatrix_right()
    La - diagonal matrix of eigenvalues -> eigenmatrix_right()
    L - lambda
    M - Size of Q
    Description:
    generates G inverse
    Ginv i,j = sum_{k=1}^M (Q_ik * Q_jk)/(La_kk + L)
    See "notes on regularized least squares" page 5
    '''
    doubleArray = [[sum([(Q[i,k]*Q[j,k])/(La[k,k] + L) for k in range(M)]) for i in range(M)   ] for j in range(M)  ]
    return matrix(doubleArray)
def RKHSN1(a,b,x,y,tau):
    return (tau / sinh(tau * (b - a))) * (cosh(tau*(b - max([x,y])))) * (cosh(tau*(min([x,y])-a)))
def bb(a1,a2,b1,b2,z):
    return a1 * exp(a2 * sqrt(2)*z / 2) * cos(sqrt(2)*z / 2) + b1 * exp(b2 * sqrt(2)*z / 2) * sin(sqrt(2)*z / 2)
def delta(tau):
    return tau * sqrt(2)/(16*(sin(tau * sqrt(2)/2)*sin(tau * sqrt(2)/2) - sinh(tau * sqrt(2)/2)*sinh(tau * sqrt(2)/2)))
def L(tau,a1,b1,a2,b2,a3,b3,a4,a5):
    return (delta(tau)  * (tau * sqrt(2) + a2 * sin(b2 * tau * sqrt(2) ) + a3 * exp(b3 * tau * sqrt(2) + a5) + a4))
def RKHSN2(x,y,tau):
    return L(tau,-1, 1, 1, 1, 3,-1, 0,-2) * bb(1 ,1 ,0 ,0 ,tau*min([x,y]))*bb(1 ,1 ,0 ,0 ,tau*max([x,y]))+L(tau,-1, 1,-1, 1, 1,-1, 0, 0) * bb(1 ,1 ,0 ,0 ,tau*min([x,y]))*bb(0 ,0 ,1 ,1 ,tau*max([x,y]))+L(tau,-1, 1, 3, 1,-1, 1, 0, 2) * bb(1 ,1 ,0 ,0 ,tau*min([x,y]))*bb(1 ,-1,0 ,0 ,tau*max([x,y]))+L(tau,-3, 1,-1, 1,-1, 1, 0, 4) * bb(1 ,1 ,0 ,0 ,tau*min([x,y]))*bb(0 ,0 ,1 ,-1,tau*max([x,y]))+L(tau,-1, 1,-1, 1, 1,-1, 0, 0) * bb(0 ,0 ,1 ,1 ,tau*min([x,y]))*bb(1 ,1 ,0 ,0 ,tau*max([x,y]))+L(tau, 1, 1,-1, 1, 1,-1, 0,-2) * bb(0 ,0 ,1 ,1 ,tau*min([x,y]))*bb(0 ,0 ,1 ,1 ,tau*max([x,y]))+L(tau,-1, 1, 1, 1, 1, 1, 0, 0) * bb(0 ,0 ,1 ,1 ,tau*min([x,y]))*bb(1 ,-1,0 ,0 ,tau*max([x,y]))+L(tau,-1, 1,-1, 1,-1, 1, 0, 2) * bb(0 ,0 ,1 ,1 ,tau*min([x,y]))*bb(0 ,0 ,1 ,-1,tau*max([x,y]))+L(tau,-1, 1, 3, 1,-1, 1,-sqrt(2)/4, 2) * bb(1 ,-1,0 ,0 ,tau*min([x,y]))*bb(1 ,1 ,0 ,0 ,tau*max([x,y]))+L(tau,-1, 1, 1, 1, 1, 1, sqrt(2)/4, 0) * bb(1 ,-1,0 ,0 ,tau*min([x,y]))*bb(0 ,0 ,1 ,1 ,tau*max([x,y]))+L(tau, 1, 1, 1, 1,-3, 1, 0, 2) * bb(1 ,-1,0 ,0 ,tau*min([x,y]))*bb(1 ,-1,0 ,0 ,tau*max([x,y]))+L(tau,-1, 1, 1, 1, 1, 1, 0, 0) * bb(1 ,-1,0 ,0 ,tau*min([x,y]))*bb(0 ,0 ,1 ,-1,tau*max([x,y]))+L(tau,-3, 1,-1, 1,-1, 1,-sqrt(2)/4, 4) * bb(0 ,0 ,1 ,-1,tau*min([x,y]))*bb(1 ,1 ,0 ,0 ,tau*max([x,y]))+L(tau,-1, 1,-1, 1,-1, 1,-sqrt(2)/4, 2) * bb(0 ,0 ,1 ,-1,tau*min([x,y]))*bb(0 ,0 ,1 ,1 ,tau*max([x,y]))+L(tau,-1, 1, 1, 1, 1, 1, 0, 0) * bb(0 ,0 ,1 ,-1,tau*min([x,y]))*bb(1 ,-1,0 ,0 ,tau*max([x,y]))+L(tau,-1, 1,-1, 1,-1, 1, 0, 2) * bb(0 ,0 ,1 ,-1,tau*min([x,y]))*bb(0 ,0 ,1 ,-1,tau*max([x,y]))
def RKHSM(en,m,x,y):
    return en*en * max([x,y])**(-m-1) * integrate(x**m * (1-x)**(en-1) * (1-(min([x,y])/max([x,y]))*x)**(en-1),x,0,1)   
def RKHSMN1(m):
    return (1/(m+1))
def RKHSMN2(m,x,y):
    z = min([x,y])/max([x,y])
    return RKHSMN1(m) - z * RKHSMN1(m+1) - RKHSMN1(m+1) + z * RKHSMN1(m+2)
class CrossValidationParams:
    def GetQArray(self):
        raise NotImplementedError("Implement in child class")
    def LOOEGenerator(self): 
        '''
        description: creates the eigenvectors and diagonal matrix of eigenvalues for each matrix
        '''
        M = self.gridSize
        identityMatrix = matrix.identity(M)
        looeList = list()
        for L in self.lambdas:
            for Q in self.QN:
                G = Q[0] + L * identityMatrix
                diagonalEigenvalues, eigenvectorMatrix = G.eigenmatrix_right()
                gInverse = EigenInverse(eigenvectorMatrix,diagonalEigenvalues,L,M)
                c = gInverse * self.Y
                D = gInverse.diagonal()
                LOOE = vector([c[i]/D[i] for i in range(len(c))])
                looeList.append((L,Q,LOOE.norm(),c))
        sortedLooeList = sorted(looeList,key=lambda d: d[2])
        return sortedLooeList
    
    def __init__(self,FZ,tauMin,tauMax,lambdaMin,lambdaMax,lambdaStepSize):
        if FZ.StockPrices == None:
            pass
        else:
            self.a = FZ.minPrice
            self.b = FZ.maxPrice
            self.gridPoints = FZ.GetGridInverseStandardDeviation()
            self.X = vector([P[0] for P in self.gridPoints])
            self.Y = vector([P[1] for P in self.gridPoints])
            self.gridSize = len(self.gridPoints)
            self.taus = range(1,6)#1,2,...,9
            self.lambdas = srange(.1,12,.75)
            self.QN = self.GetQArray()#[(matrix(QQ, self.gridSize, self.gridSize,lambda i,j: RKHSN2(self.gridPoints[i],self.gridPoints[j],tau)),tau) for tau in self.taus]
            self.looeListSorted= self.LOOEGenerator()
            self.L = self.looeListSorted[0][0]
            self.tau = self.looeListSorted[0][1][1]
            self.ChosenRKHS = self.looeListSorted[0][1][0]
            self.c = self.looeListSorted[0][3] #needs to evaluate this with RKHSN2(self.a,self.b,self.gridPoints[i],X,tau) for any X to become an estimator
            

class CrossValidationRKHSN2(CrossValidationParams):
    '''
    This allows us to perform Leave-One-Out Cross Validation over
    RKHSN2
    '''
    def GetQArray(self):
        return [(matrix(QQ, self.gridSize, self.gridSize,lambda i,j: RKHSN2(self.X[i],self.X[j],tau)),tau) for tau in self.taus]
    
    def __init__(self,FZ):
        '''
        Constructor
        Input:
        Floren Zmirou Estimator - FZ
        Description:
        1) Performs LOOE over RKHSN2 on FZ  
        '''
        CrossValidationParams.__init__(self, FZ, 1, 6, .1, 12, .75)
        
        
class CrossValidationRKHSN1(CrossValidationParams):
    '''
    This allows us to perform Leave-One-Out Cross Validation over
    RKHSN1
    '''
    def GetQArray(self):
        return [(matrix(QQ, self.gridSize, self.gridSize, lambda i,j: RKHSN1(self.a,self.b,self.X[i],self.X[j],tau)),tau) for tau in self.taus]
    def __init__(self, FZ):
        '''
        Constructor
        Input:
        Floren Zmirou Estimator - FZ
        Description:
        1) Performs LOOE over RKHSN1 on FZ  
        '''
        CrossValidationParams.__init__(self, FZ, 1, 10, .1, 10, .75)

class CrossValidationRKHSM(CrossValidationParams):
    '''
    This allows us to perform Leave-One-Out Cross Validation over
    RKHSM.  However we're not sorting on min ||LOOE(RKHSM)||  we are sorting on Argmin sqrt(int(sigma_m - sigma^b))
    '''
    def GetQArray(self):
        return [(matrix(QQ, self.gridSize, self.gridSize, lambda i,j: RKHSM(2,m,self.X[i],self.X[j])),m) for m in self.ems]
    def __init__(self,FZ):
        '''
        Constructor
        Input:
        Floren Zmirou Estimator - FZ
        Description:
        1) Performs LOOE over RKHSM on FZ  
        '''
        self.ems = srange(.1,10,.1) 
        CrossValidationParams.__init__(self, FZ, 1, 2, 1, 2, 1) #the last 5 entries are not important for RKHSM
        
class ExtrapolationOptimizationTestN2(CrossValidationRKHSN2):
    def GetQArrayM(self):
        return [(matrix(QQ, self.gridSize, self.gridSize, lambda i,j: RKHSMN2(m,self.X[i],self.X[j])),m) for m in self.ems]
    def LOOEGeneratorRKHSM(self): 
        '''
        description: creates the eigenvectors and diagonal matrix of eigenvalues for each matrix
        '''
        M = self.gridSize
        identityMatrix = matrix.identity(M)
        looeList = list()
        for L in self.lambdas:
            for Q in self.QM:
                G = Q[0] + L * identityMatrix
                diagonalEigenvalues, eigenvectorMatrix = G.eigenmatrix_right()
                gInverse = EigenInverse(eigenvectorMatrix,diagonalEigenvalues,L,M)
                c = gInverse * self.Y
                D = gInverse.diagonal()
                LOOE = vector([c[i]/D[i] for i in range(len(c))])
                looeList.append((L,Q,LOOE.norm(),c,Q[1]))#Q[1] = m
    def TrapezoidRule(self,f,a,b):
        '''
        domainPoints = the set of points in usableGridPoints in the range of [a,b] union (the previous grid point befor a)
        
        '''
        domainPoints = drange(self.gridPoints,a)
        domainPoints.sort()
        xDeltas = vector([(domainPoints[i+1] - domainPoints[i]) for i in range(len(domainPoints)-1)])
        fDeltas = vector([(f(domainPoints[i+1]) - f(domainPoints[i])) for i in range(len(domainPoints)-1)])
        return (1.0/2.0) * xDeltas.dot_product(fDeltas)
    
    def __init__(self,FZ):
        '''
        step 1:  Compute sigma_b
        step 2:  Compute sigma_m's
        step 3:  for each sigma_m:  
                    compute/add to list (m, square_root(integral(|sigma_m - sigma_b|^2)))
        step 4:  sort list in step 3 by smallest square_root(integral(|sigma_m - sigma_b|^2))
        step 5:  return m of step 4.
        '''
        CrossValidationRKHSN2.__init__(self, FZ)#step 1
        #Step 2 - Compute sigma_m's
        self.ems = srange(.1,12,.75)
        self.QM = self.GetQArrayM()
        self.looeListM= self.LOOEGeneratorRKHSM()
        #step 3.1
        resultantList = list()
        aye = self.b - (1.0/3.0) * (self.b - self.a)
        sigma_b = lambda x: 1/sqrt(self.c.dot_product(vector([RKHSN2(ex,x,self.tau) for ex in self.X])))
        for looeItem in self.looeListM:
            '''
            ----Does not need to be done in the for loop---- step 3.1
            step    -3: resultantList = list()
            step    -2: aye = self.b  - (1.0/3.0) * (self.b - self.a) 
            Remark   1: self.c = c_b for f_b 
            step     2: sigma_b(x) = 1/sqrt(self.c.dot_product(vector([RKHSN2(ex,x,self.tau) for ex in self.X])))
            ----Does not need to be done in the for loop----
            ----Needs to be done in the for loop---- step 3.2
            step    -1: m = looeItem[4]
            step     0: cM = looeItem[3]
            step     3: sigma_m(x) = 1/sqrt(cM.dot_product(vector([RKHSM(2,m,ex,x) for ex in self.X])))
            step     4: f(x) = abs(sigma_m(x) - sigma_b(x))^2
            step     5: area <- Trapezoid Rule over aye to maxS on f(x)
            step     6: add to resultantList (m,cM,area)
            ----Needs to be done in the for loop----
            ----Does not need to be done in the for loop---- step 3.3
            step     7: sort resultantList by area
            ----Does not need to be done in the for loop----
            '''
            m = looeItem[4]
            cM = looeItem[3]
            sigma_m = lambda x: 1/sqrt(cM.dot_product(vector([RKHSMN2(m,ex,x) for ex in self.X])))
            f = lambda x: abs(sigma_m(x) - sigma_b(x))**2
            area = self.TrapezoidRule(f,aye,self.b)
            resultantList.append((m,cM,sigma_m,area))
        self.sortedResultantList = sorted(resultantList,key=lambda result: result[0])

class ExtrapolationOptimizationTestN1(CrossValidationRKHSN1):
    def GetQArrayM(self):
        return [(matrix(QQ, self.gridSize, self.gridSize, lambda i,j: RKHSMN1(m)),m) for m in self.ems]
    def LOOEGeneratorRKHSM(self): 
        '''
        description: creates the eigenvectors and diagonal matrix of eigenvalues for each matrix
        '''
        M = self.gridSize
        identityMatrix = matrix.identity(M)
        looeList = list()
        for L in self.lambdas:
            for Q in self.QM:
                G = Q[0] + L * identityMatrix
                diagonalEigenvalues, eigenvectorMatrix = G.eigenmatrix_right()
                gInverse = EigenInverse(eigenvectorMatrix,diagonalEigenvalues,L,M)
                c = gInverse * self.Y
                D = gInverse.diagonal()
                LOOE = vector([c[i]/D[i] for i in range(len(c))])
                looeList.append((L,Q,LOOE.norm(),c,Q[1]))#Q[1] = m
        return looeList
    
    def TrapezoidRule(self,f,a,b):
        '''
        domainPoints = the set of points in usableGridPoints in the range of [a,b] union (the previous grid point befor a)
        
        '''
        domainPoints = drange(self.X.list(),a)
        domainPoints.sort()
        xDeltas = vector([(domainPoints[i+1] - domainPoints[i]) for i in range(len(domainPoints)-1)])
        fDeltas = vector([(f(domainPoints[i+1]) - f(domainPoints[i])) for i in range(len(domainPoints)-1)])
        return (1.0/2.0) * xDeltas.dot_product(fDeltas)
    
    def __init__(self,FZ):
        '''
        step 1:  Compute sigma_b
        step 2:  Compute sigma_m's
        step 3:  for each sigma_m:  
                    compute/add to list (m, square_root(integral(|sigma_m - sigma_b|^2)))
        step 4:  sort list in step 3 by smallest square_root(integral(|sigma_m - sigma_b|^2))
        step 5:  return m of step 4.
        '''
        CrossValidationRKHSN1.__init__(self, FZ)#step 1
        #Step 2 - Compute sigma_m's
        self.ems = srange(.1,12,.75)
        self.QM = self.GetQArrayM()
        self.looeListM= self.LOOEGeneratorRKHSM()
        #step 3.1
        resultantList = list()
        aye = self.b - (1.0/3.0) * (self.b - self.a)
        sigma_b = lambda x: 1/sqrt(self.c.dot_product(vector([RKHSN2(ex,x,self.tau) for ex in self.X])))
        if self.looeListM is not None:
            for looeItem in self.looeListM:
                '''
                ----Does not need to be done in the for loop---- step 3.1
                step    -3: resultantList = list()
                step    -2: aye = self.b  - (1.0/3.0) * (self.b - self.a) 
                Remark   1: self.c = c_b for f_b 
                step     2: sigma_b(x) = 1/sqrt(self.c.dot_product(vector([RKHSN2(ex,x,self.tau) for ex in self.X])))
                ----Does not need to be done in the for loop----
                ----Needs to be done in the for loop---- step 3.2
                step    -1: m = looeItem[4]
                step     0: cM = looeItem[3]
                step     3: sigma_m(x) = 1/sqrt(cM.dot_product(vector([RKHSM(2,m,ex,x) for ex in self.X])))
                step     4: f(x) = abs(sigma_m(x) - sigma_b(x))^2
                step     5: area <- Trapezoid Rule over aye to maxS on f(x)
                step     6: add to resultantList (m,cM,area)
                ----Needs to be done in the for loop----
                ----Does not need to be done in the for loop---- step 3.3
                step     7: sort resultantList by area
                ----Does not need to be done in the for loop----
                '''
                m = looeItem[4]
                cM = looeItem[3]
                sigma_m = lambda x: 1/sqrt(cM.dot_product(vector([RKHSMN1(m) for ex in self.X])))
                f = lambda x: abs(sigma_m(x) - sigma_b(x))**2
                area = self.TrapezoidRule(f,aye,self.b)
                resultantList.append((m,cM,sigma_m,area))
            self.sortedResultantList = sorted(resultantList,key=lambda result: result[0])
            