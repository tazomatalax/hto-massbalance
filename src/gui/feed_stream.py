#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Feed stream input component for the HTO Mass Balance Calculator.
This module defines the UI components for inputting feed stream data.
"""

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QFrame, QComboBox, QTableWidget, QTableWidgetItem,
    QHeaderView, QGroupBox, QMessageBox
)
from PyQt5.QtCore import Qt, pyqtSignal

class FeedStreamWidget(QWidget):
    """Widget for inputting feed stream data."""
    
    # Signal emitted when the user requests removal of this feed stream
    remove_requested = pyqtSignal(object)
    
    def __init__(self, name):
        super().__init__()
        self.name = name
        self.components = []
        self.init_ui()
    
    def init_ui(self):
        """Initialize the user interface."""
        # Main layout
        main_layout = QVBoxLayout(self)
        
        # Create a frame with a border
        frame = QFrame()
        frame.setFrameShape(QFrame.StyledPanel)
        frame.setFrameShadow(QFrame.Raised)
        frame_layout = QVBoxLayout(frame)
        
        # Header section with name and remove button
        header_layout = QHBoxLayout()
        
        # Stream name label
        self.name_label = QLabel(self.name)
        self.name_label.setStyleSheet("font-weight: bold; font-size: 14px;")
        header_layout.addWidget(self.name_label)
        
        # Stream name edit field
        self.name_edit = QLineEdit()
        self.name_edit.setPlaceholderText("Enter stream name (e.g., Organic Waste)")
        header_layout.addWidget(self.name_edit, 1)
        
        # Remove button
        remove_button = QPushButton("Remove")
        remove_button.clicked.connect(self.request_removal)
        header_layout.addWidget(remove_button)
        
        frame_layout.addLayout(header_layout)
        
        # Add horizontal separator
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setFrameShadow(QFrame.Sunken)
        frame_layout.addWidget(separator)
        
        # Components table
        components_group = QGroupBox("Components")
        components_layout = QVBoxLayout(components_group)
        
        # Create table for components
        self.components_table = QTableWidget(0, 3)
        self.components_table.setHorizontalHeaderLabels([
            "Component Name", "Mass Flow Rate", "Unit"
        ])
        self.components_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.components_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.components_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)
        components_layout.addWidget(self.components_table)
        
        # Add component controls
        controls_layout = QHBoxLayout()
        
        # Add component button
        add_component_button = QPushButton("Add Component")
        add_component_button.clicked.connect(self.add_component)
        controls_layout.addWidget(add_component_button)
        
        # Remove component button
        remove_component_button = QPushButton("Remove Selected Component")
        remove_component_button.clicked.connect(self.remove_component)
        controls_layout.addWidget(remove_component_button)
        
        components_layout.addLayout(controls_layout)
        frame_layout.addWidget(components_group)
        
        # Add initial component
        self.add_component()
        
        main_layout.addWidget(frame)
    
    def set_name(self, name):
        """Update the name of this feed stream."""
        self.name = name
        self.name_label.setText(name)
    
    def add_component(self):
        """Add a new component row to the table."""
        row = self.components_table.rowCount()
        self.components_table.insertRow(row)
        
        # Component name field
        name_item = QTableWidgetItem()
        self.components_table.setItem(row, 0, name_item)
        
        # Mass flow rate field
        flow_item = QTableWidgetItem()
        self.components_table.setItem(row, 1, flow_item)
        
        # Unit selection dropdown
        unit_combo = QComboBox()
        unit_combo.addItems(["kg/hr", "g/min", "g/hr", "ton/day"])
        self.components_table.setCellWidget(row, 2, unit_combo)
    
    def remove_component(self):
        """Remove the selected component row from the table."""
        selected_rows = set(index.row() for index in self.components_table.selectedIndexes())
        
        # Remove rows in reverse order to avoid index shifting
        for row in sorted(selected_rows, reverse=True):
            self.components_table.removeRow(row)
        
        # Ensure at least one component row exists
        if self.components_table.rowCount() == 0:
            self.add_component()
    
    def request_removal(self):
        """Emit signal to request removal of this feed stream."""
        self.remove_requested.emit(self)
    
    def get_data(self):
        """
        Collect and validate the data from this feed stream.
        
        Returns:
            dict: The feed stream data if valid, None otherwise.
        """
        # Get the stream name
        stream_name = self.name_edit.text().strip()
        if not stream_name:
            stream_name = self.name  # Use default name if not provided
        
        # Collect component data
        components = []
        for row in range(self.components_table.rowCount()):
            name_item = self.components_table.item(row, 0)
            flow_item = self.components_table.item(row, 1)
            unit_combo = self.components_table.cellWidget(row, 2)
            
            component_name = name_item.text().strip() if name_item else ""
            
            # Skip empty components
            if not component_name:
                continue
            
            try:
                flow_rate = float(flow_item.text()) if flow_item and flow_item.text().strip() else 0.0
            except ValueError:
                QMessageBox.warning(self, "Invalid Input", 
                                    f"Mass flow rate for {component_name} must be a number.")
                return None
            
            unit = unit_combo.currentText() if unit_combo else "kg/hr"
            
            components.append({
                "name": component_name,
                "flow_rate": flow_rate,
                "unit": unit
            })
        
        # Validate at least one component with non-zero flow rate
        if not any(c["flow_rate"] > 0 for c in components):
            QMessageBox.warning(self, "Invalid Input", 
                               "At least one component must have a non-zero mass flow rate.")
            return None
        
        return {
            "name": stream_name,
            "components": components
        }