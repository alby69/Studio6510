from PySide6.QtGui import QSyntaxHighlighter, QTextCharFormat, QColor, QFont
from PySide6.QtCore import QRegularExpression

class ASMHighlighter(QSyntaxHighlighter):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.highlighting_rules = []

        # Instructions (6502)
        instruction_format = QTextCharFormat()
        instruction_format.setForeground(QColor("#569cd6"))
        instruction_format.setFontWeight(QFont.Bold)
        instructions = [
            "LDA", "LDX", "LDY", "STA", "STX", "STY",
            "INC", "DEC", "INX", "DEX", "INY", "DEY",
            "ADC", "SBC", "CMP", "CPX", "CPY",
            "JMP", "JSR", "RTS", "RTI",
            "BCC", "BCS", "BEQ", "BMI", "BNE", "BPL", "BVC", "BVS",
            "CLC", "CLD", "CLI", "CLV", "SEC", "SED", "SEI",
            "PHA", "PHP", "PLA", "PLP", "TAX", "TAY", "TSX", "TXA", "TXS", "TYA",
            "AND", "ORA", "EOR", "BIT", "ASL", "LSR", "ROL", "ROR",
            "NOP", "BRK"
        ]
        for instr in instructions:
            pattern = QRegularExpression(rf"\b{instr}\b", QRegularExpression.CaseInsensitiveOption)
            self.highlighting_rules.append((pattern, instruction_format))

        # Directives
        directive_format = QTextCharFormat()
        directive_format.setForeground(QColor("#c586c0"))
        directives = ["!byte", "!word", "!bin", "*=", ".byte", ".word", ".org"]
        for direct in directives:
            pattern = QRegularExpression(rf"{QRegularExpression.escape(direct)}\b", QRegularExpression.CaseInsensitiveOption)
            self.highlighting_rules.append((pattern, directive_format))

        # Comments
        comment_format = QTextCharFormat()
        comment_format.setForeground(QColor("#6a9955"))
        self.highlighting_rules.append((QRegularExpression(";.*"), comment_format))

        # Numbers (Hex, Dec, Bin)
        number_format = QTextCharFormat()
        number_format.setForeground(QColor("#b5cea8"))
        self.highlighting_rules.append((QRegularExpression(r"\$[0-9a-fA-F]+"), number_format)) # Hex
        self.highlighting_rules.append((QRegularExpression(r"#[0-9]+"), number_format))      # Immediate Dec
        self.highlighting_rules.append((QRegularExpression(r"%[01]+"), number_format))       # Bin

    def highlightBlock(self, text):
        for pattern, format in self.highlighting_rules:
            match_iterator = pattern.globalMatch(text)
            while match_iterator.hasNext():
                match = match_iterator.next()
                self.setFormat(match.capturedStart(), match.capturedLength(), format)
