from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QTableWidget, QTableWidgetItem, QComboBox,
    QMessageBox, QScrollArea, QFrame, QTextEdit
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
import csv
from PyQt5.QtWidgets import QFileDialog, QApplication


class PaymentTab(QWidget):
    def __init__(self, db_manager):
        super().__init__()
        self.db_manager = db_manager
        self.init_ui()
        self.load_payments()

    def init_ui(self):
        """Initialize payment tab UI"""
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        # Title
        title_label = QLabel("Manajemen Pembayaran")
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title_label.setFont(title_font)
        main_layout.addWidget(title_label)

        # Create scroll area for form
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setMaximumHeight(550)

        # Form container
        form_container = QWidget()
        form_layout = QVBoxLayout()
        form_container.setLayout(form_layout)

        # Form frame
        form_frame = QFrame()
        form_frame.setFrameStyle(QFrame.Box)
        form_frame.setLineWidth(1)
        form_frame_layout = QVBoxLayout()
        form_frame.setLayout(form_frame_layout)

        # Input fields
        input_layout = QHBoxLayout()

        # Customer name with clipboard integration
        name_layout = QVBoxLayout()
        name_layout.addWidget(QLabel("Nama Pelanggan:"))
        name_input_layout = QHBoxLayout()
        self.customer_name_input = QLineEdit()
        self.customer_name_input.setPlaceholderText("Masukkan nama pelanggan...")

        # Clipboard paste button (Requirement 1: QClipboard)
        self.paste_button = QPushButton("Paste dari Clipboard")
        self.paste_button.clicked.connect(self.paste_from_clipboard)

        name_input_layout.addWidget(self.customer_name_input)
        name_input_layout.addWidget(self.paste_button)
        name_layout.addLayout(name_input_layout)
        input_layout.addLayout(name_layout)

        # Total amount
        amount_layout = QVBoxLayout()
        amount_layout.addWidget(QLabel("Total Pembayaran:"))
        self.total_amount_input = QLineEdit()
        self.total_amount_input.setPlaceholderText("0")
        amount_layout.addWidget(self.total_amount_input)
        input_layout.addLayout(amount_layout)

        # Payment method
        method_layout = QVBoxLayout()
        method_layout.addWidget(QLabel("Metode Pembayaran:"))
        self.payment_method_combo = QComboBox()
        self.payment_method_combo.addItems([
            "Tunai", "Kartu Debit", "Kartu Kredit",
            "Transfer Bank", "E-Wallet", "QRIS"
        ])
        method_layout.addWidget(self.payment_method_combo)
        input_layout.addLayout(method_layout)

        form_frame_layout.addLayout(input_layout)

        # Notes field
        notes_layout = QVBoxLayout()
        notes_layout.addWidget(QLabel("Catatan:"))
        self.notes_input = QTextEdit()
        self.notes_input.setMaximumHeight(160)
        self.notes_input.setPlaceholderText("Catatan tambahan (opsional)...")
        notes_layout.addWidget(self.notes_input)
        form_frame_layout.addLayout(notes_layout)

        # Buttons
        button_layout = QHBoxLayout()
        self.add_button = QPushButton("Tambah Pembayaran")
        self.add_button.clicked.connect(self.add_payment)
        self.update_button = QPushButton("Update Pembayaran")
        self.update_button.clicked.connect(self.update_payment)
        self.update_button.setEnabled(False)
        self.clear_button = QPushButton("Bersihkan Form")
        self.clear_button.clicked.connect(self.clear_form)

        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.update_button)
        button_layout.addWidget(self.clear_button)
        button_layout.addStretch()

        form_frame_layout.addLayout(button_layout)
        form_layout.addWidget(form_frame)

        scroll_area.setWidget(form_container)
        main_layout.addWidget(scroll_area)

        # Table for payments
        self.payments_table = QTableWidget()
        self.payments_table.setColumnCount(7)
        self.payments_table.setHorizontalHeaderLabels([
            "ID", "Nama Pelanggan", "Total", "Metode Pembayaran",
            "Status", "Tanggal", "Catatan"
        ])

        # Table settings (Requirement 3: Scroll support)
        self.payments_table.setAlternatingRowColors(True)
        self.payments_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.payments_table.setSortingEnabled(True)
        self.payments_table.setHorizontalScrollMode(QTableWidget.ScrollPerPixel)
        self.payments_table.setVerticalScrollMode(QTableWidget.ScrollPerPixel)

        # Connect table selection
        self.payments_table.itemSelectionChanged.connect(self.on_payment_selected)

        main_layout.addWidget(self.payments_table)

        # Action buttons
        action_layout = QHBoxLayout()
        self.delete_button = QPushButton("Hapus Pembayaran")
        self.delete_button.clicked.connect(self.delete_payment)
        self.delete_button.setEnabled(False)

        self.export_button = QPushButton("Ekspor ke CSV")
        self.export_button.clicked.connect(self.export_to_csv)

        action_layout.addWidget(self.delete_button)
        action_layout.addStretch()
        action_layout.addWidget(self.export_button)

        main_layout.addLayout(action_layout)

    def paste_from_clipboard(self):
        """Paste text from clipboard to customer name field"""
        clipboard = QApplication.clipboard()
        clipboard_text = clipboard.text()
        if clipboard_text:
            self.customer_name_input.setText(clipboard_text)
            QMessageBox.information(self, "Sukses", "Teks berhasil di-paste dari clipboard!")
        else:
            QMessageBox.warning(self, "Peringatan", "Clipboard kosong!")

    def add_payment(self):
        """Add new payment record"""
        customer_name = self.customer_name_input.text().strip()
        total_amount = self.total_amount_input.text().strip()
        payment_method = self.payment_method_combo.currentText()
        notes = self.notes_input.toPlainText().strip()

        if not customer_name:
            QMessageBox.warning(self, "Error", "Nama pelanggan harus diisi!")
            return

        try:
            total_amount = float(total_amount)
            if total_amount <= 0:
                QMessageBox.warning(self, "Error", "Total pembayaran harus lebih dari 0!")
                return
        except ValueError:
            QMessageBox.warning(self, "Error", "Total pembayaran harus berupa angka!")
            return

        success = self.db_manager.add_payment(customer_name, total_amount, payment_method, notes)
        if success:
            QMessageBox.information(self, "Sukses", "Pembayaran berhasil ditambahkan!")
            self.clear_form()
            self.load_payments()
        else:
            QMessageBox.critical(self, "Error", "Gagal menambahkan pembayaran!")

    def update_payment(self):
        """Update selected payment record"""
        selected_row = self.payments_table.currentRow()
        if selected_row < 0:
            QMessageBox.warning(self, "Error", "Pilih pembayaran yang akan diupdate!")
            return

        payment_id = int(self.payments_table.item(selected_row, 0).text())
        customer_name = self.customer_name_input.text().strip()
        total_amount = self.total_amount_input.text().strip()
        payment_method = self.payment_method_combo.currentText()
        notes = self.notes_input.toPlainText().strip()

        if not customer_name:
            QMessageBox.warning(self, "Error", "Nama pelanggan harus diisi!")
            return

        try:
            total_amount = float(total_amount)
            if total_amount <= 0:
                QMessageBox.warning(self, "Error", "Total pembayaran harus lebih dari 0!")
                return
        except ValueError:
            QMessageBox.warning(self, "Error", "Total pembayaran harus berupa angka!")
            return

        success = self.db_manager.update_payment(payment_id, customer_name, total_amount, payment_method, notes)
        if success:
            QMessageBox.information(self, "Sukses", "Pembayaran berhasil diupdate!")
            self.clear_form()
            self.load_payments()
        else:
            QMessageBox.critical(self, "Error", "Gagal mengupdate pembayaran!")

    def delete_payment(self):
        """Delete selected payment record"""
        selected_row = self.payments_table.currentRow()
        if selected_row < 0:
            QMessageBox.warning(self, "Error", "Pilih pembayaran yang akan dihapus!")
            return

        payment_id = int(self.payments_table.item(selected_row, 0).text())
        customer_name = self.payments_table.item(selected_row, 1).text()

        reply = QMessageBox.question(
            self, "Konfirmasi Hapus",
            f"Apakah Anda yakin ingin menghapus pembayaran dari {customer_name}?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            success = self.db_manager.delete_payment(payment_id)
            if success:
                QMessageBox.information(self, "Sukses", "Pembayaran berhasil dihapus!")
                self.clear_form()
                self.load_payments()
            else:
                QMessageBox.critical(self, "Error", "Gagal menghapus pembayaran!")

    def clear_form(self):
        """Clear all form inputs"""
        self.customer_name_input.clear()
        self.total_amount_input.clear()
        self.payment_method_combo.setCurrentIndex(0)
        self.notes_input.clear()
        self.update_button.setEnabled(False)
        self.add_button.setEnabled(True)
        self.delete_button.setEnabled(False)

    def load_payments(self):
        """Load all payments into table"""
        payments = self.db_manager.get_payments()
        self.payments_table.setRowCount(len(payments))

        for row, payment in enumerate(payments):
            for col, data in enumerate(payment):
                if col == 2:  # Format currency
                    item = QTableWidgetItem(f"Rp {data:,.0f}")
                elif col == 5:  # Format date
                    item = QTableWidgetItem(str(data)[:19])  # Remove microseconds
                else:
                    item = QTableWidgetItem(str(data))

                if col == 0:  # Make ID read-only
                    item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)

                self.payments_table.setItem(row, col, item)

        # Resize columns to content
        self.payments_table.resizeColumnsToContents()

    def on_payment_selected(self):
        """Handle payment selection"""
        selected_row = self.payments_table.currentRow()
        if selected_row >= 0:
            # Fill form with selected payment data
            customer_name = self.payments_table.item(selected_row, 1).text()
            total_amount = self.payments_table.item(selected_row, 2).text()
            # Remove currency formatting
            total_amount = total_amount.replace("Rp ", "").replace(",", "")
            payment_method = self.payments_table.item(selected_row, 3).text()
            notes = self.payments_table.item(selected_row, 6).text() if self.payments_table.item(selected_row,
                                                                                                 6) else ""

            self.customer_name_input.setText(customer_name)
            self.total_amount_input.setText(total_amount)

            # Set combo box selection
            index = self.payment_method_combo.findText(payment_method)
            if index >= 0:
                self.payment_method_combo.setCurrentIndex(index)

            self.notes_input.setPlainText(notes)

            # Enable update and delete buttons
            self.update_button.setEnabled(True)
            self.add_button.setEnabled(False)
            self.delete_button.setEnabled(True)

    def search_payments(self, search_term):
        """Search payments by customer name or ID"""
        if search_term.strip():
            payments = self.db_manager.search_payments(search_term)
        else:
            payments = self.db_manager.get_payments()

        self.payments_table.setRowCount(len(payments))

        for row, payment in enumerate(payments):
            for col, data in enumerate(payment):
                if col == 2:  # Format currency
                    item = QTableWidgetItem(f"Rp {data:,.0f}")
                elif col == 5:  # Format date
                    item = QTableWidgetItem(str(data)[:19])
                else:
                    item = QTableWidgetItem(str(data))

                if col == 0:  # Make ID read-only
                    item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)

                self.payments_table.setItem(row, col, item)

        self.payments_table.resizeColumnsToContents()

    def export_to_csv(self):
        """Export payments to CSV file"""
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Simpan File CSV", "pembayaran_export.csv", "CSV Files (*.csv)"
        )

        if file_path:
            try:
                with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
                    writer = csv.writer(csvfile)

                    # Write headers
                    headers = ["ID", "Nama Pelanggan", "Total", "Metode Pembayaran",
                               "Status", "Tanggal", "Catatan"]
                    writer.writerow(headers)

                    # Write data
                    payments = self.db_manager.get_payments()
                    for payment in payments:
                        writer.writerow(payment)

                QMessageBox.information(self, "Sukses", f"Data berhasil diekspor ke {file_path}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Gagal mengekspor data: {str(e)}")