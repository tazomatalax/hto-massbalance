#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Reactor parameters input component for the HTO Mass Balance Calculator.
This module defines the UI components for inputting reactor parameters.
"""

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QFrame, QComboBox, QFormLayout, QGroupBox, QSpinBox,
    QDoubleSpinBox
)
from PyQt5.QtCore import Qt

class ReactorWidget(QWidget):
    """Widget for inputting hydrothermal oxidation reactor parameters."""
    
    def __init__(self):
        super().__init__()
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
        
        # Title
        title_label = QLabel("Reactor Parameters")
        title_label.setStyleSheet("font-weight: bold; font-size: 14px;")
        title_label.setAlignment(Qt.AlignCenter)
        frame_layout.addWidget(title_label)
        
        # Form layout for parameters
        form_group = QGroupBox("HTO Reactor Configuration")
        form_layout = QFormLayout(form_group)
        
        # Reactor volume
        self.volume_input = QDoubleSpinBox()
        self.volume_input.setRange(0.1, 10000)
        self.volume_input.setValue(100)
        self.volume_input.setSuffix(" L")
        self.volume_input.setDecimals(1)
        form_layout.addRow("Reactor Volume:", self.volume_input)
        
        # Operating temperature
        self.temperature_input = QDoubleSpinBox()
        self.temperature_input.setRange(20, 1000)
        self.temperature_input.setValue(300)
        self.temperature_input.setSuffix(" °C")
        self.temperature_input.setDecimals(1)
        form_layout.addRow("Operating Temperature:", self.temperature_input)
        
        # Operating pressure
        self.pressure_input = QDoubleSpinBox()
        self.pressure_input.setRange(1, 500)
        self.pressure_input.setValue(25)
        self.pressure_input.setSuffix(" MPa")
        self.pressure_input.setDecimals(1)
        form_layout.addRow("Operating Pressure:", self.pressure_input)
        
        # Reaction time
        self.reaction_time_input = QDoubleSpinBox()
        self.reaction_time_input.setRange(1, 1000)
        self.reaction_time_input.setValue(60)
        self.reaction_time_input.setSuffix(" min")
        self.reaction_time_input.setDecimals(1)
        form_layout.addRow("Reaction Time:", self.reaction_time_input)
        
        # Reactor type
        self.reactor_type_input = QComboBox()
        self.reactor_type_input.addItems([
            "Batch", "Continuous Stirred Tank", "Plug Flow"
        ])
        form_layout.addRow("Reactor Type:", self.reactor_type_input)
        
        # Additional notes
        self.notes_input = QLineEdit()
        self.notes_input.setPlaceholderText("Enter any additional notes about the reactor setup")
        form_layout.addRow("Notes:", self.notes_input)
        
        frame_layout.addWidget(form_group)
        main_layout.addWidget(frame)
        
        # Add stretch to push form to the top
        main_layout.addStretch()
    
    def get_data(self):
        """
        Collect the reactor parameter data.
        
        Returns:
            dict: The reactor parameter data.
        """
        return {
            "volume": self.volume_input.value(),
            "volume_unit": "L",
            "temperature": self.temperature_input.value(),
            "temperature_unit": "°C",
            "pressure": self.pressure_input.value(),
            "pressure_unit": "MPa",
            "reaction_time": self.reaction_time_input.value(),
            "reaction_time_unit": "min",
            "reactor_type": self.reactor_type_input.currentText(),
            "notes": self.notes_input.text().strip()
        }