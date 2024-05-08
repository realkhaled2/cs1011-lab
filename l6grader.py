
import os
import sys
import subprocess,glob
import ntpath
import re
import types
import ast
import builtins
from unittest.mock import patch, call

instructor = False

def test_part1(in_order):
    
    grade1 = 0
    
    try:
        n1 = [5, 6, 7, 8, 3]
        v = in_order(n1)
        if (v is not None) or (v==False):
            grade1 += 5
            print(f'test with input {n1}.... pass')
        else:
            print(f'test with input {n1}.... fail')
    except Exception as ex:
        pass
    
    try:
        n2 = [5, 6, 7, 8, 10]
        v = in_order(n2)
        if v:
            grade1 += 5
            print(f'test with input {n2}.... pass')
        else:
            print(f'test with input {n2}.... fail')
    except Exception as ex:
        pass
    
    return grade1

def test_part2(max_,sum_,remove_,append_,average_,set_,uniq_,replace_):

    lst = [1, 3, 3, 4, 5, 5, 6, 6]
    clst = lst.copy()
    
    grade = 0
    try:
        if max_(lst) == 6:
            grade += 1
            print('max_() is correct')
        else:
            print('max_() is not correct')
    except Exception as ex:
        pass
        
    try:
        if sum_(lst) == 33:
            grade += 1
            print('sum_() is correct')
        else:
            print('sum_() is not correct')
    except Exception as ex:
        pass  
            
    try:
        if remove_(clst).sort() == [1, 3, 4, 5, 5, 6, 6].sort():
            grade += 1
            print('remove_() is correct')
        else:
            print('remove_() is not correct')
    except Exception as ex:
        pass
        
        
    try:
        if append_(clst,1000).sort() == [1, 3, 4, 5, 5, 6, 6, 1000].sort():
            grade += 1
            print('append_() is correct')
        else:
            print('append_() is not correct')
    except Exception as ex:
        pass
    
    try:
        if math.isclose(average_(lst),sum(lst)/len(lst)) == True:
            grade += 1
            print('average_() is correct')
        else:
            print('average_() is not correct')
    except Exception as ex:
        pass
        
    try:
        s = set_(lst)
        if s[0]== 3 and s[1] == 5:
            grade += 2
            print('set_() is correct')
        else:
            print('set_() is not correct')
    except Exception as ex:
        pass
        
        
    try:
        u = uniq_(lst)
        if u.sort() == [1, 3, 4, 5, 6].sort():
            grade += 1
            print('uniq_() is correct')
        else:
            print('uniq_() is not correct')
    except Exception as ex:
        pass
        
        
    try:
        rlst = replace_(lst)
        if rlst[0] == -1:
            grade += 2
            print('replace_min() is correct')
        else:
            print('replace_min() is not correct')
    except Exception as ex:
        pass
    return grade
    
def test():
    
    files = glob.glob('lab6-*.ipynb')
    
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
        
        
        from basename import in_order,max_,sum_,remove_,append_,average_,set_,uniq_,replace_
        import math
        
        print('='*20)
        print(f'Check if list is sorted')
        print('='*20)

        grade_p1 = test_part1(in_order)

        print('='*20)
        print(f'List Operations')
        print('='*20)
        
        grade_p2 = test_part2(max_,sum_,remove_,append_,average_,set_,uniq_,replace_)

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
    


