
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

 
@patch('builtins.print') # to test the builtin function print
def test_builtin(mock_print):
    
    from basename import calculate_calories
    
    age_years = 19
    weight_pounds = 155
    heart_bpm = 145
    time_minutes = 60
    
    try:
        calculate_calories(age_years,weight_pounds,heart_bpm,time_minutes)
        mock_print.assert_called_with('Calories: 653.71')
        return 10
    except Exception as ex:
        return 0


def test():
    
    files = glob.glob('lab1-*.ipynb')
    
    grades = []
    stud_nums = []
    error = []
    
    for fn in files:
        
        grade = 0

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
        
        from basename import calculate_calories,line_number,prefix,area_code
        
        
        print('='*20)
        print(f'Part 1')
        print('='*20)
        
        
        try:
            bgrade = test_builtin()
            grade += bgrade
            if bgrade != 0:
                print('calories are correctly calculated \n')
            else:
                print('calories are not correctly calculated \n')
            
        except Exception as ex:
            pass
        
        
        print('='*20)
        print(f'Part 2')
        print('='*20)
        
        phone_number = 9994446545
        try:
            if line_number(phone_number) == 6545:
                grade += 5
                print('line_number is correct')
            else:
                print('line_number is not correct')
        except Exception as ex:
            pass
        
        try:
            if prefix(phone_number) == 444:
                grade += 5
                print('prefix is correct')
            else:
                print('prefix is not correct')
        except Exception as ex:
            pass  
            
        try:
            if area_code(phone_number) == 999:
                grade += 5
                print('area_code is correct')
            else:
                print('area_code is not correct')
        except Exception as ex:
            pass

        grades.append(grade)
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
        
        df = pd.DataFrame(list(zip(num, grade)),columns =['Student ID', 'Grade'],dtype = float)
        df.to_excel(f'{lab_name}.xlsx')
    


