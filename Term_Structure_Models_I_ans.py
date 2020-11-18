from term_structure_lattice_model import TSLM

dict_params= {'r0':0.05, 'u':1.1, 'd':0.9, 'q':0.5, 'maturity':10,'face_value':100}      
test_params = {'r0':0.06, 'u':1.25, 'd':0.9, 'q':0.5, 'maturity':5,'face_value':100}
def q1():
    #test = TSLM(0.06,1.25,0.9,0.5,4,100)
    test = TSLM(**dict_params)
    return test.zcb_price()
    #return test.zcb_price() 
q1_ans = q1()
print('q1',q1_ans)


def forward_on_zcb(forward_maturity):
    top = TSLM(**dict_params).zcb_price()
    bot = TSLM(0.05,1.1,0.9,0.5,forward_maturity,1).zcb_price()
    return top/bot

def q2():
    return forward_on_zcb(4)
print('q2',q2())

def q3():
    model = TSLM(**dict_params)
    return model.future_zcb_price(4)
print('q3',q3())
#74.82

def q4():
    model = TSLM(**dict_params)
    return model.us_call_zcb_price(6,80)
print('q4',q4())
#2.36

def q5():
    model = TSLM(**dict_params)
    return model.swap_price(1,0.045,1000000)
print('q5',q5())
#33374

def q6():
    model = TSLM(**dict_params)
    return model.swaption_price(1,0.045,5,0,1000000)
print('q6',q6())

