# restaurant_app.py - Main Application Window
from PyQt5.QtWidgets import (
    QMainWindow, QTabWidget, QMenuBar, QMenu, QAction,
    QDockWidget, QStatusBar, QWidget, QVBoxLayout, QHBoxLayout,
    QLineEdit, QLabel, QMessageBox
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from db_manager import DatabaseManager
from widgets.payment_tab import PaymentTab
from widgets.menu_tab import MenuTab
from widgets.report_tab import ReportTab
from widgets.about_tab import AboutTab


class RestaurantPaymentApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sistem Pembayaran Rumah Makan")
        self.resize(1900, 1200)

        # Initialize database
        self.db_manager = DatabaseManager()

        self.init_ui()
        self.init_menu_bar()
        self.init_dock_widget()
        self.init_status_bar()

    def init_ui(self):
        """Initialize the main user interface"""
        # Create central widget with tabs
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        # Initialize tabs
        self.payment_tab = PaymentTab(self.db_manager)
        self.menu_tab = MenuTab(self.db_manager)
        self.report_tab = ReportTab(self.db_manager)
        self.about_tab = AboutTab()

        # Add tabs
        self.tabs.addTab(self.payment_tab, "Pembayaran")
        self.tabs.addTab(self.menu_tab, "Menu")
        self.tabs.addTab(self.report_tab, "Laporan")
        self.tabs.addTab(self.about_tab, "Tentang")

    def init_menu_bar(self):
        """Initialize menu bar"""
        menu_bar = self.menuBar()

        # File menu
        file_menu = menu_bar.addMenu("File")

        refresh_action = QAction("Refresh Data", self)
        refresh_action.setShortcut("F5")
        refresh_action.triggered.connect(self.refresh_all_data)

        export_action = QAction("Ekspor Laporan", self)
        export_action.triggered.connect(self.export_report)

        exit_action = QAction("Keluar", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)

        file_menu.addAction(refresh_action)
        file_menu.addAction(export_action)
        file_menu.addSeparator()
        file_menu.addAction(exit_action)

        # View menu
        view_menu = menu_bar.addMenu("View")

        search_action = QAction("Toggle Search Panel", self)
        search_action.setShortcut("Ctrl+F")
        search_action.triggered.connect(self.toggle_search_dock)

        view_menu.addAction(search_action)

        # Help menu
        help_menu = menu_bar.addMenu("Help")

        about_action = QAction("Tentang Aplikasi", self)
        about_action.triggered.connect(self.show_about)

        help_menu.addAction(about_action)

    def init_dock_widget(self):
        """Initialize dock widget for search functionality"""
        self.search_dock = QDockWidget("Panel Pencarian", self)
        self.search_dock.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea | Qt.TopDockWidgetArea)

        # Create search widget
        search_widget = QWidget()
        search_layout = QVBoxLayout()

        # Search label
        search_label = QLabel("Cari Transaksi:")
        search_layout.addWidget(search_label)

        # Search input
        self.global_search_input = QLineEdit()
        self.global_search_input.setPlaceholderText("Masukkan nama pelanggan atau ID transaksi...")
        self.global_search_input.textChanged.connect(self.perform_global_search)
        search_layout.addWidget(self.global_search_input)

        # Quick search label
        quick_label = QLabel("Pencarian Cepat Menu:")
        search_layout.addWidget(quick_label)

        # Menu search input
        self.menu_search_input = QLineEdit()
        self.menu_search_input.setPlaceholderText("Cari nama menu...")
        self.menu_search_input.textChanged.connect(self.perform_menu_search)
        search_layout.addWidget(self.menu_search_input)

        search_widget.setLayout(search_layout)
        self.search_dock.setWidget(search_widget)

        # Add dock to right side
        self.addDockWidget(Qt.RightDockWidgetArea, self.search_dock)

    def init_status_bar(self):
        """Initialize status bar with student information"""
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage(
            "M. Ilham Abdul Shaleh | F1D022120 | Sistem Pembayaran Rumah Makan")

    def refresh_all_data(self):
        """Refresh all data in all tabs"""
        try:
            self.payment_tab.load_payments()
            self.menu_tab.load_menu_items()
            self.report_tab.load_reports()
            self.status_bar.showMessage("Data berhasil di-refresh", 3000)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Gagal refresh data: {str(e)}")

    def export_report(self):
        """Export report functionality"""
        self.tabs.setCurrentWidget(self.report_tab)
        self.report_tab.export_report()

    def toggle_search_dock(self):
        """Toggle search dock visibility"""
        if self.search_dock.isVisible():
            self.search_dock.hide()
        else:
            self.search_dock.show()

    def show_about(self):
        """Show about tab"""
        self.tabs.setCurrentWidget(self.about_tab)

    def perform_global_search(self, text):
        """Perform global search across payments"""
        if hasattr(self.payment_tab, 'search_payments'):
            self.payment_tab.search_payments(text)

    def perform_menu_search(self, text):
        """Perform menu search"""
        if hasattr(self.menu_tab, 'search_menu_items'):
            self.menu_tab.search_menu_items(text)

    def closeEvent(self, event):
        """Handle application close event"""
        reply = QMessageBox.question(
            self, 'Konfirmasi Keluar',
            'Apakah Anda yakin ingin keluar dari aplikasi?',
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            # Close database connection
            self.db_manager.close_connection()
            event.accept()
        else:
            event.ignore()