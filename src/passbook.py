class Passbook:

    def __init__(self, lines):
        self.lines = lines
        self.passbooks = dict()

    def initialize(self, line):
        if not self.passbooks.get(line['payer'], None):
            self.passbooks[line['payer']] = [
                {
                    'transaction_date': line['transaction_date'],
                    'amount_type': 'initial',
                    'payee': 'initial',
                    'amount': 0.00,
                    'balance': 0.00
                }
            ]
        if not self.passbooks.get(line['payee'], None):
            self.passbooks[line['payee']] = [
                {
                    'transaction_date': line['transaction_date'],
                    'amount_type': 'initial',
                    'payee': 'initial',
                    'amount': 0.00,
                    'balance': 0.00
                }
            ]

    def debit(self, line):
        last_transaction = self.passbooks[line['payer']][-1]
        self.passbooks[line['payer']].append(
            {
                'transaction_date': line['transaction_date'],
                'amount_type': 'debit',
                'counterparty': line['payee'],
                'amount': line['amount'],
                'balance': last_transaction['balance'] - line['amount']
            }
        )

    def credit(self, line):
        last_transaction = self.passbooks[line['payee']][-1]
        self.passbooks[line['payee']].append(
            {
                'transaction_date': line['transaction_date'],
                'amount_type': 'credit',
                'counterparty': line['payer'],
                'amount': line['amount'],
                'balance': last_transaction['balance'] + line['amount']
            }
        )

    def execute(self):
        for line in self.lines:
            self.initialize(line)
            self.credit(line)
            self.debit(line)
        return self.passbooks
