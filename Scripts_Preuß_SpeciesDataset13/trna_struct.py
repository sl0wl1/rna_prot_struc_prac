import re

def find_trna_struc_sections(struc: str)->str:
    """
    Find the sections of the tRNA structure. Uses the method of changing characters. Do not use ;)
    """
    if not struc:
        return ""
    
    tmp_char = struc[0]
    str_sections = f"{tmp_char}"
    for char in struc:
        
        if char != tmp_char:            
            str_sections = f"{str_sections}{char}"
            tmp_char = char
      
    return str_sections

def count_stems(struc_abs: str) -> int:
    """
    Count the number of stems in the abstracted tRNA structure.
    """
    
    if "(" in struc_abs:
        number_opening_brackets = struc_abs.count("(")
        number_closing_brackets = struc_abs.count(")")
        
    else:
        number_opening_brackets = struc_abs.count("[")
        number_closing_brackets = struc_abs.count("]")
        
    
    try:
        
        if number_opening_brackets == number_closing_brackets:
        
            return number_opening_brackets
        
        else:
            raise ValueError("The number of opening and closing brackets does not match in the structure string.")  
    
    except ValueError:
        
        return 0
        
def check_struc_abs(struc_abs: str, patterns:dict = {"(.(.).(.).(.)).": "tRNA_4-stems", "(.(.).(.).(.).(.)).": "tRNA_5-stems"}) -> str:
    """
    Check for structure patterns in the tRNA structure. 
    """
     
    if struc_abs in patterns.keys():
        
        return(patterns[struc_abs])
        
    else:
        
        return "tRNA_out"      
    
def check_struc_abs_viennarna(struc_abs: str, patterns:dict = {"[[][][]]": "tRNA_4-stems", "[[][][][]]": "tRNA_5-stems"}) -> str:
    """
    Check for structure patterns in the tRNA structure. 
    """
     
    if struc_abs in patterns.keys():
        
        return(patterns[struc_abs])
        
    else:
        
        return "tRNA_out"  
    
def struct_abstractor(struct: str) -> str:
    """
    Abstracts the input string to single brackets and dots for every part.
    This is the way! 
    """
    stack_counter_opening_brackets = []
    result = ""
    counter_opening_brackets = 0
    counter_closing_brackets = 0
    prev_char = ""   
    
    for char in struct:
        
        if char == "(":
            
            counter_opening_brackets += 1
            
        else:
            
            if counter_opening_brackets > 0:
                
                stack_counter_opening_brackets.append(counter_opening_brackets)
                result = f"{result}("
                counter_opening_brackets = 0
                
            if char == ")":
                
                counter_closing_brackets += 1
                
                if stack_counter_opening_brackets:
                    
                    if counter_closing_brackets == stack_counter_opening_brackets[-1]:
                        
                        result = f"{result})"
                        stack_counter_opening_brackets.pop()
                        counter_closing_brackets = 0
                        
            if char == "." and prev_char != ".":
                
                result = f"{result}."

        prev_char = char

    return result

def struct_abstractor_test(struct: str) -> str:
    """
    Abstracts the input string to single brackets and dots for every part.
    This is the way! 
    """
    stack_counter_opening_brackets = []
    result_1 = ""
    counter_opening_brackets = 0
    counter_closing_brackets = 0
    prev_char = ""   
    
    for char in struct:
        
        if char == "(":
            
            counter_opening_brackets += 1
            
        elif char != "(":
            
            if counter_opening_brackets > 0:
                
                stack_counter_opening_brackets.append(counter_opening_brackets)
                result_1 = f"{result_1}("
                counter_opening_brackets = 0
                
            if char == ")":
                
                counter_closing_brackets += 1
                
                if stack_counter_opening_brackets:
                    
                    if counter_closing_brackets == stack_counter_opening_brackets[-1]:
                        
                        result = f"{result_1})"
                        stack_counter_opening_brackets.pop()
                        counter_closing_brackets = 0
                        
            if char == "." and prev_char != ".":
                
                result = f"{result_1}."
        
        elif char == ")":
            
            counter_closing_brackets += 1
            
        else:
            
            if counter_opening_brackets > 0:
                
                stack_counter_opening_brackets.append(counter_opening_brackets)
                result_1 = f"{result_1}("
                counter_opening_brackets = 0
                
            if char == ")":
                
                counter_closing_brackets += 1
                
                if stack_counter_opening_brackets:
                    
                    if counter_closing_brackets == stack_counter_opening_brackets[-1]:
                        
                        result = f"{result_1})"
                        stack_counter_opening_brackets.pop()
                        counter_closing_brackets = 0
                        
            if char == "." and prev_char != ".":
                
                result = f"{result_1}."             
                


        prev_char = char

    return result



def find_loop_dots(struct:str) -> list[str]:
    """
    Finds all substrings in the input string where a random number of dots are enclosed in round brackets.
    Example: '(....)', '(..)', etc.
    Returns a list of matches.
    """
    pattern = r'\(\.+\)'
    return re.findall(pattern, struct)