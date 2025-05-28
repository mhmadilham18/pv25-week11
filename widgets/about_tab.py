from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QFrame, QPushButton, QScrollArea, QGroupBox
)
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtGui import QPixmap, QFont, QDesktopServices
import sys
import platform


class AboutTab(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        """Initialize the about tab UI"""
        # Create main layout
        main_layout = QVBoxLayout()
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(30, 30, 30, 30)

        # Create scroll area for better content management
        scroll_area = QScrollArea()
        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout()

        # App Title Section
        self.create_app_title_section(scroll_layout)

        # Developer Information Section
        self.create_developer_section(scroll_layout)

        # Application Information Section
        self.create_app_info_section(scroll_layout)

        # System Information Section
        self.create_system_info_section(scroll_layout)

        # Credits Section
        self.create_credits_section(scroll_layout)

        # Add stretch to push content to top
        scroll_layout.addStretch()

        scroll_widget.setLayout(scroll_layout)
        scroll_area.setWidget(scroll_widget)
        scroll_area.setWidgetResizable(True)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)

        main_layout.addWidget(scroll_area)
        self.setLayout(main_layout)

    def create_app_title_section(self, layout):
        """Create application title section"""
        title_frame = QFrame()
        title_frame.setFrameStyle(QFrame.Box)
        title_frame.setStyleSheet("""
            QFrame {
                background-color: #f0f8ff;
                border: 2px solid #4a90e2;
                border-radius: 10px;
                padding: 15px;
            }
        """)

        title_layout = QVBoxLayout()

        # Main title
        app_title = QLabel("Sistem Pembayaran Rumah Makan")
        app_title.setAlignment(Qt.AlignCenter)
        title_font = QFont()
        title_font.setPointSize(24)
        title_font.setBold(True)
        app_title.setFont(title_font)
        app_title.setStyleSheet("color: #2c3e50; margin: 10px;")
        title_layout.addWidget(app_title)

        # Subtitle
        subtitle = QLabel("Aplikasi Manajemen Pembayaran dan Menu Restoran")
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle_font = QFont()
        subtitle_font.setPointSize(12)
        subtitle_font.setItalic(True)
        subtitle.setFont(subtitle_font)
        subtitle.setStyleSheet("color: #7f8c8d; margin-bottom: 10px;")
        title_layout.addWidget(subtitle)

        # Version
        version_label = QLabel("Versi 1.0.0")
        version_label.setAlignment(Qt.AlignCenter)
        version_font = QFont()
        version_font.setPointSize(10)
        version_label.setFont(version_font)
        version_label.setStyleSheet("color: #95a5a6;")
        title_layout.addWidget(version_label)

        title_frame.setLayout(title_layout)
        layout.addWidget(title_frame)

    def create_developer_section(self, layout):
        """Create developer information section"""
        dev_group = QGroupBox("Informasi Pengembang")
        dev_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                font-size: 14px;
                color: #2c3e50;
                border: 2px solid #bdc3c7;
                border-radius: 8px;
                margin-top: 10px;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
                background-color: white;
            }
        """)

        dev_layout = QVBoxLayout()
        dev_layout.setSpacing(15)

        # Developer name
        name_layout = QHBoxLayout()
        name_label = QLabel("Nama:")
        name_label.setStyleSheet("font-weight: bold; color: #34495e; min-width: 120px;")
        name_value = QLabel("M. Ilham Abdul Shaleh")
        name_value.setStyleSheet("color: #2c3e50; font-size: 12px;")
        name_layout.addWidget(name_label)
        name_layout.addWidget(name_value)
        name_layout.addStretch()
        dev_layout.addLayout(name_layout)

        # Student ID
        nim_layout = QHBoxLayout()
        nim_label = QLabel("NIM:")
        nim_label.setStyleSheet("font-weight: bold; color: #34495e; min-width: 120px;")
        nim_value = QLabel("F1D022061")
        nim_value.setStyleSheet("color: #2c3e50; font-size: 12px;")
        nim_layout.addWidget(nim_label)
        nim_layout.addWidget(nim_value)
        nim_layout.addStretch()
        dev_layout.addLayout(nim_layout)

        # University
        univ_layout = QHBoxLayout()
        univ_label = QLabel("Universitas:")
        univ_label.setStyleSheet("font-weight: bold; color: #34495e; min-width: 120px;")
        univ_value = QLabel("Universitas Jenderal Soedirman")
        univ_value.setStyleSheet("color: #2c3e50; font-size: 12px;")
        univ_layout.addWidget(univ_label)
        univ_layout.addWidget(univ_value)
        univ_layout.addStretch()
        dev_layout.addLayout(univ_layout)

        # Development date
        date_layout = QHBoxLayout()
        date_label = QLabel("Dikembangkan:")
        date_label.setStyleSheet("font-weight: bold; color: #34495e; min-width: 120px;")
        date_value = QLabel("2024")
        date_value.setStyleSheet("color: #2c3e50; font-size: 12px;")
        date_layout.addWidget(date_label)
        date_layout.addWidget(date_value)
        date_layout.addStretch()
        dev_layout.addLayout(date_layout)

        dev_group.setLayout(dev_layout)
        layout.addWidget(dev_group)

    def create_app_info_section(self, layout):
        """Create application information section"""
        app_group = QGroupBox("Tentang Aplikasi")
        app_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                font-size: 14px;
                color: #2c3e50;
                border: 2px solid #bdc3c7;
                border-radius: 8px;
                margin-top: 10px;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
                background-color: white;
            }
        """)

        app_layout = QVBoxLayout()
        app_layout.setSpacing(15)

        # Description
        desc_label = QLabel("Deskripsi:")
        desc_label.setStyleSheet("font-weight: bold; color: #34495e;")
        app_layout.addWidget(desc_label)

        description = QLabel("""
        Sistem Pembayaran Rumah Makan adalah aplikasi desktop yang dikembangkan untuk membantu 
        pengelolaan transaksi pembayaran dan manajemen menu di rumah makan atau restoran. 
        Aplikasi ini menyediakan fitur-fitur lengkap mulai dari pencatatan transaksi, 
        manajemen menu, hingga pembuatan laporan.
        """)
        description.setWordWrap(True)
        description.setStyleSheet("color: #2c3e50; font-size: 11px; margin-left: 20px; margin-bottom: 10px;")
        app_layout.addWidget(description)

        # Features
        features_label = QLabel("Fitur Utama:")
        features_label.setStyleSheet("font-weight: bold; color: #34495e;")
        app_layout.addWidget(features_label)

        features_text = QLabel("""
        • Manajemen transaksi pembayaran dengan interface yang user-friendly
        • Pengelolaan menu dan harga dengan fitur CRUD (Create, Read, Update, Delete)
        • Sistem pencarian transaksi dan menu yang cepat dan akurat
        • Pembuatan laporan penjualan dengan berbagai filter
        • Ekspor laporan ke format Excel untuk analisis lebih lanjut
        • Database SQLite yang ringan dan efisien
        """)
        features_text.setWordWrap(True)
        features_text.setStyleSheet("color: #2c3e50; font-size: 11px; margin-left: 20px;")
        app_layout.addWidget(features_text)

        app_group.setLayout(app_layout)
        layout.addWidget(app_group)

    def create_system_info_section(self, layout):
        """Create system information section"""
        sys_group = QGroupBox("Informasi Sistem")
        sys_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                font-size: 14px;
                color: #2c3e50;
                border: 2px solid #bdc3c7;
                border-radius: 8px;
                margin-top: 10px;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
                background-color: white;
            }
        """)

        sys_layout = QVBoxLayout()
        sys_layout.setSpacing(10)

        # Python version
        python_layout = QHBoxLayout()
        python_label = QLabel("Python:")
        python_label.setStyleSheet("font-weight: bold; color: #34495e; min-width: 120px;")
        python_value = QLabel(f"{sys.version.split()[0]}")
        python_value.setStyleSheet("color: #2c3e50; font-size: 11px;")
        python_layout.addWidget(python_label)
        python_layout.addWidget(python_value)
        python_layout.addStretch()
        sys_layout.addLayout(python_layout)

        # Platform
        platform_layout = QHBoxLayout()
        platform_label = QLabel("Platform:")
        platform_label.setStyleSheet("font-weight: bold; color: #34495e; min-width: 120px;")
        platform_value = QLabel(f"{platform.system()} {platform.release()}")
        platform_value.setStyleSheet("color: #2c3e50; font-size: 11px;")
        platform_layout.addWidget(platform_label)
        platform_layout.addWidget(platform_value)
        platform_layout.addStretch()
        sys_layout.addLayout(platform_layout)

        # Architecture
        arch_layout = QHBoxLayout()
        arch_label = QLabel("Arsitektur:")
        arch_label.setStyleSheet("font-weight: bold; color: #34495e; min-width: 120px;")
        arch_value = QLabel(f"{platform.machine()}")
        arch_value.setStyleSheet("color: #2c3e50; font-size: 11px;")
        arch_layout.addWidget(arch_label)
        arch_layout.addWidget(arch_value)
        arch_layout.addStretch()
        sys_layout.addLayout(arch_layout)

        sys_group.setLayout(sys_layout)
        layout.addWidget(sys_group)

    def create_credits_section(self, layout):
        """Create credits and acknowledgments section"""
        credits_group = QGroupBox("Teknologi yang Digunakan")
        credits_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                font-size: 14px;
                color: #2c3e50;
                border: 2px solid #bdc3c7;
                border-radius: 8px;
                margin-top: 10px;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
                background-color: white;
            }
        """)

        credits_layout = QVBoxLayout()
        credits_layout.setSpacing(10)

        # Technologies used
        tech_list = [
            ("PyQt5", "Framework GUI untuk Python"),
            ("SQLite3", "Database ringan dan embedded"),
            ("Pandas", "Library untuk manipulasi dan analisis data"),
            ("OpenPyXL", "Library untuk membaca dan menulis file Excel"),
            ("Python", "Bahasa pemrograman utama")
        ]

        for tech, desc in tech_list:
            tech_layout = QHBoxLayout()
            tech_label = QLabel(f"• {tech}:")
            tech_label.setStyleSheet("font-weight: bold; color: #34495e; min-width: 100px;")
            tech_desc = QLabel(desc)
            tech_desc.setStyleSheet("color: #2c3e50; font-size: 11px;")
            tech_layout.addWidget(tech_label)
            tech_layout.addWidget(tech_desc)
            tech_layout.addStretch()
            credits_layout.addLayout(tech_layout)

        # Footer
        credits_layout.addWidget(QLabel(""))  # Spacer
        footer_label = QLabel("Terima kasih kepada komunitas open source yang telah menyediakan tools dan libraries yang digunakan dalam pengembangan aplikasi ini.")
        footer_label.setWordWrap(True)
        footer_label.setAlignment(Qt.AlignCenter)
        footer_label.setStyleSheet("color: #7f8c8d; font-size: 10px; font-style: italic; margin: 10px;")
        credits_layout.addWidget(footer_label)

        credits_group.setLayout(credits_layout)
        layout.addWidget(credits_group)

    def get_app_info(self):
        """Get application information"""
        return {
            'name': 'Sistem Pembayaran Rumah Makan',
            'version': '1.0.0',
            'developer': 'M. Ilham Abdul Shaleh',
            'nim': 'F1D022061',
            'university': 'Universitas Jenderal Soedirman',
            'year': '2024'
        }