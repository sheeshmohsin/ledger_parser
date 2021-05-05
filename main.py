from src.validators import Validator
from src.passbook import Passbook

import os
import pathlib


class Main:

    def __init__(self):
        self.lines = []
        self.invalid_lines = []

    def read_file(self):
        dir_path = pathlib.Path(__file__).parent.absolute()
        csv_file_path = os.path.join(dir_path, 'data.csv')
        with open(csv_file_path) as csv_file:
            for line in csv_file:
                self._process_line(line)
        return self.lines

    def _process_line(self, line):
        if line:
            try:
                obj = Validator(line)
                obj.validate()
                line = obj.validated_data
                self.lines.append(line)
            except ValueError as e:
                self.invalid_lines.append(line)
                print('\n', e, '-> ', line)

    def _search(self, array, date):
        i = 0
        l = len(array)
        idx = None
        for x in array:
            if date == x['transaction_date']:
                idx = i
                break
            elif date < x['transaction_date']:
                idx = i
                break
            elif date > x['transaction_date']:
                pass
            i += 1
        if l == i:
            return -1
        else:
            return idx

    def take_input(self):
        e = True
        while e:
            q1 = input("Enter person name to know their balance: ")
            q2 = input("Enter date in format (YYYY-MM-DD) to know balance of specific date, Ignore if you want to know only current balance: ")
            obj = Validator()
            if q1:
                q1 = obj.validate_str(q1)
            if q2:
                q2 = obj.validate_date(q2)
            if q1:
                q1 = q1.lower()
                if not passbooks.get(q1, None):
                    print("Name not found.\n")
                else:
                    balance = passbooks[q1][-1]['balance']
                    if q2:
                        idx = self._search(passbooks[q1], q2)
                        if idx == 0 or idx == -1:
                            balance = passbooks[q1][idx]['balance']
                        else:
                            balance = passbooks[q1][idx - 1]['balance']
            yield q1, balance
                    

if __name__ == '__main__':
    main_obj = Main()
    lines = main_obj.read_file()
    obj = Passbook(lines)
    passbooks = obj.execute()
    for q1, balance in main_obj.take_input():
        print("%s's Balance is %d\n" % (q1, balance))
