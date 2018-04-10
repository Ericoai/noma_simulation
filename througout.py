##
import random
import math

##

#
W = 50*(10**6)

#
H = []
i = 0
while i < 10:
    h = random.uniform(-30, -42)
    H.append(h)
    i = i + 1


#user pairing
def pairing(user):
    i = 0
    user_pair = []
    user.sort()
    n = len(user)
    user_weak = user[0:n / 2]
    user_strong = user[n / 2:n]
    #print user_weak
    #print user_strong
    while i < n/2:
        user_pair.append(user_weak[i])
        user_pair.append(user_strong[i])
        i = i + 1
    return user_pair



#n = 2
#print([user_pair[i:i + n] for i in range(0, len(user_pair), n)])


#compute user rate
#a1 = 0.07
#a2 = 0.2
#channel = -36.23
#rate =(5*(10**7))*math.log(1+a1*(10**(2*channel/10))/(5*(10**(-10))),2)
#rate =(5*(10**7))*math.log(1+a2*(10**(2*channel/10))/(5*(10**(-10))+a1*(10**(2*channel/10))),2)
#print rate
def compute(pair,a):
    a1 = a
    a2 = 1- a1
    rate1 = []
    rate2 = []
    rate1.append((5 * (10 ** 7)) * math.log(1 + a1 * (10 ** (2 * pair[1] / 10)) / (5 * (10 ** (-10))), 2))
    rate2.append((5 * (10 ** 7)) * math.log(1 + a2 * (10 ** (2 * pair[0] / 10)) / (5 * (10 ** (-10)) + a1 * (10 ** (2 * pair[0] / 10))), 2))
    return rate1,rate2

def computer1(user_strong,a):

    rate1 = (5 * (10 ** 7)) * math.log(1 + a * (10 ** (2 * user_strong / 10)) / (5 * (10 ** (-10))), 2)
    return rate1
def computer2(user_weak,a):
    rate2 = (5 * (10 ** 7)) * math.log(1 + (1-a) * (10 ** (2 * user_weak / 10)) / (5 * (10 ** (-10)) + a * (10 ** (2 * user_weak / 10))), 2)
    return rate2


#compute total rate

def total_rate(rate):
    sum = 0
    n = len(rate)
    i = 0
    tot_rate = 0
    if rate == []:
        return tot_rate
    else:
        while i <(n - 1):
            sum = sum + rate[i]
            i = i +1
        tot_rate = 0.99 *sum + 0.01*rate[-1]
        return tot_rate


#compute power allocation factor
def power_alloc1(T1,user1,T2,user2):
    user1 = 10 ** (2 * user1 / 10)
    user2 = 10 ** (2 * user2 / 10)
    a_min = (((1+2*user1)**(1/2))-1)/user1
    a_max = ((1+2*user2)**(1/2))*(1+user2-((1+2*user2)**(1/2)))/(user2*(1+2*user2))
    if T1 != T2:
        a = (T1/user1 - T2/user2)/(T2 - T1)
        if a >= a_min and a <= a_max:
            a_opt = a
        elif a >= a_max or T1 < T2:
            a_opt = a_max
        else:
            a_opt = a_min
        return a_opt
    else:
        a_opt = a_max
        return a_opt

#compute gean rate of user
def gean_rate(rate):
    all_rate = 0
    for i in rate:
        all_rate = all_rate + i
    gean = all_rate/len(rate)
    return gean
#compute sum rate of the users
def sum_rate(user1,user2):
    rate1 = []
    rate2 = []
    i = 0
    while i < 10:
        total_rate1 = total_rate(rate1)
        total_rate2 = total_rate(rate2)
        a_opt = power_alloc1(total_rate1,user1,total_rate2,user2)
        rate1.append(computer1(user1,a_opt))
        rate2.append(computer2(user2,a_opt))
        i = i + 1
    #return gean_rate(rate1),gean_rate(rate2)
    return rate1,rate2
user1 = -25.0
user2 = -41
user1 = (10.0*(10.0 ** (2.0 * user1 / 10.0)))/((10.0**(-17.0))*(12.0*(10.0**6.0)))
user2 =(10.0*(10.0 ** (2.0 * user2 / 10.0)))/((10.0**(-17.0))*(12.0*(10.0**6.0)))
a_min = (((1.0+2.0*user1)**(1.0/2.0))-1.0)/user1
a_max = ((1+2*user2)**(1/2))*(1+user2-((1+2*user2)**(1/2)))/(user2*(1+2*user2))
print a_min
print a_max


print sum_rate(-39.76,-36.53)



    


