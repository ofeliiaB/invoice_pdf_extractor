import re
import pdfplumber


class Extractor:

    def __init__(self, filename, input_currency_symbol):
        self.filename = filename
        self.input_currency_symbol = input_currency_symbol

    def open_file(self):
        with pdfplumber.open(f"files/{self.filename}") as pdf:
            page = pdf.pages[0]
            words = page.extract_words()
        return words

    def get_currency_sign(self):
        currency_symbols = ["€", "$", "£", "Kč"]
        sign = None
        for i in range(len(currency_symbols)):
            if self.input_currency_symbol == currency_symbols[i]:
                sign = currency_symbols[i]
        return sign

    @staticmethod
    def extract_all_invoice_lines(words_info_dict):

        """
        groups text data based on top coordinate in the words dictionary
        returns a dictionary where key = top coordinate,
        value = all text characters on that coordinate
        :param words_info_dict: dict
        :return: dict
        """
        top_coordinate_txt_dict = dict()
        for word in words_info_dict:
            if float(word["top"]) not in top_coordinate_txt_dict:
                top_coordinate_txt_dict[float(word["top"])] = word["text"]
            else:
                top_coordinate_txt_dict[float(word["top"])] = top_coordinate_txt_dict[float(word["top"])] + " " + \
                                                              word["text"]
        return top_coordinate_txt_dict

    @staticmethod
    def get_txt_on_same_line(top_coordinate_txt_dict):

        """
        finds lines that are close to each other (not far than 2) and processes them as one line
        returns a set of lines of all text in the invoice
        :param top_coordinate_txt_dict: dict
        :return: set
        """

        def get_key(input_dict, val):
            for key, value in input_dict.items():
                if val == value:
                    return key
            return "no such key"

        keys, values = top_coordinate_txt_dict.keys(), top_coordinate_txt_dict.values()

        same_line = dict()
        for i in keys:
            for v in values:
                k = get_key(top_coordinate_txt_dict, v)
                if abs(i - k) <= 1.8:
                    if i not in same_line:
                        same_line[i] = v
                    else:
                        same_line[i] = same_line[i] + " " + v

        same_lines = set(same_line.values())
        return same_lines

    def extract_item_lines(self, on_same_line_strings, currency_sign):

        """
        takes in all text lines in the invoice and returns only the lines about items
        the item line is identified based on use of currency sign
        works for use cases where item details in the invoice contain unit price
        and total price, therefore, the currency sybmol is present more than once
        :param on_same_line_strings: set / list
        :return: list
        """
        item_lines = [line for line in on_same_line_strings if line.count(currency_sign) > 1]
        return item_lines

    def structure_final_result(self, item_lines, currency_sign):

        """
        structures details about invoice items into a list of dictionaries
        :param item_lines: list
        :return: list
        """
        result = []
        for item_line in item_lines:
            output = dict()
            pattern = rf"[\?{currency_sign}]?K?č?\d*,?\d+?\.\d+"
            price = re.findall(pattern, item_line)
            if len(price) > 0:
                description = " ".join(re.findall("[a-zA-Z]+[^Kč]", item_line))
                quantity = re.findall("\d+", item_line)[0]
                unit_price = price[0]
                total_price = price[1]
                output["description"] = description
                output["quantity"] = int(quantity)
                output["unit_price"] = unit_price
                output["total_price"] = total_price
                result.append(output)
        return result

    def extract_structured_data(self):
        """
        orders and runs all the methods of the Extractor
        :return: list
        """
        words = self.open_file()
        top_coordinate_txt = self.extract_all_invoice_lines(words_info_dict=words)
        same_lines_lst = self.get_txt_on_same_line(top_coordinate_txt_dict=top_coordinate_txt)
        currency_sign = self.get_currency_sign()
        items_line = self.extract_item_lines(on_same_line_strings=same_lines_lst, currency_sign=currency_sign)
        result = self.structure_final_result(item_lines=items_line, currency_sign=currency_sign)
        return result


if __name__ == "__main__":
    # delete this, the code is here just for testing purposes
    # input_currency_symbol = "Kč"
    input_currency_symbol = "$"
    e = Extractor("sample_invoice.pdf", input_currency_symbol)
    result = e.extract_structured_data()
    print(result)
