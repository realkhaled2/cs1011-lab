
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

def test_part1(swap_values):
    
    grade1 = 0
    
    
    try:
        user_input1 = 3 
        user_input2 = 8 
        user_input3 = 2
        user_input4 = 4   
        v1,v2,v3,v4 = swap_values(user_input1, user_input2, user_input3, user_input4)
        #print(ord_lst)
        if v1 == user_input2 and v2 == user_input1:
            grade1 += 10
            print(f'test1 .... pass')
        else:
            print(f'test1 .... fail')
        if v3 == user_input4 and v4 == user_input3:
            grade1 += 10
            print(f'test2 .... pass')
        else:
            print(f'test2 .... fail')
    except Exception as ex:
        grade1 = 0
        pass
    
    
    return grade1



def test():
    
    files = glob.glob('lab3-*.ipynb')
    
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
        
        
        from basename import swap_values
        import math
        
        print('='*20)
        print(f'Swapping variables')
        print('='*20)

        grade_p1 = test_part1(swap_values)
        
        print()

        grades.append(grade_p1)
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
    


