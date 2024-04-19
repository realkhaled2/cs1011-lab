
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


def test_part2(output_range):
    
    grade2 = 0
    
    num1,num2 = -15,10
    try:
        output = output_range(num1,num2)
        if output == [-15, -10, -5, 0, 5, 10]:
            grade2 += 10
            print(f'test with input {num1} and {num2}....     pass')
        else:
            print(f'test with input {num1} and {num2}....     fail')
    except Exception as ex:
        pass
        
    num1,num2 = 20,5
    try:
        output = output_range(num1,num2)
        if output == 0:
            grade2 += 10
            print(f'test with input {num1} and {num2}....     pass')
        else:
            print(f'test with input {num1} and {num2}....     fail')
    except Exception as ex:
        pass
    
    return grade2

def test():
    
    files = glob.glob('lab4-*.ipynb')
    
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
        
        
        from basename import output_range
        import math
        
        print('='*20)
        print(f'Output range with increment of 5')
        print('='*20)

        grade_p2 = test_part2(output_range)

        grades.append(grade_p2)
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
    


