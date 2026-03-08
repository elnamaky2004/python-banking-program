from PyQt5.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QApplication, QPushButton,
    QHBoxLayout, QCheckBox, QLineEdit, QTableWidget, QTableWidgetItem,
    QDoubleSpinBox, QSpinBox, QGridLayout, QFrame
)
from PyQt5.QtCore import Qt
import sys
import theme


def _make_theme_switch(parent: QWidget):
    try:
        return theme.AnimatedToggleSwitch(parent)
    except Exception:
        fallback = QCheckBox(parent)
        fallback.setCursor(Qt.PointingHandCursor)
        return fallback


class LoanCalculator(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Loan Calculator")
        self.setGeometry(100, 100, 800, 600)
        
        self.init_ui()
        
        theme.sync_checkbox_to_theme(self.mode_switch)
        self.mode_label.setText(theme.theme_text())

    def init_ui(self):
        # Theme mode section
        self.mode_label = QLabel(theme.theme_text(), self)
        self.mode_label.setObjectName("modeLabel")

        self.mode_switch = _make_theme_switch(self)
        self.mode_switch.toggled.connect(self.toggle_mode)

        mode_row = QHBoxLayout()
        mode_row.addStretch()
        mode_row.addWidget(self.mode_label)
        mode_row.addWidget(self.mode_switch)

        # Title
        title = QLabel("Loan Calculator", self)
        title.setObjectName("title")
        title.setAlignment(Qt.AlignCenter)

        # Input section using Grid Layout
        input_frame = QFrame(self)
        input_layout = QGridLayout(input_frame)
        input_layout.setSpacing(15)

        # Loan Amount
        loan_label = QLabel("Loan Amount ($):", self)
        self.loan_input = QDoubleSpinBox(self)
        self.loan_input.setRange(0, 1000000)
        self.loan_input.setValue(10000)
        self.loan_input.setDecimals(2)
        self.loan_input.setMinimumWidth(150)
        
        # Number of Instalments
        instalments_label = QLabel("Instalments:", self)
        self.instalments_input = QSpinBox(self)
        self.instalments_input.setRange(1, 360)
        self.instalments_input.setValue(12)
        self.instalments_input.setMinimumWidth(150)

        # Interest Rate
        rate_label = QLabel("Interest Rate (%):", self)
        self.rate_input = QDoubleSpinBox(self)
        self.rate_input.setRange(0, 100)
        self.rate_input.setValue(5.0)
        self.rate_input.setDecimals(2)
        self.rate_input.setMinimumWidth(150)

        # Calculate button
        calculate_button = QPushButton("Calculate", self)
        calculate_button.clicked.connect(self.calculate_loan)

        # Add widgets to grid layout
        input_layout.addWidget(loan_label, 0, 0, Qt.AlignRight)
        input_layout.addWidget(self.loan_input, 0, 1)
        input_layout.addWidget(instalments_label, 0, 2, Qt.AlignRight)
        input_layout.addWidget(self.instalments_input, 0, 3)
        input_layout.addWidget(rate_label, 1, 0, Qt.AlignRight)
        input_layout.addWidget(self.rate_input, 1, 1)
        input_layout.addWidget(calculate_button, 1, 2, 1, 2)

        input_layout.setColumnStretch(1, 1)
        input_layout.setColumnStretch(3, 1)

        # Results table
        self.results_table = QTableWidget(self)
        self.results_table.setColumnCount(4)
        self.results_table.setHorizontalHeaderLabels([
            "Instalment #", 
            "Amount ($)", 
            "Interest ($)", 
            "Principal ($)"
        ])
        self.results_table.setColumnWidth(0, 100)
        self.results_table.setColumnWidth(1, 150)
        self.results_table.setColumnWidth(2, 150)
        self.results_table.setColumnWidth(3, 150)

        # Summary section
        summary_frame = QFrame(self)
        summary_layout = QGridLayout(summary_frame)
        summary_layout.setSpacing(20)

        self.total_interest_label = QLabel("Total Interest: $0.00", self)
        self.total_amount_label = QLabel("Total Amount: $0.00", self)
        self.monthly_payment_label = QLabel("Payment per Instalment: $0.00", self)
        
        self.total_interest_label.setAlignment(Qt.AlignCenter)
        self.total_amount_label.setAlignment(Qt.AlignCenter)
        self.monthly_payment_label.setAlignment(Qt.AlignCenter)
        
        summary_layout.addWidget(self.total_interest_label, 0, 0)
        summary_layout.addWidget(self.total_amount_label, 0, 1)
        summary_layout.addWidget(self.monthly_payment_label, 0, 2)
        summary_layout.setColumnStretch(0, 1)
        summary_layout.setColumnStretch(1, 1)
        summary_layout.setColumnStretch(2, 1)

        # Schedule label
        schedule_label = QLabel("Payment Schedule:", self)

        # Main layout
        main_layout = QVBoxLayout()
        main_layout.addLayout(mode_row)
        main_layout.addWidget(title)
        main_layout.addSpacing(10)
        main_layout.addWidget(input_frame)
        main_layout.addSpacing(10)
        main_layout.addWidget(schedule_label)
        main_layout.addWidget(self.results_table)
        main_layout.addSpacing(10)
        main_layout.addWidget(summary_frame)

        self.setLayout(main_layout)

    def calculate_loan(self):
        """Calculate loan instalments with interest"""
        principal = self.loan_input.value()
        num_instalments = self.instalments_input.value()
        annual_rate = self.rate_input.value()
        
        if principal <= 0 or num_instalments <= 0:
            return
        
        # Convert annual rate to monthly (if annual rate is provided)
        monthly_rate = (annual_rate / 100) / 12
        
        # Calculate monthly payment using the formula:
        # M = P * [r(1+r)^n] / [(1+r)^n - 1]
        if monthly_rate == 0:
            monthly_payment = principal / num_instalments
        else:
            numerator = monthly_rate * (1 + monthly_rate) ** num_instalments
            denominator = (1 + monthly_rate) ** num_instalments - 1
            monthly_payment = principal * (numerator / denominator)
        
        # Clear previous results
        self.results_table.setRowCount(0)
        
        remaining_balance = principal
        total_interest = 0
        
        # Calculate and populate each instalment
        for i in range(1, num_instalments + 1):
            interest_payment = remaining_balance * monthly_rate if monthly_rate > 0 else 0
            principal_payment = monthly_payment - interest_payment
            
            # Adjust last payment to account for rounding
            if i == num_instalments:
                principal_payment = remaining_balance
                interest_payment = monthly_payment - principal_payment
            
            remaining_balance -= principal_payment
            total_interest += interest_payment
            
            # Add row to table
            row_position = self.results_table.rowCount()
            self.results_table.insertRow(row_position)
            
            self.results_table.setItem(row_position, 0, QTableWidgetItem(str(i)))
            self.results_table.setItem(row_position, 1, QTableWidgetItem(f"${monthly_payment:.2f}"))
            self.results_table.setItem(row_position, 2, QTableWidgetItem(f"${interest_payment:.2f}"))
            self.results_table.setItem(row_position, 3, QTableWidgetItem(f"${principal_payment:.2f}"))
        
        # Update summary
        total_amount = principal + total_interest
        self.total_interest_label.setText(f"Total Interest: ${total_interest:.2f}")
        self.total_amount_label.setText(f"Total Amount: ${total_amount:.2f}")
        self.monthly_payment_label.setText(f"Payment per Instalment: ${monthly_payment:.2f}")

    def toggle_mode(self):
        """Toggle between light and dark theme"""
        theme.set_global_theme(self.mode_switch.isChecked())
        self.mode_label.setText(theme.theme_text())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    theme.set_global_theme(False)
    
    calculator = LoanCalculator()
    calculator.show()
    sys.exit(app.exec_())
