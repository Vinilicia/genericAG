import numpy as np
import math

def funcaoObjetivo(indv, d, p, xMin, xMax):
    xs = []
    for bits in indv:
        num = 0
        for bit in bits:
            num = num * 2 + bit
        xs.append(num)
    for i in range(len(xs)):    
        xs[i] = xMin+((xMax-xMin)/(2**p-1))*xs[i]
    e = math.e
    sum1 = np.sum(np.square(xs))
    sum2 = np.sum(np.cos(2 * np.pi * np.array(xs)))
    f = -20*e**(-0.2*np.sqrt(sum1/d)) -e**((1/d)*sum2) + 20 + e
    return f

def avaliaPopulacao(pop, nPop, d, p, xMin, xMax, melhor):
    fits = []
    for i in range(nPop):
        fit = funcaoObjetivo(pop[i], d, p, xMin, xMax)
        fits.append(fit)
        if fit < melhor:
            melhor = fit
    return fits, melhor

def selecionaPais(nPop, fit):
    pais = []
    pv = 0.9
    for i in range(nPop):
        p1 = np.random.randint(0, nPop)
        p2 = np.random.randint(0, nPop)
        while p1 == p2:
            p2 = np.random.randint(0, nPop)
        r = np.random.uniform(0, 1)
        if fit[p1] < fit[p2]:
            if r > pv or (i > 0 and pais[i-1] == p1):
                pais.append(p2)
            else:
                pais.append(p1)
        else:
            if r < pv or (i > 0 and pais[i-1] == p1):
                pais.append(p2)
            else:
                pais.append(p1)
    return pais

def cruzamento(pais, pop, nPop, Pc, p, d):
    popIntermed = pop.copy()
    for i in range(0,nPop,2):
        r = np.random.uniform(0, 1)
        if r < Pc:
            r = np.random.randint(1, p)
            for j in range(d):
                temp = popIntermed[pais[i]][j][:r].copy()
                popIntermed[pais[i]][j][:r] = popIntermed[pais[i+1]][j][:r]
                popIntermed[pais[i+1]][j][:r] = temp
    return popIntermed

def mutacao(pop, nPop, Pm, p, d):
    for i in range(nPop):
        for j in range(d):
            for k in range(p):
                r = np.random.uniform(0, 1)
                if r < Pm:
                    pop[i][j][k] = 1 - pop[i][j][k]

def elitismo(pop, popi, n, ne, d, p, xMin, xMax):
    
    fit, _ = avaliaPopulacao
    pass

def genericAG(melhor):
    nPop = 100
    dimFunc = 2
    precisao = 6
    nGer = 100
    nElite = 2
    xMin = -2
    xMax = 2
    pop = np.random.randint(0, 2, (nPop, dimFunc, precisao))
    Pc = 1
    Pm = 0.1
    melhor = funcaoObjetivo(pop[0], dimFunc, precisao, xMin, xMax)
    print(melhor)
    for i in range(nGer):
        fit, melhor = avaliaPopulacao(pop, nPop, dimFunc, precisao, xMin, xMax, melhor)
        pais = selecionaPais(nPop, fit)
        popIntermed = cruzamento(pais, pop, nPop, Pc, precisao, dimFunc)
        mutacao(popIntermed, nPop, Pm, precisao, dimFunc)
        elitismo(pop, popIntermed, nPop, nElite)
        pop = popIntermed.copy()
    return melhor

melhor = 0
melhor = genericAG(melhor)
print(melhor)