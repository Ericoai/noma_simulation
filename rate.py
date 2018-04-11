# -*- coding: utf-8 -*-
#添加模块
import random
import math

#设置发射功率
P = 10
w = 50 * 10 ** 6

#初始化信道参数列表
H = []

'''
#通过距离计算信道参数浙大师兄的信道参数设置
i = 0
while i < 10:
    d = random.uniform(0.1, 0.5)
    h = 128.1+37.6*math.log10(d)
    H.append(h)
    i = i + 1
'''
#通过距离计算信道参数浙大师兄的信道参数设置
i = 0
while i < 10:
    d = random.uniform(0.1, 0.5)
    h = 55.1+30.6*math.log10(d)
    H.append(h)
    i = i + 1
#print "输出随机产生的信道参数："
#print H

#生成信道差异矩阵
def diff_channel(user):
    total = []
    for i in user:
        raw = []
        for j in user:
            raw.append(abs(i - j))
        total.append(raw)
    return total

#变化信道差异矩阵显示方式
'''
print "输出信道差异矩阵："
a =  diff_channel(H)
for i in a:
    for j in i:
        print '%.3f\t'%j,
    print '\n'
'''
#用户匹配算法使用折半匹配的方式
def pairing(user):
    i = 0
    user_pair = []
    user.sort()
    n = len(user)
    user_weak = user[0:n / 2]
    user_strong = user[n / 2:n]
    while i < n/2:
        user_pair.append(user_weak[i])
        user_pair.append(user_strong[i])
        i = i + 1
    return user_pair
#print "输出折半匹配后的信道参数："
#print pairing(H)

#H = [29.11737063308213, 34.91647140269404, 30.865439656662296, 38.63593266226554, 31.117535749027926, 40.02373702295605, 32.5754176651823, 40.99045566021399, 32.769672626736494, 42.252680382764495]

#计算OMA方式下用户数据速率
def compute1_oma(user_strong):
    #w = 2 * 10 ** 6
    rate1 = (1/2.0)*w * math.log(1 + P * (10.0 ** (user_strong *2 / 10.0)) / ((10.0 ** (-17.4)) * w *(1/2.0)), 2)
    return rate1

def computer2_oma(user_weak):
    #w = 2 * 10 ** 6
    rate2 = (1/2.0) * w * math.log(1 + P * (10.0 ** (user_weak * 2/ 10.0)) / ((10.0 ** (-17.4))*w *(1/2.0)), 2)
    return rate2

#计算NOMA方式下用户数据速率
def computer1_noma(user_strong,a):
    #w = 2 * 10 ** 6
    rate1 = w * math.log(1 + a * P * (10 ** (user_strong *2 / 10)) /((10 ** (-17.4))*w), 2)
    return rate1

def computer2_noma(user_weak,a):
    #w = 2 * 10 ** 6
    rate2 = w * math.log(1 + (1-a) * P * (10 ** (user_weak * 2 / 10)) / ((10 ** (-17.4))*w + a * P * (10 ** (user_weak * 2/ 10))), 2)
    return rate2


#计算系统总吞吐量
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


#使用比列公平计算方法计算用户间功率分配因子
def power_alloc1(T1,user1,T2,user2):
    a_chance = []
    user1 = 10.0 ** (user1 * 2 / 10)
    user2 = 10.0 ** (user2 * 2/ 10)
    user1 = user1 * P/(10**(-17)*w)
    user2 = user2 * P/(10**(-17)*w)
    a_min = (((1+2.0*user1)**(1/2.0))-1)/user1
    a_max = (((1 + 2.0 * user2) ** (1 / 2.0)) - 1) / user2
    if a_max > 0.5:
        a_max = 0.5
    a_chance.append(a_min)
    a_chance.append(a_max)
    #print "输出最大和最小功率分配因子："
    #print a_chance
    #a_max = ((1+2*user2)**(1/2.0))*(1+user2-((1+2.0*user2)**(1/2.0)))/(user2*(1+2.0*user2))
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

#计算用户的平均数据速率
def gean_rate(rate):
    all_rate = 0
    for i in rate:
        all_rate = all_rate + i
    gean = all_rate/len(rate)
    return gean

#计算用户在OMA系统中的速率
def sum_rate_oma(user1,user2):
    rate_oma = []
    rate_oma.append(compute1_oma(user1))
    rate_oma.append(computer2_oma(user2))
    return rate_oma

#计算系统OMA的总数据速率
def sum_total_oma(user1,user2):
    return compute1_oma(user1)+computer2_oma(user2)

#计算用户在NOMA系统中的总数据
def sum_rate_noma(user1,user2):
    rate1 = []
    rate2 = []
    rate_two_user = []
    i = 0
    while i < 10:
        total_rate1 = total_rate(rate1)
        total_rate2 = total_rate(rate2)
        a_opt = power_alloc1(total_rate1,user1,total_rate2,user2)
        #print a_opt
        rate1.append(computer1_noma(user1,a_opt))
        rate2.append(computer2_noma(user2,a_opt))
        i = i + 1
    rate_two_user.append(gean_rate(rate1))
    rate_two_user.append(gean_rate(rate2))
    return rate_two_user
    #return rate1,rate2

#计算两用户在NOMA系统中的总速率
def sum_total_noma(user1,user2):
    rate1 = []
    rate2 = []
    rate_two_user = []
    i = 0
    while i < 10:
        total_rate1 = total_rate(rate1)
        total_rate2 = total_rate(rate2)
        a_opt = power_alloc1(total_rate1,user1,total_rate2,user2)
        #print a_opt
        rate1.append(computer1_noma(user1,a_opt))
        rate2.append(computer2_noma(user2,a_opt))
        i = i + 1
    return gean_rate(rate1)+ gean_rate(rate2)

print "输出两用户OMA的平均速率："
total_user_oma = []
total_user_oma.append(sum_rate_oma(-29.117,-34.916))
total_user_oma.append(sum_rate_oma(-30.864,-38.636))
total_user_oma.append(sum_rate_oma(-31.118,-40.024))
total_user_oma.append(sum_rate_oma(-32.575,-40.990))
total_user_oma.append(sum_rate_oma(-32.770,-42.253))
print total_user_oma

print "输出两用户NOMA的平均速率："
total_user_noma = []
total_user_noma.append(sum_rate_noma(-29.117,-34.916))
total_user_noma.append(sum_rate_noma(-30.864,-38.636))
total_user_noma.append(sum_rate_noma(-31.118,-40.024))
total_user_noma.append(sum_rate_noma(-32.575,-40.990))
total_user_noma.append(sum_rate_noma(-32.770,-42.253))
print total_user_noma

print "输出OMA系统两用户总数据速率："
total_system_oma = []
total_system_oma.append(sum_total_oma(-29.117,-34.916))
total_system_oma.append(sum_total_oma(-30.864,-38.636))
total_system_oma.append(sum_total_oma(-31.118,-40.024))
total_system_oma.append(sum_total_oma(-32.575,-40.990))
total_system_oma.append(sum_total_oma(-32.770,-42.253))
sum_system_oma = sum_total_oma(-29.117,-34.916) + sum_total_oma(-30.864,-38.636)+sum_total_oma(-31.118,-40.024) + sum_total_oma(-32.575,-40.990)+ sum_total_oma(-32.770,-42.253)
print total_system_oma
print sum_system_oma

print "输出NOMA系统两用户总数据速率："
total_system_noma = []
total_system_noma.append(sum_total_noma(-29.117,-34.916))
total_system_noma.append(sum_total_noma(-30.864,-38.636))
total_system_noma.append(sum_total_noma(-31.118,-40.024))
total_system_noma.append(sum_total_noma(-32.575,-40.990))
total_system_noma.append(sum_total_noma(-32.770,-42.253))
sum_system_noma = sum_total_noma(-29.117,-34.916)+sum_total_noma(-30.864,-38.636)+sum_total_noma(-31.118,-40.024)+sum_total_noma(-32.575,-40.990)+sum_total_noma(-32.770,-42.253)
print total_system_noma
print sum_system_noma
