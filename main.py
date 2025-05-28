from PyQt5.QtWidgets import QApplication
import sys
from restaurant_app import RestaurantPaymentApp

def main():
    app = QApplication(sys.argv)
    window = RestaurantPaymentApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()