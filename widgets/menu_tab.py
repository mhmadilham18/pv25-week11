from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QTableWidget, QTableWidgetItem, QComboBox,
    QMessageBox, QScrollArea, QFrame, QTextEdit, QCheckBox
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
import csv
from PyQt5.QtWidgets import QFileDialog


class MenuTab(QWidget):
    def __init__(self, db_manager):
        super().__init__()
        self.db_manager = db_manager
        self.init_ui()
        self.load_menu_items()

    def init_ui(self):
        """Initialize menu tab UI"""
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        # Title
        title_label = QLabel("Manajemen Menu")
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title_label.setFont(title_font)
        main_layout.addWidget(title_label)

        # Create scroll area for form (Requirement 4: QScrollArea)
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setMaximumHeight(450)

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

        # First row of inputs
        input_row1 = QHBoxLayout()

        # Menu name
        name_layout = QVBoxLayout()
        name_layout.addWidget(QLabel("Nama Menu:"))
        self.menu_name_input = QLineEdit()
        self.menu_name_input.setPlaceholderText("Masukkan nama menu...")
        name_layout.addWidget(self.menu_name_input)
        input_row1.addLayout(name_layout)

        # Category
        category_layout = QVBoxLayout()
        category_layout.addWidget(QLabel("Kategori:"))
        self.category_combo = QComboBox()
        self.category_combo.setEditable(True)
        self.category_combo.addItems([
            "Makanan Utama", "Minuman", "Appetizer", "Dessert",
            "Tambahan", "Paket", "Promo"
        ])
        category_layout.addWidget(self.category_combo)
        input_row1.addLayout(category_layout)

        # Price
        price_layout = QVBoxLayout()
        price_layout.addWidget(QLabel("Harga (Rp):"))
        self.price_input = QLineEdit()
        self.price_input.setPlaceholderText("0")
        price_layout.addWidget(self.price_input)
        input_row1.addLayout(price_layout)

        form_frame_layout.addLayout(input_row1)

        # Description
        desc_layout = QVBoxLayout()
        desc_layout.addWidget(QLabel("Deskripsi:"))
        self.description_input = QTextEdit()
        self.description_input.setMaximumHeight(60)
        self.description_input.setPlaceholderText("Deskripsi menu (opsional)...")
        desc_layout.addWidget(self.description_input)
        form_frame_layout.addLayout(desc_layout)

        # Available checkbox
        availability_layout = QHBoxLayout()
        self.available_checkbox = QCheckBox("Menu Tersedia")
        self.available_checkbox.setChecked(True)
        availability_layout.addWidget(self.available_checkbox)
        availability_layout.addStretch()
        form_frame_layout.addLayout(availability_layout)

        # Buttons
        button_layout = QHBoxLayout()
        self.add_menu_button = QPushButton("Tambah Menu")
        self.add_menu_button.clicked.connect(self.add_menu_item)
        self.update_menu_button = QPushButton("Update Menu")
        self.update_menu_button.clicked.connect(self.update_menu_item)
        self.update_menu_button.setEnabled(False)
        self.clear_menu_button = QPushButton("Bersihkan Form")
        self.clear_menu_button.clicked.connect(self.clear_form)

        button_layout.addWidget(self.add_menu_button)
        button_layout.addWidget(self.update_menu_button)
        button_layout.addWidget(self.clear_menu_button)
        button_layout.addStretch()

        form_frame_layout.addLayout(button_layout)
        form_layout.addWidget(form_frame)

        scroll_area.setWidget(form_container)
        main_layout.addWidget(scroll_area)

        # Table for menu items
        self.menu_table = QTableWidget()
        self.menu_table.setColumnCount(6)
        self.menu_table.setHorizontalHeaderLabels([
            "ID", "Nama Menu", "Kategori", "Harga", "Deskripsi", "Tersedia"
        ])

        # Table settings (Requirement 4: Scroll support)
        self.menu_table.setAlternatingRowColors(True)
        self.menu_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.menu_table.setSortingEnabled(True)
        self.menu_table.setHorizontalScrollMode(QTableWidget.ScrollPerPixel)
        self.menu_table.setVerticalScrollMode(QTableWidget.ScrollPerPixel)

        # Connect table selection
        self.menu_table.itemSelectionChanged.connect(self.on_menu_selected)

        main_layout.addWidget(self.menu_table)

        # Action buttons
        action_layout = QHBoxLayout()
        self.delete_menu_button = QPushButton("Hapus Menu")
        self.delete_menu_button.clicked.connect(self.delete_menu_item)
        self.delete_menu_button.setEnabled(False)

        self.export_menu_button = QPushButton("Ekspor Menu ke CSV")
        self.export_menu_button.clicked.connect(self.export_menu_to_csv)

        action_layout.addWidget(self.delete_menu_button)
        action_layout.addStretch()
        action_layout.addWidget(self.export_menu_button)

        main_layout.addLayout(action_layout)

    def add_menu_item(self):
        """Add new menu item"""
        name = self.menu_name_input.text().strip()
        category = self.category_combo.currentText().strip()
        price = self.price_input.text().strip()
        description = self.description_input.toPlainText().strip()
        available = self.available_checkbox.isChecked()

        if not name:
            QMessageBox.warning(self, "Error", "Nama menu harus diisi!")
            return

        if not category:
            QMessageBox.warning(self, "Error", "Kategori harus diisi!")
            return

        try:
            price = float(price)
            if price < 0:
                QMessageBox.warning(self, "Error", "Harga tidak boleh negatif!")
                return
        except ValueError:
            QMessageBox.warning(self, "Error", "Harga harus berupa angka!")
            return

        success = self.db_manager.add_menu_item(name, category, price, description, available)
        if success:
            QMessageBox.information(self, "Sukses", "Menu berhasil ditambahkan!")
            self.clear_form()
            self.load_menu_items()
        else:
            QMessageBox.critical(self, "Error", "Gagal menambahkan menu!")

    def update_menu_item(self):
        """Update selected menu item"""
        selected_row = self.menu_table.currentRow()
        if selected_row < 0:
            QMessageBox.warning(self, "Error", "Pilih menu yang akan diupdate!")
            return

        item_id = int(self.menu_table.item(selected_row, 0).text())
        name = self.menu_name_input.text().strip()
        category = self.category_combo.currentText().strip()
        price = self.price_input.text().strip()
        description = self.description_input.toPlainText().strip()
        available = self.available_checkbox.isChecked()

        if not name:
            QMessageBox.warning(self, "Error", "Nama menu harus diisi!")
            return

        if not category:
            QMessageBox.warning(self, "Error", "Kategori harus diisi!")
            return

        try:
            price = float(price)
            if price < 0:
                QMessageBox.warning(self, "Error", "Harga tidak boleh negatif!")
                return
        except ValueError:
            QMessageBox.warning(self, "Error", "Harga harus berupa angka!")
            return

        success = self.db_manager.update_menu_item(item_id, name, category, price, description, available)
        if success:
            QMessageBox.information(self, "Sukses", "Menu berhasil diupdate!")
            self.clear_form()
            self.load_menu_items()
        else:
            QMessageBox.critical(self, "Error", "Gagal mengupdate menu!")

    def delete_menu_item(self):
        """Delete selected menu item"""
        selected_row = self.menu_table.currentRow()
        if selected_row < 0:
            QMessageBox.warning(self, "Error", "Pilih menu yang akan dihapus!")
            return

        item_id = int(self.menu_table.item(selected_row, 0).text())
        menu_name = self.menu_table.item(selected_row, 1).text()

        reply = QMessageBox.question(
            self, "Konfirmasi Hapus",
            f"Apakah Anda yakin ingin menghapus menu '{menu_name}'?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            success = self.db_manager.delete_menu_item(item_id)
            if success:
                QMessageBox.information(self, "Sukses", "Menu berhasil dihapus!")
                self.clear_form()
                self.load_menu_items()
            else:
                QMessageBox.critical(self, "Error", "Gagal menghapus menu!")

    def clear_form(self):
        """Clear all form inputs"""
        self.menu_name_input.clear()
        self.category_combo.setCurrentIndex(0)
        self.price_input.clear()
        self.description_input.clear()
        self.available_checkbox.setChecked(True)
        self.update_menu_button.setEnabled(False)
        self.add_menu_button.setEnabled(True)
        self.delete_menu_button.setEnabled(False)

    def load_menu_items(self):
        """Load all menu items into table"""
        menu_items = self.db_manager.get_menu_items()
        self.menu_table.setRowCount(len(menu_items))

        for row, item in enumerate(menu_items):
            for col, data in enumerate(item):
                if col == 3:  # Format price
                    table_item = QTableWidgetItem(f"Rp {data:,.0f}")
                elif col == 5:  # Format availability
                    table_item = QTableWidgetItem("Ya" if data else "Tidak")
                else:
                    table_item = QTableWidgetItem(str(data))

                if col == 0:  # Make ID read-only
                    table_item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)

                self.menu_table.setItem(row, col, table_item)

        # Resize columns to content
        self.menu_table.resizeColumnsToContents()

    def on_menu_selected(self):
        """Handle menu selection"""
        selected_row = self.menu_table.currentRow()
        if selected_row >= 0:
            # Fill form with selected menu data
            menu_name = self.menu_table.item(selected_row, 1).text()
            category = self.menu_table.item(selected_row, 2).text()
            price = self.menu_table.item(selected_row, 3).text()
            # Remove currency formatting
            price = price.replace("Rp ", "").replace(",", "")
            description = self.menu_table.item(selected_row, 4).text()
            available = self.menu_table.item(selected_row, 5).text() == "Ya"

            self.menu_name_input.setText(menu_name)
            self.price_input.setText(price)
            self.description_input.setPlainText(description)
            self.available_checkbox.setChecked(available)

            # Set category combo box
            index = self.category_combo.findText(category)
            if index >= 0:
                self.category_combo.setCurrentIndex(index)
            else:
                self.category_combo.setEditText(category)

            # Enable update and delete buttons
            self.update_menu_button.setEnabled(True)
            self.add_menu_button.setEnabled(False)
            self.delete_menu_button.setEnabled(True)

    def search_menu_items(self, search_term):
        """Search menu items by name or category"""
        if search_term.strip():
            menu_items = self.db_manager.search_menu_items(search_term)
        else:
            menu_items = self.db_manager.get_menu_items()

        self.menu_table.setRowCount(len(menu_items))

        for row, item in enumerate(menu_items):
            for col, data in enumerate(item):
                if col == 3:  # Format price
                    table_item = QTableWidgetItem(f"Rp {data:,.0f}")
                elif col == 5:  # Format availability
                    table_item = QTableWidgetItem("Ya" if data else "Tidak")
                else:
                    table_item = QTableWidgetItem(str(data))

                if col == 0:  # Make ID read-only
                    table_item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)

                self.menu_table.setItem(row, col, table_item)

        self.menu_table.resizeColumnsToContents()

    def export_menu_to_csv(self):
        """Export menu items to CSV file"""
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Simpan File CSV", "menu_export.csv", "CSV Files (*.csv)"
        )

        if file_path:
            try:
                with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
                    writer = csv.writer(csvfile)

                    # Write headers
                    headers = ["ID", "Nama Menu", "Kategori", "Harga", "Deskripsi", "Tersedia"]
                    writer.writerow(headers)

                    # Write data
                    menu_items = self.db_manager.get_menu_items()
                    for item in menu_items:
                        # Convert boolean to text for CSV
                        item_list = list(item)
                        item_list[5] = "Ya" if item_list[5] else "Tidak"
                        writer.writerow(item_list)

                QMessageBox.information(self, "Sukses", f"Data menu berhasil diekspor ke {file_path}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Gagal mengekspor data: {str(e)}")