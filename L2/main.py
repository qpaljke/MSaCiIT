import re
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QTextEdit, QPushButton, QFileDialog


class JSCodeAnalyzerApp(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('JS Code Analyzer')
        self.setGeometry(100, 100, 600, 800)

        layout = QVBoxLayout()

        self.result_label = QLabel()
        layout.addWidget(self.result_label)

        self.text_edit = QTextEdit()
        layout.addWidget(self.text_edit)

        analyze_button = QPushButton('Parse')
        analyze_button.clicked.connect(self.analyze_code)
        layout.addWidget(analyze_button)

        load_button = QPushButton('Load Code from File')
        load_button.clicked.connect(self.load_code_from_file)
        layout.addWidget(load_button)

        self.setLayout(layout)

    def analyze_code(self):
        js_code = self.text_edit.toPlainText()

        operators_len = len(self.calculate_operators(js_code)) + len(self.parse_js_code(js_code))
        conditional_operators_len = len(self.find_conditional_operators(js_code))
        case_operator_len = self.count_matches(js_code)
        print(operators_len, conditional_operators_len, case_operator_len)

        result_text = f"CL: {conditional_operators_len}\n" \
                      f"cl: {round(conditional_operators_len / (operators_len + case_operator_len), 3)}\n" \
                      f"CLI: {self.max_nested_level(js_code)}"

        self.result_label.setText(result_text)

    def load_code_from_file(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, 'Load Code from File', '', 'JavaScript Files (*.js);;All Files (*)')

        if file_path:
            with open(file_path, 'r') as file:
                code_content = file.read()
                self.text_edit.setPlainText(code_content)

    def calculate_operators(self, code):
        operators_pattern = re.compile(r'\b(?:\s*for\s*|\s*while\s*|\s*if\s*|\s*else\s*|\s*switch\s*|\s*else if\s*|\s*do\s*)\b')
        print(operators_pattern.findall(code))
        return re.findall(operators_pattern, code)

    def find_conditional_operators(self, code):
        conditional_pattern = re.compile(r'\b(?:if|switch|case|while|for|do)\b')
        return conditional_pattern.findall(code)

    def count_matches(self, code):
        match_counter = 0
        for line in code.split('\n'):
            if 'case ' in line:
                match_counter += 1
        return match_counter

    def max_nested_level(self, js_code):
        max_level = 0
        current_level = 0

        for char in js_code:
            if char == '{':
                current_level += 1
                max_level = max(max_level, current_level)
            elif char == '}':
                current_level -= 1

        return max_level - 1

    def parse_js_code(self, js_code):
        pattern = r"\+\+|--|===|!==|==|!=|<=|>=|&&|\|\||\+=|-=|\*=|\/=|%=\*\*=|<<=|>>=|>>>=|&=|\|=|\^=|(?<![\+\-*/=()])=(?!=)|[+\-*/%&|^<>~!]"
        operators = re.findall(pattern, js_code)
        print(operators)
        return operators


if __name__ == '__main__':
    app = QApplication([])
    window = JSCodeAnalyzerApp()
    window.show()
    app.exec_()
