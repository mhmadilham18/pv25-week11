from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QTableWidget, QTableWidgetItem, QDateEdit, QGroupBox,
    QMessageBox, QFileDialog, QFrame
)
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtGui import QFont
import csv
import pandas as pd
from datetime import datetime
import os


class ReportTab(QWidget):
    def __init__(self, db_manager):
        super().__init__()
        self.db_manager = db_manager
        self.init_ui()
        self.load_reports()

    def init_ui(self):
        """Initialize report tab UI"""
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        # Title
        title_label = QLabel("Laporan Penjualan")
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title_label.setFont(title_font)
        main_layout.addWidget(title_label)

        # Summary section
        summary_group = QGroupBox("Ringkasan Hari Ini")
        summary_layout = QHBoxLayout()
        summary_group.setLayout(summary_layout)

        # Summary labels
        self.total_transactions_label = QLabel("Total Transaksi: 0")
        self.total_revenue_label = QLabel("Total Pendapatan: Rp 0")
        self.avg_transaction_label = QLabel("Rata-rata per Transaksi: Rp 0")

        summary_layout.addWidget(self.total_transactions_label)
        summary_layout.addWidget(self.total_revenue_label)
        summary_layout.addWidget(self.avg_transaction_label)
        summary_layout.addStretch()

        main_layout.addWidget(summary_group)

        # Date filter section
        filter_group = QGroupBox("Filter Tanggal")
        filter_layout = QHBoxLayout()
        filter_group.setLayout(filter_layout)

        filter_layout.addWidget(QLabel("Tanggal:"))
        self.date_edit = QDateEdit()
        self.date_edit.setDate(QDate.currentDate())
        self.date_edit.setCalendarPopup(True)
        filter_layout.addWidget(self.date_edit)

        self.filter_button = QPushButton("Filter")
        self.filter_button.clicked.connect(self.filter_by_date)
        filter_layout.addWidget(self.filter_button)

        self.reset_button = QPushButton("Reset")
        self.reset_button.clicked.connect(self.reset_filter)
        filter_layout.addWidget(self.reset_button)

        filter_layout.addStretch()

        main_layout.addWidget(filter_group)

        # Transactions table
        table_label = QLabel("Detail Transaksi")
        table_font = QFont()
        table_font.setPointSize(12)
        table_font.setBold(True)
        table_label.setFont(table_font)
        main_layout.addWidget(table_label)

        self.report_table = QTableWidget()
        self.report_table.setColumnCount(7)
        self.report_table.setHorizontalHeaderLabels([
            "ID", "Nama Pelanggan", "Total", "Metode Pembayaran",
            "Status", "Tanggal", "Catatan"
        ])

        # Table settings
        self.report_table.setAlternatingRowColors(True)
        self.report_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.report_table.setSortingEnabled(True)
        self.report_table.setHorizontalScrollMode(QTableWidget.ScrollPerPixel)
        self.report_table.setVerticalScrollMode(QTableWidget.ScrollPerPixel)

        main_layout.addWidget(self.report_table)

        # Export buttons
        export_layout = QHBoxLayout()
        self.export_csv_button = QPushButton("Ekspor ke CSV")
        self.export_csv_button.clicked.connect(self.export_to_csv)

        self.export_excel_button = QPushButton("Ekspor ke Excel")
        self.export_excel_button.clicked.connect(self.export_to_excel)

        self.export_report_button = QPushButton("Ekspor Laporan Lengkap")
        self.export_report_button.clicked.connect(self.export_report)

        export_layout.addStretch()
        export_layout.addWidget(self.export_csv_button)
        export_layout.addWidget(self.export_excel_button)
        export_layout.addWidget(self.export_report_button)

        main_layout.addLayout(export_layout)

    def load_reports(self):
        """Load all payment reports"""
        payments = self.db_manager.get_payments()
        self.report_table.setRowCount(len(payments))

        total_amount = 0

        for row, payment in enumerate(payments):
            for col, data in enumerate(payment):
                if col == 2:  # Format currency
                    item = QTableWidgetItem(f"Rp {data:,.0f}")
                    total_amount += data
                elif col == 5:  # Format date
                    item = QTableWidgetItem(str(data)[:19])
                else:
                    item = QTableWidgetItem(str(data))

                self.report_table.setItem(row, col, item)

        # Update summary
        self.update_summary(len(payments), total_amount)

        # Resize columns to content
        self.report_table.resizeColumnsToContents()

    def filter_by_date(self):
        """Filter transactions by selected date"""
        selected_date = self.date_edit.date().toString("yyyy-MM-dd")
        daily_report = self.db_manager.get_daily_report(selected_date)

        # Get all payments for the selected date
        self.db_manager.cursor.execute("""
            SELECT id, customer_name, total_amount, payment_method, 
                   payment_status, order_date, notes
            FROM payments
            WHERE DATE(order_date) = ?
            ORDER BY order_date DESC
        """, (selected_date,))

        payments = self.db_manager.cursor.fetchall()
        self.report_table.setRowCount(len(payments))

        total_amount = 0

        for row, payment in enumerate(payments):
            for col, data in enumerate(payment):
                if col == 2:  # Format currency
                    item = QTableWidgetItem(f"Rp {data:,.0f}")
                    total_amount += data
                elif col == 5:  # Format date
                    item = QTableWidgetItem(str(data)[:19])
                else:
                    item = QTableWidgetItem(str(data))

                self.report_table.setItem(row, col, item)

        # Update summary with filtered data
        self.update_summary(len(payments), total_amount)
        self.report_table.resizeColumnsToContents()

    def reset_filter(self):
        """Reset filter and show all transactions"""
        self.date_edit.setDate(QDate.currentDate())
        self.load_reports()

    def update_summary(self, count, total):
        """Update summary labels"""
        avg = total / count if count > 0 else 0

        self.total_transactions_label.setText(f"Total Transaksi: {count}")
        self.total_revenue_label.setText(f"Total Pendapatan: Rp {total:,.0f}")
        self.avg_transaction_label.setText(f"Rata-rata per Transaksi: Rp {avg:,.0f}")

    def export_to_csv(self):
        """Export current table data to CSV"""
        try:
            # Get file path from user
            file_path, _ = QFileDialog.getSaveFileName(
                self,
                "Simpan Laporan CSV",
                f"laporan_transaksi_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                "CSV Files (*.csv)"
            )

            if not file_path:
                return

            # Get current table data
            rows = self.report_table.rowCount()
            cols = self.report_table.columnCount()

            # Prepare data
            data = []
            headers = []

            # Get headers
            for col in range(cols):
                headers.append(self.report_table.horizontalHeaderItem(col).text())

            data.append(headers)

            # Get data rows
            for row in range(rows):
                row_data = []
                for col in range(cols):
                    item = self.report_table.item(row, col)
                    if item:
                        row_data.append(item.text())
                    else:
                        row_data.append("")
                data.append(row_data)

            # Write to CSV
            with open(file_path, 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerows(data)

            QMessageBox.information(self, "Sukses", f"Data berhasil diekspor ke {file_path}")

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Gagal mengekspor data: {str(e)}")

    def export_to_excel(self):
        """Export current table data to Excel"""
        try:
            # Get file path from user
            file_path, _ = QFileDialog.getSaveFileName(
                self,
                "Simpan Laporan Excel",
                f"laporan_transaksi_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                "Excel Files (*.xlsx)"
            )

            if not file_path:
                return

            # Get current table data
            rows = self.report_table.rowCount()
            cols = self.report_table.columnCount()

            # Prepare data for DataFrame
            data = []
            headers = []

            # Get headers
            for col in range(cols):
                headers.append(self.report_table.horizontalHeaderItem(col).text())

            # Get data rows
            for row in range(rows):
                row_data = []
                for col in range(cols):
                    item = self.report_table.item(row, col)
                    if item:
                        # Clean currency formatting for Excel
                        text = item.text()
                        if col == 2 and text.startswith("Rp "):  # Total column
                            # Remove "Rp " and commas, convert to number
                            clean_number = text.replace("Rp ", "").replace(",", "")
                            try:
                                row_data.append(float(clean_number))
                            except ValueError:
                                row_data.append(text)
                        else:
                            row_data.append(text)
                    else:
                        row_data.append("")
                data.append(row_data)

            # Create DataFrame and export
            df = pd.DataFrame(data, columns=headers)
            df.to_excel(file_path, index=False, engine='openpyxl')

            QMessageBox.information(self, "Sukses", f"Data berhasil diekspor ke {file_path}")

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Gagal mengekspor data: {str(e)}")

    def export_report(self):
        """Export comprehensive report with summary and details"""
        try:
            # Get file path from user
            file_path, _ = QFileDialog.getSaveFileName(
                self,
                "Simpan Laporan Lengkap",
                f"laporan_lengkap_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                "Excel Files (*.xlsx)"
            )

            if not file_path:
                return

            # Create Excel writer
            with pd.ExcelWriter(file_path, engine='openpyxl') as writer:

                # Sheet 1: Summary Report
                summary_data = {
                    'Keterangan': [
                        'Total Transaksi',
                        'Total Pendapatan',
                        'Rata-rata per Transaksi',
                        'Tanggal Generate Laporan'
                    ],
                    'Nilai': [
                        self.total_transactions_label.text().split(': ')[1],
                        self.total_revenue_label.text().split(': ')[1],
                        self.avg_transaction_label.text().split(': ')[1],
                        datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    ]
                }

                summary_df = pd.DataFrame(summary_data)
                summary_df.to_excel(writer, sheet_name='Ringkasan', index=False)

                # Sheet 2: Detailed Transactions
                rows = self.report_table.rowCount()
                cols = self.report_table.columnCount()

                headers = []
                for col in range(cols):
                    headers.append(self.report_table.horizontalHeaderItem(col).text())

                data = []
                for row in range(rows):
                    row_data = []
                    for col in range(cols):
                        item = self.report_table.item(row, col)
                        if item:
                            text = item.text()
                            if col == 2 and text.startswith("Rp "):  # Total column
                                clean_number = text.replace("Rp ", "").replace(",", "")
                                try:
                                    row_data.append(float(clean_number))
                                except ValueError:
                                    row_data.append(text)
                            else:
                                row_data.append(text)
                        else:
                            row_data.append("")
                    data.append(row_data)

                detail_df = pd.DataFrame(data, columns=headers)
                detail_df.to_excel(writer, sheet_name='Detail Transaksi', index=False)

                # Sheet 3: Daily Summary (if filtered by date)
                if hasattr(self, 'current_filter_date'):
                    daily_summary = self.get_daily_summary()
                    daily_df = pd.DataFrame(daily_summary)
                    daily_df.to_excel(writer, sheet_name='Ringkasan Harian', index=False)

            QMessageBox.information(self, "Sukses", f"Laporan lengkap berhasil diekspor ke {file_path}")

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Gagal mengekspor laporan: {str(e)}")

    def get_daily_summary(self):
        """Get daily summary data for export"""
        try:
            # Get daily statistics from database
            self.db_manager.cursor.execute("""
                SELECT 
                    DATE(order_date) as tanggal,
                    COUNT(*) as total_transaksi,
                    SUM(total_amount) as total_pendapatan,
                    AVG(total_amount) as rata_rata,
                    payment_method,
                    COUNT(*) as jumlah_per_metode
                FROM payments
                GROUP BY DATE(order_date), payment_method
                ORDER BY tanggal DESC, payment_method
            """)

            results = self.db_manager.cursor.fetchall()

            summary_data = []
            for result in results:
                summary_data.append({
                    'Tanggal': result[0],
                    'Total Transaksi': result[1],
                    'Total Pendapatan': f"Rp {result[2]:,.0f}",
                    'Rata-rata': f"Rp {result[3]:,.0f}",
                    'Metode Pembayaran': result[4],
                    'Jumlah per Metode': result[5]
                })

            return summary_data

        except Exception as e:
            print(f"Error getting daily summary: {e}")
            return []

    def get_current_table_data(self):
        """Get current table data for other components"""
        rows = self.report_table.rowCount()
        cols = self.report_table.columnCount()

        data = []
        headers = []

        # Get headers
        for col in range(cols):
            headers.append(self.report_table.horizontalHeaderItem(col).text())

        # Get data
        for row in range(rows):
            row_data = []
            for col in range(cols):
                item = self.report_table.item(row, col)
                if item:
                    row_data.append(item.text())
                else:
                    row_data.append("")
            data.append(row_data)

        return {'headers': headers, 'data': data}