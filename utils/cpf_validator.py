"""
Module that contain a class to validate CPF client
"""

from dataclasses import dataclass


@dataclass
class CpfValidator:
    """
    Class to validate CPF client.
    :param cpf:
    :return: None.
    :rtype: none.
    """
    cpf: str

    def is_valid(self):
        """
        Method to validate CPF client.
        :return: bool.
        :rtype: bool.
        """
        if len(self.cpf) != 11 or not self.cpf.isnumeric():
            return False
        # first digit
        cont = 0
        for index, digit in enumerate(self.cpf[:9]):
            cont += int(digit) * (index + 1)
        rest = cont % 11
        if rest == 10:
            rest = 0
        if str(rest) != self.cpf[9:10]:
            return False
        # second digit
        cont = 0
        for index, digit in enumerate(self.cpf[:10]):
            cont += int(digit) * index
        rest = cont % 11
        if rest == 10:
            rest = 0
        if str(rest) != self.cpf[10:11]:
            return False
        return True
