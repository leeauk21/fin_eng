import math
import numpy as np


class bs_bin_tree:

    def __init__(self,T,s0,r,sigma,c,K,n):
        self.T = T
        self.r = r
        self.c = c
        self.sigma = sigma
        self.K = K
        self.s0 = s0
        self.n = n
        self.u = math.exp(self.sigma*np.sqrt(self.T/self.n))
        self.q = (math.exp((self.r-self.c)*T/self.n)-(1/self.u))/(self.u-(1/self.u))
        self.R = math.exp(self.r*self.T/self.n)
        self.__print_param__()

    def __print_param__(self):
        print('Time',self.T)
        print('Starting Price',self.s0)
        print('r',self.r)
        print('volatility',self.sigma)
        print('dividend yield',self.c)
        print('strike',self.K)
        print('# period',self.n)
        
    
    def generate_price(self):
        arr=[[self.s0]]
        for i in range(self.n):
            arr_to_add=[]
            for j in range(len(arr[i])):
                arr_to_add.append(arr[i][j]/self.u)
                if j == (len(arr[i])-1):
                    arr_to_add.append(arr[i][j]*self.u)
            arr.append(arr_to_add)
        return arr

    def neutral_pricing(self,p1,p2):
        price = ((1-self.q)*p1 + (self.q)*p2)/self.R
        return price

    def eu_put(self):
        arr = self.generate_price()
        arr_rev = arr[::-1]
        res=[]
        for i in range(len(arr_rev)):
            res_to_add = []
            for j in range(len(arr_rev[i])):
                if i == 0:
                    a = max(self.K-arr_rev[i][j],0)
                    res_to_add.append(a)
                else:
                    price = self.neutral_pricing(res[i-1][j], res[i-1][j+1])
                    #a = max(arr_rev[i][j]-strike,0)
                    #a = max(a,price)
                    a = price
                    res_to_add.append(a)
                
            res.append(res_to_add)
        return res[::-1]

    def eu_call(self):
        arr = self.generate_price()
        arr_rev = arr[::-1]
        res=[]
        for i in range(len(arr_rev)):
            res_to_add = []
            for j in range(len(arr_rev[i])):
                if i == 0:
                    a = max(arr_rev[i][j]-self.K,0)
                    res_to_add.append(a)
                else:
                    price = self.neutral_pricing(res[i-1][j], res[i-1][j+1])
                    #a = max(arr_rev[i][j]-strike,0)
                    #a = max(a,price)
                    a = price
                    res_to_add.append(a)
                
            res.append(res_to_add)
        return res[::-1]

    def us_call(self):
        arr = self.generate_price()
        arr_rev = arr[::-1]
        res=[]
        for i in range(len(arr_rev)):
            res_to_add = []
            for j in range(len(arr_rev[i])):
                if i == 0:
                    a = max(arr_rev[i][j]-self.K,0)
                    res_to_add.append(a)
                else:
                    price = self.neutral_pricing(res[i-1][j], res[i-1][j+1])
                    a1 = max(arr_rev[i][j]-self.K,0)
                    a = max(a1,price)
                    res_to_add.append(a)
                
            res.append(res_to_add)
        return res[::-1]

    def us_call_price(self):
        return self.us_call()[0][0]

    def us_put(self):
        arr = self.generate_price()
        arr_rev = arr[::-1]
        res=[]
        for i in range(len(arr_rev)):
            res_to_add = []
            for j in range(len(arr_rev[i])):
                if i == 0:
                    a = max(self.K-arr_rev[i][j],0)
                    res_to_add.append(a)
                else:
                    price = self.neutral_pricing(res[i-1][j], res[i-1][j+1])
                    a1 = max(self.K - arr_rev[i][j],0)
                    a = max(a1,price)
                    res_to_add.append(a)
                
            res.append(res_to_add)
        return res[::-1]

    def us_put_price(self):
        return self.us_put()[0][0]

    def us_put_early_ex(self):
        early_ex = False
        early_ex_earning = 0
        early_ex_time = self.n
        arr = self.generate_price()
        arr_rev = arr[::-1]
        res=[]
        for i in range(len(arr_rev)):
            res_to_add = []
            for j in range(len(arr_rev[i])):
                if i == 0:
                    a = max(self.K-arr_rev[i][j],0)
                    res_to_add.append(a)
                else:
                    price = self.neutral_pricing(res[i-1][j], res[i-1][j+1])
                    a1 = max(self.K-arr_rev[i][j],0)
                    if a1 > price:
                        if early_ex_time == self.n - i:
                            early_ex_earning = max(early_ex_earning,a1)
                        else:
                            early_ex_earning = a1
                        early_ex =True
                        early_ex_time = self.n - i


                    a = max(a1,price)
                    res_to_add.append(a)
                
            res.append(res_to_add)
        return {early_ex_time:early_ex_earning} if early_ex == True else False

    def us_put_call_parity(self):
        LHS = self.us_put_price() + self.s0 * math.exp(-self.c * self.T)
        RHS = self.us_call_price() + self.K * math.exp(-self.r * self.T)
        print('Put Side',LHS)
        print('Call Side',RHS)
        return LHS==RHS

    def generate_future_price(self):
        arr = self.generate_price()
        arr_rev = arr[::-1]
        res=[]
        for i in range(len(arr_rev)):
            res_to_add = []
            for j in range(len(arr_rev[i])):
                if i == 0:
                    res_to_add.append(arr_rev[i][j])
                else:
                    price = self.neutral_pricing(res[i-1][j], res[i-1][j+1])*self.R
                    res_to_add.append(price)
                
            res.append(res_to_add)
        return res[::-1]

    def option_on_future(self,option_maturity):
        arr = self.generate_future_price()[0:option_maturity+1]
        arr_rev = arr[::-1]
        res=[]
        for i in range(option_maturity+1):
            res_to_add = []
            for j in range(len(arr_rev[i])):
                if i == 0:
                    a = max(arr_rev[i][j]-self.K,0)
                    res_to_add.append(a)
                else:
                    price = self.neutral_pricing(res[i-1][j], res[i-1][j+1])
                    a1 = max(arr_rev[i][j]-self.K,0)
                    a = max(a1,price)
                    res_to_add.append(a)
                
            res.append(res_to_add)
        return res[::-1]

    def option_price_on_future(self,option_maturity):
        return self.option_on_future(option_maturity)[0][0]

    def option_on_future_early_ex(self,option_maturity):
        arr = self.generate_future_price()[0:option_maturity+1]
        arr_rev = arr[::-1]
        res=[]
        early_ex = False
        early_ex_earning = 0
        early_ex_time = self.n
        for i in range(option_maturity+1):
            res_to_add = []
            for j in range(len(arr_rev[i])):
                if i == 0:
                    a = max(arr_rev[i][j]-self.K,0)
                    res_to_add.append(a)
                else:
                    price = self.neutral_pricing(res[i-1][j], res[i-1][j+1])
                    a1 = max(arr_rev[i][j]-self.K,0)
                    if a1 > price:
                        if early_ex_time == option_maturity - i:
                            early_ex_earning = max(early_ex_earning,a1)
                        else:
                            early_ex_earning = a1
                        early_ex =True
                        early_ex_time =  len(arr_rev) - i -1


                    a = max(a1,price)
                    res_to_add.append(a)
                
            res.append(res_to_add)
        return {early_ex_time:early_ex_earning} if early_ex == True else False

    def nCr(self,n,r):
        f = math.factorial
        return f(n) / f(r) / f(n-r)
    
    def chooser_option_price(self,option_expire):
        call = self.eu_call()[option_expire]
        put = self.eu_put()[option_expire]
        res=[]
        for i in range(len(call)):
            res.append(max(call[i],put[i]))
        result=0
        for j in range(0,len(res)):
            result += self.nCr(option_expire,j)* (self.q**(j)) * (1-self.q)**(option_expire-j) * res[j]
        return (result/self.R**(option_expire))
