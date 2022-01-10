# coding:utf-8
import sys

g_sepTable = dict()

def initTable():
    g_sepTable[3000] = (0.03, 0)
    g_sepTable[12000] = (0.1, 210)
    g_sepTable[25000] = (0.2, 1410)
    g_sepTable[35000] = (0.25, 2660)
    g_sepTable[55000] = (0.3, 4410)
    g_sepTable[80000] = (0.35, 7160)
    g_sepTable[1000000] = (0.45, 15100)


def alignClass(amount):
    if amount <= 3000:
        return 3000
    elif amount <= 12000:
        return 12000
    elif amount <= 25000:
        return 25000
    elif amount <= 35000:
        return 35000
    elif amount <= 55000:
        return 55000
    elif amount <= 80000:
        return 80000
    else:
        return 1000000

def salaryTaxCalc(amountPerMonth):
    align = alignClass(amountPerMonth)
    factor = g_sepTable[align][0]
    reduct = g_sepTable[align][1]
    tax = (amountPerMonth * factor  - reduct) * 12.0
    return factor, tax, reduct

def bonusTaxCalc(bonusPerMonth):
    align = alignClass(bonusPerMonth)
    factor = g_sepTable[align][0]
    reduct = g_sepTable[align][1]
    tax = bonusPerMonth*12.0 * factor  - reduct
    return factor, tax, reduct

# 分开计税
# salary: 工资收入
# bonus：年终奖
def separateTax(salary, bonus):
    salaryFactor, salaryTax, salaryReduct = salaryTaxCalc(salary/12.0)
    bonusFactor, bonusTax, bonusReduct = bonusTaxCalc(bonus/12.0)
    

    print("\n单独计税:\t" + str(salaryTax + bonusTax) + "\n")
    
    print("\t1. 工资扣税:\t" + str(salaryTax))
    print("\t系数: \t" + str(salaryFactor) + "\t速算扣除:\t" +str(salaryReduct) + "*" + str(12.0) + "=" +str(salaryReduct*12.0) )

    print("\t2. 年终奖扣税:\t" + str(bonusTax))
    print("\t系数: \t" + str(bonusFactor) + "\t速算扣除:\t" +str(bonusReduct) )

    
# 合并计税
# salary: 工资收入
# bonus：年终奖
def mergeTax(salary, bonus):
    amount = (salary + bonus)/12.0
    factor, tax, reduct = salaryTaxCalc(amount)

    print("\n合并计税:\t" + str(tax) + "\n")
    print("\t系数: \t" + str(factor) + "\t速算扣除:\t" +str(reduct*12.0)  )


initTable()
while(True):
    salary, bonus = input("请输入2项数字: 年应税工资收入, 年终奖\n")
    separateTax(salary, bonus)
    mergeTax(salary, bonus)