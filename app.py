import tkinter as tk
from tkinter.font import Font


class Calculator:

    def __init__(self, frame):
        # States
        self.first_operand = ''
        self.operator = ''
        self.second_operand = ''
        self.result = ''

        # Main buttons styles
        self.buttn_styles = dict(width=8, height=4, bd=0, relief="solid", font=Font(family="Verdana", size=12))

        # Main input
        self.main_input = tk.Label(frame, padx=15, pady=15, height=2, anchor="se",
                                   bg="#fff", fg="#141719", font=Font(family="Verdana", size=24))
        self.main_input.grid(column=0, row=0, columnspan=4, sticky="nsew")

        # Operators generation
        self.generate_operands(frame)
        # Numbers generation
        self.generate_numbers(frame)
        # Special characters generation
        self.generate_special(frame)

    def generate_numbers(self, frame):
        number_params = dict(**self.buttn_styles, bg="#1e2326", fg="#fff", activebackground="#181c1f", activeforeground="#fff")

        for number in range(1, 10):
            column = (number - 1) % 3
            row = 4 if number < 4 else 3 if number < 7 else 2
            tk.Button(frame, text=str(number), command=self._number_callback(number), **number_params).grid(column=column, row=row, sticky='news')

        # Create 0
        tk.Button(frame, text='0', command=self._number_callback(0), **number_params).grid(column=0, row=5, sticky='news')

        # Create .
        tk.Button(frame, text='.', command=self.add_dot, **number_params).grid(column=1, row=5, sticky='news')

        # Create .
        tk.Button(frame, text='del', command=self.clear_all, **number_params).grid(column=2, row=5, sticky='news')

    def generate_operands(self, frame):
        operand_params = dict(width=7, height=3, bd=0, relief="solid", font=Font(family="Verdana", size=14),
                              bg="#ff9f0a", fg="#fff", activebackground="#f1960a", activeforeground="#fff")

        for index, operator in enumerate(['÷', '×', '-', '+']):
            column = 3
            row = index + 1
            tk.Button(frame, text=str(operator), command=self._operand_callback(operator),
                      **operand_params,).grid(column=column, row=row, sticky='nsew')

        # Create =
        tk.Button(frame, text='=', command=self.get_result, **operand_params).grid(column=3, row=5, sticky='nsew')

    def generate_special(self, frame):
        special_params = dict(**self.buttn_styles, bg="#141719", fg="#fff", activebackground="#0f1113", activeforeground="#fff")

        # Create C
        tk.Button(frame, text='C', command=self.remove_last, **special_params).grid(column=0, row=1, sticky='news')

        # Create ±
        tk.Button(frame, text='±', command=self.inver_operand,  **special_params).grid(column=1, row=1, sticky='news')

        # Create %
        tk.Button(frame, text='%', command=self.add_percentage, **special_params).grid(column=2, row=1, sticky='news')

    def add_number(self, number):
        # Move result to the firs operand and clear other states if the number was pressed when the result is not empty
        self._result_to_first_operand()

        if self.operator:
            self.second_operand = self._concat_values(self.second_operand, number)
        else:
            self.first_operand = self._concat_values(self.first_operand, number)

        # Show changes on the screen
        self._detect_screen_changes()

    def add_dot(self):
        # Move result to the firs operand and clear other states if the dot was pressed when the result is not empty
        self._result_to_first_operand()

        if self.operator and '.' not in self.second_operand:
            self.second_operand = self._concat_values(self.second_operand, '.')
        elif '.' not in self.first_operand:
            self.first_operand = self._concat_values(self.first_operand, '.')

        # Show changes on the screen
        self._detect_screen_changes()

    def add_percentage(self):
        # Move result to the firs operand and clear other states if the percentage was pressed when the result is not empty
        self._result_to_first_operand()

        if self.operator:
            self.second_operand = self.second_operand if '%' in self.second_operand else self.second_operand + '%'
        else:
            self.first_operand = self.first_operand if '%' in self.first_operand else self.first_operand + '%'

        # Show changes on the screen
        self._detect_screen_changes()

    def add_operator(self, operator):
        # Move result to the firs operand and clear other states if an operator was pressed when the result is not empty
        self._result_to_first_operand()
        # Change operator
        self.operator = operator
        # Show changes on the screen
        self._detect_screen_changes()

    def inver_operand(self):
        # Move result to the firs operand and clear other states if the invert button was pressed when the result is not empty
        self._result_to_first_operand()

        if self.operator and '-' not in self.second_operand:
            self.second_operand = self._concat_values('-', self.second_operand)
        elif '-' not in self.first_operand:
            self.first_operand = self._concat_values('-', self.first_operand)

        # Show changes on the screen
        self._detect_screen_changes()

    def remove_last(self):
        # Move result to the firs operand and clear other states if the C button was pressed when the result is not empty
        self._result_to_first_operand()

        if self.second_operand:
            self.second_operand = self.second_operand[:-1]
        elif self.operator:
            self.operator = ''
        elif self.first_operand:
            self.first_operand = self.first_operand[:-1]

        # Show changes on the screen
        self._detect_screen_changes()

    def clear_all(self):
        self.first_operand = ''
        self.operator = ''
        self.second_operand = ''
        self.result = ''

        # Show changes on the screen
        self._detect_screen_changes()

    def get_result(self):
        # If '=' pressed when we already have a result (1+2=3 -> 3+2=5 ...)
        self.first_operand = self.result if self.result else self.first_operand
        # Check and convers percentages
        first, second = self._percentage_convert(self.first_operand, self.second_operand)
        self.first_operand = first
        self.second_operand = second

        case = {
            '+': float(self.first_operand) + float(self.second_operand),
            '-': float(self.first_operand) - float(self.second_operand),
            '×': float(self.first_operand) * float(self.second_operand),
            '÷': float(0) if self.second_operand == '0' else float(self.first_operand) / float(self.second_operand),
            'default': ''
        }

        # Get math results and round number to 8 symbols after the dot
        math_result = round(case.get(self.operator, 'default'), 8)
        # Remove .0 from the end of the number
        math_result = int(math_result) if math_result % 1 == 0 else math_result
        # Set result to the global state
        self.result = str(math_result)
        # Show changes on the screen
        self._detect_screen_changes()

    def _number_callback(self, number):
        return lambda: self.add_number(number)

    def _operand_callback(self, operand):
        return lambda: self.add_operator(operand)

    def _concat_values(self, first, second):
        # Convert to strings
        first = str(first)
        second = str(second)
        # Remove % from string
        new_first = first.rstrip('%') if '%' in first else first
        new_second = second.rstrip('%') if '%' in second else second
        # Add number
        result = str(new_first) + str(new_second)
        # Retunr % if needed
        result = result + '%' if '%' in first or '%' in second else result

        return result

    def _result_to_first_operand(self):
        if self.result:
            # Save the result value before cleaning
            sotred_result = self.result
            # Clear all states
            self.clear_all()
            # Add stored results to the first operator
            self.first_operand = sotred_result

    def _percentage_convert(self, *args):
        # Convert % value to decimal value
        converted_args = [str(float(arg.rstrip('%')) / 100) if '%' in arg else arg for arg in [*args]]
        return [*converted_args]

    def _detect_screen_changes(self):
        if self.result:
            self.main_input['text'] = self.result
        else:
            first_part = self.first_operand if len(self.first_operand) else ''
            second_part = ' ' + self.operator if len(self.first_operand) and len(self.operator) else ''
            third_part = ' ' + self.second_operand if len(self.first_operand) and len(self.operator) and len(self.second_operand) else ''

            self.main_input['text'] = first_part + second_part + third_part

    @staticmethod
    def start():
        root = tk.Tk()
        root.title('Calculator')
        root.iconbitmap('./assets/favicon.ico')
        root.resizable(width=False, height=False)
        Calculator(root)
        root.mainloop()


Calculator.start()
