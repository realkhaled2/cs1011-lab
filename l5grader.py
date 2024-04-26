
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

def test_part1(reverse):
    
    grade1 = 0
    
    try:
        lst = 'Hello there'
        v = reverse(lst)
        if v == 'ereht olleH':
            grade1 += 10
            print(f'test with input {lst}.... pass')
        else:
            print(f'test with input {lst}.... fail')
    except Exception as ex:
        pass
    
    try:
        lst = 'See Saw'
        v = reverse(lst)
        if v == 'waS eeS':
            grade1 += 5
            print(f'test with input {lst}.... pass')
        else:
            print(f'test with input {lst}.... fail')
    except Exception as ex:
        pass
    
    try:
        lst = 'Oh my!!!'
        v = reverse(lst)
        if v == '!!!ym hO':
            grade1 += 5
            print(f'test with input {lst}.... pass')
        else:
            print(f'test with input {lst}.... fail')
    except Exception as ex:
        pass
    
    return grade1

def test():
    
    files = glob.glob('lab5-*.ipynb')
    
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
        
        
        from basename import reverse
        import math
        
        print('='*20)
        print(f'Print string in reverse')
        print('='*20)

        grade_p1 = test_part1(reverse)

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
    


