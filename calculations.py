import math


def calculate(prompt):
    """
    Checks if the input prompt contains certain keywords then
    performs mathematical functions on the input string.
    The string must follow certain rules for each equation listed below:
        addition: command - 'calculate number plus number' or
                            'calculate number add number'
        subtraction: command - 'calculate number minus number' or
                            'calculate number subtract number' or
                            'calculate number subtracted by number'
        multiplication: command - 'calculate number times number' or
                                'calculate number multiplied by number'
        division: command - 'calculate number divided by number' or
                            'calculate number multiplied by number'
        exponential: command - 'calculate number to the power of number' or
                                'calculate number to the power number' or
                                'calculate number power number'
        square root: command - 'calculate the square root of number'
        factorial: command - 'calculate number factorial'
        logarithmic: command - 'calculate log base number of number'
    :param prompt:
    :return: a tuple of the result and the formula
    """
    if 'add' in prompt:
        """Splits the command at 'add' then adds the 2 numbers from the prompt: 'calculate number add number'"""
        calc_prompt = prompt.split('add')
        result = round(float(calc_prompt[0]) + float(calc_prompt[1]), 2)
        return (result, prompt)

    if '+' in prompt:
        """Splits the command at '+' then adds the 2 numbers from the prompt: 'calculate number plus number'"""
        calc_prompt = prompt.split('+')
        result = round(float(calc_prompt[0]) + float(calc_prompt[1]), 2)
        return (result, prompt)

    if '-' in prompt:
        """Splits the command at '-' then subtracts the 2nd number from the 1st from the prompt: 'calculate number minus number'"""
        calc_prompt = prompt.split('-')
        prompt = prompt.replace('-', 'minus')
        result = round(float(calc_prompt[0]) - float(calc_prompt[1]), 2)
        return (result, prompt)

    if 'subtract' in prompt:
        """Splits the command at 'subtract' then subtracts the 2nd number from the 1st from the prompt: 'calculate number subtract number'"""
        calc_prompt = prompt.split('subtract')
        prompt = prompt.replace('subtract', 'minus')
        result = round(float(calc_prompt[0]) - float(calc_prompt[1]), 2)
        return (result, prompt)

    if 'subtracted by' in prompt:
        """Splits the command at 'subtracted by' then subtracts the 2nd number from the 1st from the prompt: 'calculate number subtracted by number'"""
        calc_prompt = prompt.split('subtracted by')
        prompt = prompt.replace('subtracted by', 'minus')
        result = round(float(calc_prompt[0]) - float(calc_prompt[1]), 2)
        return (result, prompt)

    if 'times' in prompt:
        """Splits the command at 'times' then multiplied the 2 numbers from the prompt: 'calculate number times number'"""
        calc_prompt = prompt.split('times')
        result = round(float(calc_prompt[0]) * float(calc_prompt[1]), 2)
        return (result, prompt)

    if 'multiplied by' in prompt:
        """Splits the command at 'multiplied by' then multiplies the 2 numbers from the prompt: 'calculate number multiplied by number'"""
        calc_prompt = prompt.split('multiplied by')
        result = round(float(calc_prompt[0]) * float(calc_prompt[1]), 2)
        return (result, prompt)

    if '*' in prompt:
        """Splits the command at '*' then multiplies the 2 numbers from the prompt: 'calculate number times number'"""
        calc_prompt = prompt.split('*')
        prompt = prompt.replace('*', 'times')
        result = round(float(calc_prompt[0]) * float(calc_prompt[1]), 2)
        return (result, prompt)

    if '/' in prompt:
        """Splits the command at '/' then divides the 1st number by the 2nd number from the prompt: 'calculate number divided by number'"""
        calc_prompt = prompt.split('/')
        prompt = prompt.replace('/', 'divided by')
        result = round(float(calc_prompt[0]) / float(calc_prompt[1]), 2)
        return (result, prompt)

    if 'divided by' in prompt:
        """Splits the command at 'divided by' then divides the 1st number by the 2nd number from the prompt: 'calculate number divided by number'"""
        calc_prompt = prompt.split('divided by')
        result = round(float(calc_prompt[0]) / float(calc_prompt[1]), 2)
        return (result, prompt)

    if 'to the power of' in prompt:
        """Splits the command at 'to the power of' then takes the 1st number to the power of the 2nd number from the prompt: 'calculate number to the power of number'"""
        calc_prompt = prompt.split('to the power of')
        result = round(float(calc_prompt[0]) ** float(calc_prompt[1]), 2)
        return (result, prompt)

    if 'to the power' in prompt:
        """Splits the command at 'to the power' then takes the 1st number to the power of the 2nd number from the prompt: 'calculate number to the power number'"""
        calc_prompt = prompt.split('to the power')
        prompt = prompt.replace('to the power', 'to the power of')
        result = round(float(calc_prompt[0]) ** float(calc_prompt[1]), 2)
        return (result, prompt)

    if 'power' in prompt:
        """Splits the command at 'power' then takes the 1st number to the power of the 2nd number from the prompt: 'calculate number power number'"""
        calc_prompt = prompt.split('power')
        prompt = prompt.replace('power', 'to the power of')
        result = round(float(calc_prompt[0]) ** float(calc_prompt[1]), 2)
        return (result, prompt)

    if '^' in prompt:
        """Splits the command at '^' then takes the 1st number to the power of the 2nd number from the prompt: 'calculate number to the power of number'"""
        calc_prompt = prompt.split('^')
        prompt = prompt.replace('^', 'to the power of')
        result = round(float(calc_prompt[0]) ** float(calc_prompt[1]), 2)
        return (result, prompt)

    if 'the square root of' in prompt:
        """Remove 'the square root of' from the command then takes the square root of the number from the prompt: 'calculate the square root of number'"""
        calc_prompt = prompt.replace('the square root of', '')
        result = round(math.sqrt(float(calc_prompt)), 2)
        return (result, prompt)

    if 'factorial' in prompt:
        """Removes 'factorial' from the command then takes the factorial of the number from the prompt: 'calculate number factorial'"""
        calc_prompt = prompt.replace('factorial', '')
        result = round(math.factorial(float(calc_prompt)), 2)
        return (result, prompt)

    if 'log base' in prompt:
        """Removes 'log base' and 'of' from the command then takes the log base(1st number) of the 2nd number  from the prompt: 'calculate number factorial'"""
        calc_prompt = prompt.replace(' log base ', '').replace(' of', '')
        calc_prompt = calc_prompt.split(' ')
        print('calc_prompt:', calc_prompt)
        result = round(math.log(float(calc_prompt[1]), float(calc_prompt[0])), 2)
        return (result, prompt)
