#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Main application window for the HTO Mass Balance Calculator.
This module defines the main GUI interface and connects it to the calculation logic.
"""

from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QTabWidget, QPushButton, QLabel, QMessageBox, 
    QScrollArea, QSplitter
)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QFont

from .feed_stream import FeedStreamWidget
from .reactor import ReactorWidget
from .results import ResultsWidget
from src.modeling.mass_balance import calculate_mass_balance

class MainWindow(QMainWindow):
    """Main window of the HTO Mass Balance Calculator application."""
    
    def __init__(self):
        super().__init__()
        
        self.feed_streams = []  # List to store feed stream widgets
        self.init_ui()
        
    def init_ui(self):
        """Initialize the user interface."""
        # Set window properties
        self.setWindowTitle("Hydrothermal Oxidation Mass Balance Calculator")
        self.setMinimumSize(1000, 800)
        
        # Create central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        
        # Create splitter for adjustable sections
        splitter = QSplitter(Qt.Vertical)
        main_layout.addWidget(splitter)
        
        # Create input section
        input_widget = QWidget()
        input_layout = QVBoxLayout(input_widget)
        
        # Add title
        title_label = QLabel("HTO Mass Balance Calculator")
        title_label.setFont(QFont("Arial", 16, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        input_layout.addWidget(title_label)
        
        # Create tabs for different input sections
        tab_widget = QTabWidget()
        
        # Feed Streams Tab
        feed_streams_tab = QWidget()
        feed_streams_layout = QVBoxLayout(feed_streams_tab)
        
        # Scroll area for feed streams
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_content = QWidget()
        self.feed_streams_layout = QVBoxLayout(scroll_content)
        scroll_area.setWidget(scroll_content)
        feed_streams_layout.addWidget(scroll_area)
        
        # Add initial feed stream
        self.add_feed_stream()
        
        # Add button to add new feed stream
        add_stream_button = QPushButton("Add New Feed Stream")
        add_stream_button.clicked.connect(self.add_feed_stream)
        feed_streams_layout.addWidget(add_stream_button)
        
        # Reactor Parameters Tab
        self.reactor_widget = ReactorWidget()
        
        # Add tabs to the tab widget
        tab_widget.addTab(feed_streams_tab, "Feed Streams")
        tab_widget.addTab(self.reactor_widget, "Reactor Parameters")
        
        input_layout.addWidget(tab_widget)
        
        # Add calculate button
        calculate_button = QPushButton("Calculate Mass Balance")
        calculate_button.setMinimumHeight(50)
        calculate_button.setFont(QFont("Arial", 12))
        calculate_button.clicked.connect(self.calculate)
        input_layout.addWidget(calculate_button)
        
        # Add input widget to splitter
        splitter.addWidget(input_widget)
        
        # Create results section
        self.results_widget = ResultsWidget()
        splitter.addWidget(self.results_widget)
        
        # Set initial splitter sizes
        splitter.setSizes([600, 400])
        
        # Set status bar
        self.statusBar().showMessage("Ready")
    
    def add_feed_stream(self):
        """Add a new feed stream widget to the UI."""
        feed_stream = FeedStreamWidget(f"Feed Stream {len(self.feed_streams) + 1}")
        self.feed_streams.append(feed_stream)
        self.feed_streams_layout.addWidget(feed_stream)
        
        # Connect the remove signal from the feed stream to the remove method
        feed_stream.remove_requested.connect(self.remove_feed_stream)
    
    def remove_feed_stream(self, feed_stream):
        """Remove a feed stream widget from the UI."""
        if len(self.feed_streams) > 1:  # Keep at least one feed stream
            self.feed_streams.remove(feed_stream)
            feed_stream.setParent(None)  # Remove from layout
            feed_stream.deleteLater()  # Schedule for deletion
            
            # Renumber the remaining feed streams
            for i, fs in enumerate(self.feed_streams):
                fs.set_name(f"Feed Stream {i + 1}")
        else:
            QMessageBox.warning(self, "Cannot Remove", 
                                "At least one feed stream must remain.")
    
    def calculate(self):
        """Calculate the mass balance based on user inputs."""
        try:
            # Collect data from feed streams
            feed_data = []
            for feed_stream in self.feed_streams:
                stream_data = feed_stream.get_data()
                if stream_data:
                    feed_data.append(stream_data)
                else:
                    raise ValueError(f"Invalid data in {feed_stream.name}")
            
            # Collect reactor parameters
            reactor_params = self.reactor_widget.get_data()
            
            # Calculate mass balance
            results = calculate_mass_balance(feed_data, reactor_params)
            
            # Display results
            self.results_widget.display_results(results)
            
            self.statusBar().showMessage("Calculation completed successfully")
            
        except Exception as e:
            QMessageBox.critical(self, "Calculation Error", 
                                f"An error occurred during calculation: {str(e)}")
            self.statusBar().showMessage("Calculation failed")