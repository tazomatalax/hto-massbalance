#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Main entry point for the HTO Mass Balance Calculator application.
This file initializes and launches the GUI application.
"""

import sys
from PyQt5.QtWidgets import QApplication
from src.gui.app import MainWindow

def main():
    """Initialize and launch the application."""
    app = QApplication(sys.argv)
    app.setApplicationName("HTO Mass Balance Calculator")
    
    main_window = MainWindow()
    main_window.show()
    
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()