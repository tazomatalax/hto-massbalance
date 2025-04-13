#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Results display component for the HTO Mass Balance Calculator.
This module defines the UI components for displaying mass balance results.
"""

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTableWidget,
    QTableWidgetItem, QHeaderView, QFrame, QPushButton, QFileDialog
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import numpy as np
import pandas as pd
import os

class ResultsWidget(QWidget):
    """Widget for displaying mass balance calculation results."""
    
    def __init__(self):
        super().__init__()
        self.results_data = None
        self.init_ui()
    
    def init_ui(self):
        """Initialize the user interface."""
        # Main layout
        main_layout = QVBoxLayout(self)
        
        # Title
        title_label = QLabel("Mass Balance Results")
        title_label.setFont(QFont("Arial", 14, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title_label)
        
        # Create a frame with a border
        frame = QFrame()
        frame.setFrameShape(QFrame.StyledPanel)
        frame.setFrameShadow(QFrame.Raised)
        frame_layout = QVBoxLayout(frame)
        
        # Create table for results
        self.results_table = QTableWidget(0, 4)
        self.results_table.setHorizontalHeaderLabels([
            "Component", "Total Mass Flow Rate", "Unit", "Mass Fraction (%)"
        ])
        self.results_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        frame_layout.addWidget(self.results_table)
        
        # Create placeholder for chart
        self.chart_frame = QFrame()
        self.chart_layout = QVBoxLayout(self.chart_frame)
        self.chart_canvas = None
        frame_layout.addWidget(self.chart_frame)
        
        # Add button row
        button_layout = QHBoxLayout()
        
        # Export button
        export_button = QPushButton("Export Results")
        export_button.clicked.connect(self.export_results)
        button_layout.addWidget(export_button)
        
        # Add spacer
        button_layout.addStretch()
        
        # Toggle chart button
        self.toggle_chart_button = QPushButton("Show Chart")
        self.toggle_chart_button.clicked.connect(self.toggle_chart)
        button_layout.addWidget(self.toggle_chart_button)
        
        frame_layout.addLayout(button_layout)
        main_layout.addWidget(frame)
        
        # Initial state - hide chart
        self.chart_frame.setVisible(False)
    
    def display_results(self, results):
        """
        Display the mass balance calculation results.
        
        Args:
            results (dict): The mass balance calculation results.
        """
        # Store results data for later use
        self.results_data = results
        
        # Clear existing results
        self.results_table.setRowCount(0)
        
        # Add component rows
        components = results.get("components", [])
        for i, component in enumerate(components):
            self.results_table.insertRow(i)
            
            # Component name
            name_item = QTableWidgetItem(component["name"])
            self.results_table.setItem(i, 0, name_item)
            
            # Mass flow rate
            flow_item = QTableWidgetItem(f"{component['flow_rate']:.4g}")
            flow_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.results_table.setItem(i, 1, flow_item)
            
            # Unit
            unit_item = QTableWidgetItem(component["unit"])
            self.results_table.setItem(i, 2, unit_item)
            
            # Mass fraction
            fraction_item = QTableWidgetItem(f"{component['mass_fraction']:.2f}")
            fraction_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.results_table.setItem(i, 3, fraction_item)
        
        # Add total row
        total_row = self.results_table.rowCount()
        self.results_table.insertRow(total_row)
        
        # Total label
        total_label = QTableWidgetItem("TOTAL")
        total_label.setFont(QFont("Arial", 10, QFont.Bold))
        self.results_table.setItem(total_row, 0, total_label)
        
        # Total mass flow rate
        total_flow = QTableWidgetItem(f"{results['total_flow_rate']:.4g}")
        total_flow.setFont(QFont("Arial", 10, QFont.Bold))
        total_flow.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.results_table.setItem(total_row, 1, total_flow)
        
        # Total unit
        total_unit = QTableWidgetItem(results["unit"])
        total_unit.setFont(QFont("Arial", 10, QFont.Bold))
        self.results_table.setItem(total_row, 2, total_unit)
        
        # Total mass fraction
        total_fraction = QTableWidgetItem("100.00")
        total_fraction.setFont(QFont("Arial", 10, QFont.Bold))
        total_fraction.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.results_table.setItem(total_row, 3, total_fraction)
        
        # Create chart if toggle is on
        if self.chart_frame.isVisible():
            self.create_chart()
    
    def create_chart(self):
        """Create a pie chart for the mass balance results."""
        if not self.results_data:
            return
        
        # Clear existing chart
        if self.chart_canvas:
            self.chart_layout.removeWidget(self.chart_canvas)
            self.chart_canvas.deleteLater()
        
        # Create figure and canvas
        fig, ax = plt.subplots(figsize=(8, 5))
        self.chart_canvas = FigureCanvas(fig)
        self.chart_layout.addWidget(self.chart_canvas)
        
        # Prepare data for chart
        components = self.results_data.get("components", [])
        labels = [comp["name"] for comp in components]
        fractions = [comp["mass_fraction"] for comp in components]
        
        # Create pie chart
        ax.pie(fractions, labels=labels, autopct='%1.1f%%', startangle=90)
        ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle
        
        # Set title
        ax.set_title('Mass Balance Distribution')
        
        # Draw the chart
        self.chart_canvas.draw()
    
    def toggle_chart(self):
        """Toggle the visibility of the chart."""
        is_visible = self.chart_frame.isVisible()
        self.chart_frame.setVisible(not is_visible)
        
        # Update button text
        if not is_visible:
            self.toggle_chart_button.setText("Hide Chart")
            if self.results_data:
                self.create_chart()
        else:
            self.toggle_chart_button.setText("Show Chart")
    
    def export_results(self):
        """Export the results to a CSV file."""
        if not self.results_data:
            return
        
        # Ask for file name and location
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Export Results", "", "CSV Files (*.csv);;All Files (*)"
        )
        
        if not file_path:
            return
        
        # Ensure the file has a .csv extension
        if not file_path.endswith('.csv'):
            file_path += '.csv'
        
        try:
            # Create DataFrame from results
            data = []
            for comp in self.results_data["components"]:
                data.append({
                    "Component": comp["name"],
                    "Mass Flow Rate": comp["flow_rate"],
                    "Unit": comp["unit"],
                    "Mass Fraction (%)": comp["mass_fraction"]
                })
            
            # Add total row
            data.append({
                "Component": "TOTAL",
                "Mass Flow Rate": self.results_data["total_flow_rate"],
                "Unit": self.results_data["unit"],
                "Mass Fraction (%)": 100.0
            })
            
            # Create DataFrame and save to CSV
            df = pd.DataFrame(data)
            df.to_csv(file_path, index=False)
            
            # Show success message in parent's status bar
            if hasattr(self.window(), 'statusBar'):
                self.window().statusBar().showMessage(f"Results exported to {os.path.basename(file_path)}")
        
        except Exception as e:
            if hasattr(self.window(), 'statusBar'):
                self.window().statusBar().showMessage(f"Error exporting results: {str(e)}")