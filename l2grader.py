
import os
import sys
import subprocess,glob
import ntpath
import re
import types
import ast
import builtins
#from unittest.mock import patch, call

instructor = False

def test_part1(alphabetical_order):
    
    grade1 = 0
    
    
    try:
        lst = ['a','b','c']
        ord_lst = alphabetical_order(lst)
        #print(ord_lst)
        if ord_lst == ['a','b','c']:
            grade1 += 5
            print(f'test1 with input {lst}.... pass')
        else:
            print(f'test1 with input {lst}.... fail')
    except Exception as ex:
        pass
        
    
    
    try:
        lst = ['c','b','a']
        ord_lst = alphabetical_order(lst)
        #print(ord_lst)
        if ord_lst == ['a','b','c']:
            grade1 += 2.5
            print(f'test2 with input {lst}.... pass')
        else:
            print(f'test2 with input {lst}.... fail')
    except Exception as ex:
        pass
    
    try:
        lst = ['c','a','b']
        ord_lst = alphabetical_order(lst)
        #print(ord_lst)
        if ord_lst == ['a','b','c']:
            grade1 += 2.5
            print(f'test2 with input {lst}.... pass')
        else:
            print(f'test2 with input {lst}.... fail')
    except Exception as ex:
        pass
    
    return grade1


def test_part2(count_odd):
    
    #from basename import count_odd
    
    grade2 = 0
    
    lst = [1,2,3,4]
    try:
        output = count_odd(lst)
        if output == 2:
            grade2 += 5
            print(f'test1 with input {lst}....     pass')
        else:
            print(f'test1 with input {lst}....     fail')
    except Exception as ex:
        pass
        
    lst = [19,19,19,19]
        
    try:
        output = count_odd(lst)
        if output == 4:
            grade2 += 5
            print(f'test2 with input {lst}.... pass')
        else:
            print(f'test2 with input {lst}.... fail')
    except Exception as ex:
        pass
    
    return grade2

def test():
    
    files = glob.glob('lab2-*.ipynb')
    
    grades = []
    stud_nums = []
    error = []
    
    for fn in files:

        basename = os.path.splitext(os.path.basename(fn))[0]
        stud_num = basename.split('-')[1]
        lab_name = basename.split('-')[0]
        
        with open('notebook.py', 'w') as outputFile:
            subprocess.call(['jupyter', 'nbconvert', '--to', 'script',
                             fn, '--stdout'], stdout=outputFile)

        #tree = ast.parse(open(fn).read(), 'eval')
        with open('notebook.py') as fp:
            tree = ast.parse(fp.read(), 'eval')
        
        for node in tree.body[:]:
            if (not isinstance(node, ast.FunctionDef) and not isinstance(node, ast.Import)
                and not isinstance(node, ast.ImportFrom)):
                tree.body.remove(node)
        module = types.ModuleType(basename)
        #print(module.__dict__)
        # use compile to exec multi-line
        code = compile(tree,fn, 'exec')
        sys.modules['basename'] = module
        exec(code,module.__dict__)
        
        
        from basename import alphabetical_order, count_odd
        import math
        
        print('='*20)
        print(f'Part 1: Alphabetical Order')
        print('='*20)

        grade_p1 = test_part1(alphabetical_order)
        
        print()
        
        print('='*20)
        print(f'Part 2: Count odd numbers')
        print('='*20)

        grade_p2 = test_part2(count_odd)

        grades.append(grade_p1+grade_p2)
        stud_nums.append(stud_num)
    
    return stud_nums,grades,lab_name

if __name__ == "__main__":

    num, grade,lab_name = test()


    if instructor:
        import pandas as pd
        
        print('='*40)
        print(f'Student ID\t\t' + f'Grade')
        print('='*40)

        for i in range(len(num)):
            print(f'{num[i]}\t\t\t' + f'{grade[i]}')
        
        
        df = pd.DataFrame(list(zip(num,[float(x) for x in grade])),columns =['Student ID', 'Grade'])
        df.to_excel(f'{lab_name}.xlsx')
    
    else:
        print('='*40)
        print(f'Student ID\t\t' + f'Grade')
        print(f'{num[0]}\t\t\t' + f'{grade[0]}')
        print('='*40)
    


