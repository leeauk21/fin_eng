class TSLM:

    def __init__(self, r0, u, d, q, maturity,face_value):
        self.r0 = r0
        self.u = u
        self.q = q
        self.t =maturity
        self.d = d
        self.fv = face_value
        print('r0',self.r0)
        print('u',self.u)
        print('q',self.q)
        print('t',self.t)
        print('d',self.d)
        print('face value', self.fv)

    def gen_short_rate_lattice(self):
        arr = [[self.r0]]
        for i in range(self.t):
            arr_to_add = []
            for j in range(len(arr[i])):
                arr_to_add.append(self.d*arr[i][j])
                if j == (len(arr[i])-1):
                    arr_to_add.append(self.u*arr[i][j])
            arr.append(arr_to_add)
        return arr

    def risk_neutral_price(self,r,p1,p2):
        return ((1-self.q)*p1+self.q*p2)/(1+r)

    def zcb_price_lattice(self):
        arr_rev = self.gen_short_rate_lattice()[::-1]
        arr = []
        for i in range(len(arr_rev)):
            arr_to_add=[]
            for j in range(len(arr_rev[i])):
                if i==0:
                    arr_to_add.append(self.fv)
                else:
                    price = self.risk_neutral_price(arr_rev[i][j],arr[i-1][j],arr[i-1][j+1])
                    arr_to_add.append(price)
            arr.append(arr_to_add)
        return arr[::-1]

    def zcb_price(self):
        return self.zcb_price_lattice()[0][0]



dict_params= {'r0':0.05, 'u':1.1, 'd':0.9, 'q':0.5, 'maturity':10,'face_value':100}      

def q1():
    #test = TSLM(0.06,1.25,0.9,0.5,4,100)
    test = TSLM(**dict_params)
    return test.zcb_price()
    #return test.zcb_price()
q1_ans = q1()
print(q1_ans)




