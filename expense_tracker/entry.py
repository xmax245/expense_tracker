import argparse
import json
import os.path
import datetime
import calendar
import csv

categores = {'f':'food','e':'entertainment','h':'house','b':'bills','o':'other'}

def createjson() -> list:
    temp = {}
    for num in range(1,13):
        temp[num] = 0
    data = []
    data.append(temp)
    return data

def readjson(add: bool = False) -> list:
    try:
        if os.path.exists(os.path.expanduser("~\\expense.json")):
            with open(os.path.expanduser("~\\expense.json")) as f:
                data = json.load(f)
                if type(data) == list:
                    return data
                else:
                    return createjson()
        elif add == True:
            return createjson()
        else:
            raise Exception('json file error')
    except:
        print("Expense list dosent exist please use add to create new list or delete broken expense.json file")
        exit()
        
def savejson(data: list):
    with open(os.path.expanduser("~\\expense.json"),'w+') as f:
        json.dump(data,f,indent="")

def findid(data: list,id: int,add: bool = False) -> int:
    y = 1
    for x in data[1:-1]:
        if x == {}:
            if add == True:
                return y
            else:
                y +=1
        elif add == False and x['id'] == id:
            return y
        else:
            y +=1
    if add == True:
        return None
    print('Wrong expense ID')
    raise Exception('no id in list')

def catcheck(cat: str) -> str:
    cat = cat.casefold()
    if cat in categores:
        return categores[cat]
    elif cat not in categores.values():
        print('Wrong category check your input')
        exit()
    return cat
def expense_add(desc: str,amount: int,cat: str = 'other'):
    data = readjson(True)
    id = findid(data,None,True)
    cat = catcheck(cat)    
    try:
        if id != None:
           data[id].update({'id':id,'date':datetime.datetime.now().strftime('%Y-%m-%d'),'cat':cat,'desc':desc,'amount':amount})
           print('Expense added in successfully (ID: '+str(id)+')')
        else:
            data.append({'id':len(data),'date':datetime.datetime.now().strftime('%Y-%m-%d'),'cat':cat,'desc':desc,'amount':amount})
            print('Expense added successfully (ID: '+str(len(data)-1)+')')
    except:
        print('Failed to add an expense check your input')
    savejson(data)

def expense_update(id: int,desc: str,amount: int,cat: str):
    data = readjson()
    if cat : cat = catcheck(cat)
    try:
        if desc != None or amount != None or cat != None:
            dictid = findid(data,id)
            if desc != None:
                data[dictid].update({'desc':desc})
            if amount != None:
                data[dictid].update({'amount':amount})
            if cat != None:
                data[dictid].update({'cat':cat})
            data[dictid].update({'date':datetime.datetime.now().strftime('%Y-%m-%d')})
            print('Expense updated successfully (ID: '+str(id)+')')
        else:
            raise Exception('no desc and amount')
    except:
        print('Failed to update an expense check your input')
    savejson(data)
    
def expense_delete(id: int):
    data = readjson()
    try:
        data[findid(data,id)].clear()
        print('Expense deleted successfully (ID: '+str(id)+')')
    except:
        print('Failed to delete an expense check your input')
    savejson(data)

def expense_list(cat: str):
    data = readjson()
    if cat : cat = catcheck(cat)
    print('Id  Date        Category Description  Amount')
    for x in data[1:-1]:
        if not cat:
            print(f"{x['id']}   {x['date']}  {x['cat']}  {x['desc']}  ${x['amount']}")
        elif cat == x['cat']:
            print(f"{x['id']}   {x['date']}  {x['cat']}  {x['desc']}  ${x['amount']}")
    
def expense_summary(month: int, cat:str,check: bool = False) -> int:
    if cat : cat = catcheck(cat)
    if month != None and month <= 12 and month > 0:
        data = readjson()
        amount = 0
        for x in data[1:-1]:
            if int(x['date'][0:4]) == datetime.datetime.now().year and int(x['date'][5:7]) == month:
                if not cat:
                    amount += x['amount']
                elif cat == x['cat']:
                    amount += x['amount']
        if check:
            return amount
        else:
            print(f"Total expenses for{' '+cat+' in' if cat else ''} {calendar.month_name[month].casefold()}: ${amount}")
           
    elif month == None:
        data = readjson()
        amount = 0
        for x in data[1:-1]:
            if not cat:
                amount += x['amount']
            elif cat == x['cat']:
                amount += x['amount']
        print(f"Total expenses{' for '+cat if cat else ''}: ${amount}")
    else:
        print("Wrong month number check your input")

def expense_budget(limit: int,month: str):
    data = readjson()
    if limit >= 0:
        data[0][month] = limit
        savejson(data)
    else:
        print(f"Incorrect limit can only be set to 0 or a positive whole number")
        
def budget_limit_check():
    data = readjson()
    month = datetime.datetime.now().month
    if data[0][str(month)]  > 0:
        if data[0][str(month)] < expense_summary(month,None,True):
            print(f"Warning you exceded your chosen limit for current month!\n")
        
def export():
    data = readjson()
    with open(os.path.expanduser("~\\expense export.csv"),'w',newline='') as f:
        cw = csv.writer(f)
        cw.writerow(['Id','Date','Category','Description','Amount'])
        for x in data[1:-1]:
            cw.writerow(x.values())
    print("Expenses exported to "+os.path.expanduser('~\\expense export.csv'))
def cli_entry_point():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='command')
    
    parser_add = subparsers.add_parser('add',help='Add an new expense')
    parser_add.add_argument('desc',type=str,help='expense description in "" example: "Dinner"')
    parser_add.add_argument('amount',type=int,help='expense amount example: 20')
    parser_add.add_argument('-c','--category',type=str,help='expense category: Food,Entertainment,House,Bills or Other',default='other')
    
    parser_update = subparsers.add_parser('update',help='Update an existing expense')
    parser_update.add_argument('id',type=int,help='expense id')
    parser_update.add_argument('-d','--desc',type=str,help='expense description in "" example: "Dinner"')
    parser_update.add_argument('-a','--amount',type=int,help='expense amount example: 20')
    parser_update.add_argument('-c','--category',type=str,help='expense category: Food,Entertainment,House,Bills or Other')
    
    parser_delete = subparsers.add_parser('delete',help='Delete an existing expense')
    parser_delete.add_argument('id',type=int,help='expense id')
    
    parser_list = subparsers.add_parser('list',help='list all expenses or with specific category')
    parser_list.add_argument('-c','--category',type=str,help='expense category: Food,Entertainment,House,Bills or Other')
    
    parser_summary = subparsers.add_parser('summary',help='summary of all expenses or for specific months of current year')
    parser_summary.add_argument('-m','--month',type=int,help='month number')
    parser_summary.add_argument('-c','--category',type=str,help='expense category: Food,Entertainment,House,Bills or Other')
    
    parser_budget = subparsers.add_parser('budget',help='set a budget limit for a chosen month if exceeded will display a warning')
    parser_budget.add_argument('limit',type=int,help='expense limit must be a positive whole number example: 20')
    parser_budget.add_argument('month',type=str,help='month number')
    
    subparsers.add_parser('export',help='export all expenses to .csv file')
    
    
    args = parser.parse_args()
    
    budget_limit_check()
    
    if args.command == 'add':
        expense_add(args.desc,args.amount,args.category)
    elif args.command == 'update':
        expense_update(args.id,args.desc,args.amount,args.category)
    elif args.command == 'delete':
        expense_delete(args.id)
    elif args.command == 'list':
        expense_list(args.category)
    elif args.command == 'summary':
        expense_summary(args.month,args.category)
    elif args.command == 'budget':
        expense_budget(args.limit,args.month)
    elif args.command == 'export':
        export()
    else:
        parser.print_help()
        