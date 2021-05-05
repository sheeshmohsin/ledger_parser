from datetime import datetime


class Validator:

    def __init__(self, line=[]):
        self.line = line

    def validate_date(self, data):
        data = datetime.strptime(data.strip(), '%Y-%m-%d').date()
        return data

    def validate_str(self, data):
        data = data.strip()
        if data:
            return data.lower()
        else:
            raise ValueError("Invalid String")

    def validate_float(self, data):
        data = float(data)
        if data:
            return data
        else:
            raise ValueError("Invalid Amount")

    def validate(self):
        data = self.line
        start = 0
        i = 0
        char_count = 1
        line = []
        for char in data:
            if char == ',':
                if char_count == 1:
                    val = self.validate_date(data[start:i])
                elif char_count == 2 or char_count == 3:
                    val = self.validate_str(data[start:i])
                char_count += 1
                start = i+1
                line.append(val)
            elif char_count > 3:
                val = self.validate_float(data[start:len(data)])
                line.append(val)
                break
            i += 1
        self.line = line

    @property
    def validated_data(self):
        self.validated_line = {
            'transaction_date': self.line[0],
            'payer': self.line[1],
            'payee': self.line[2],
            'amount': self.line[3]
        }
        return self.validated_line
