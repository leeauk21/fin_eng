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

    def future_zcb_price(self,future_maturity):
        arr = [self.zcb_price_lattice()[future_maturity]]
        for i in range(0,future_maturity):
            arr_to_add=[]
            for j in range(len(arr[i])-1):
                a = arr[i][j] + arr[i][j+1]
                a /= 2
                arr_to_add.append(a)
            arr.append(arr_to_add)
        return arr[::-1][0][0]


    def us_call_zcb_price(self,expire_t,strike):
        r = self.gen_short_rate_lattice()[0:expire_t+1][::-1]
        arr = self.zcb_price_lattice()[0:expire_t+1][::-1]
        res = []
        for i in range(len(arr)):
            res_to_add = []
            for j in range(len(arr[i])):
                if i == 0:
                    res_to_add.append(max(arr[i][j]-strike,0))
                else:
                    a = self.risk_neutral_price(r[i][j],res[i-1][j],res[i-1][j+1])
                    res_to_add.append(max(arr[i][j]-strike,a))
            res.append(res_to_add)
        return res[::-1][0][0]





            




dict_params= {'r0':0.05, 'u':1.1, 'd':0.9, 'q':0.5, 'maturity':10,'face_value':100}      
test_params = {'r0':0.06, 'u':1.25, 'd':0.9, 'q':0.5, 'maturity':4,'face_value':100}
def q1():
    #test = TSLM(0.06,1.25,0.9,0.5,4,100)
    test = TSLM(**dict_params)
    return test.zcb_price()
    #return test.zcb_price() 
#q1_ans = q1()
#print(q1_ans)


def forward_on_zcb(forward_maturity):
    top = TSLM(**dict_params).zcb_price()
    bot = TSLM(0.05,1.1,0.9,0.5,forward_maturity,1).zcb_price()
    return top/bot

def q2():
    return forward_on_zcb(4)
#print(q2())

def q3():
    model = TSLM(**dict_params)
    return model.future_zcb_price(4)
#print(q3())
#74.82

def q4():
    model = TSLM(**dict_params)
    return model.us_call_zcb_price(6,80)
#print(q4())
#2.36








    








