#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Mass balance calculation logic for the HTO Mass Balance Calculator.
This module contains the functions to perform mass balance calculations.
"""

def calculate_mass_balance(feed_streams, reactor_params):
    """
    Calculate the mass balance for multiple feed streams entering an HTO reactor.
    
    Args:
        feed_streams (list): List of feed stream data dictionaries.
        reactor_params (dict): Reactor parameters.
        
    Returns:
        dict: Mass balance calculation results.
    """
    # Initialize storage for component totals
    component_totals = {}
    unit_preference = "kg/hr"  # Default unit
    
    # Process each feed stream
    for stream in feed_streams:
        for component in stream.get("components", []):
            component_name = component["name"]
            flow_rate = component["flow_rate"]
            unit = component["unit"]
            
            # Convert flow rate to common unit if needed
            flow_rate_std = convert_to_standard_unit(flow_rate, unit)
            
            # Add to component totals
            if component_name in component_totals:
                component_totals[component_name]["flow_rate"] += flow_rate_std
                # Keep track of original unit for reference
                if unit != component_totals[component_name]["unit"]:
                    unit_preference = "kg/hr"  # Set to default if mixed units
            else:
                component_totals[component_name] = {
                    "name": component_name,
                    "flow_rate": flow_rate_std,
                    "unit": unit
                }
                # Set unit preference based on first component
                if unit_preference == "kg/hr" and unit != "kg/hr":
                    unit_preference = unit
    
    # Calculate total flow rate
    total_flow_rate = sum(comp["flow_rate"] for comp in component_totals.values())
    
    # Calculate mass fractions
    components_result = []
    for comp_name, comp_data in component_totals.items():
        # Calculate mass fraction (percentage)
        mass_fraction = (comp_data["flow_rate"] / total_flow_rate * 100) if total_flow_rate > 0 else 0
        
        # Convert back to preferred unit if needed
        flow_rate_pref = convert_from_standard_unit(comp_data["flow_rate"], unit_preference)
        
        components_result.append({
            "name": comp_name,
            "flow_rate": flow_rate_pref,
            "unit": unit_preference,
            "mass_fraction": mass_fraction
        })
    
    # Sort components by flow rate (descending)
    components_result.sort(key=lambda x: x["flow_rate"], reverse=True)
    
    # Convert total to preferred unit
    total_flow_rate_pref = convert_from_standard_unit(total_flow_rate, unit_preference)
    
    # Return results
    return {
        "components": components_result,
        "total_flow_rate": total_flow_rate_pref,
        "unit": unit_preference,
        "reactor_params": reactor_params
    }

def convert_to_standard_unit(value, unit):
    """
    Convert a flow rate value from given unit to standard unit (kg/hr).
    
    Args:
        value (float): The flow rate value.
        unit (str): The unit of the flow rate.
        
    Returns:
        float: The flow rate value in kg/hr.
    """
    # Conversion factors to kg/hr
    conversion_factors = {
        "kg/hr": 1.0,
        "g/min": 0.06,  # 1 g/min = 0.06 kg/hr
        "g/hr": 0.001,  # 1 g/hr = 0.001 kg/hr
        "ton/day": 41.67  # 1 ton/day = 41.67 kg/hr (approximate)
    }
    
    # Perform conversion
    if unit in conversion_factors:
        return value * conversion_factors[unit]
    else:
        # Default to no conversion if unit not recognized
        return value

def convert_from_standard_unit(value, unit):
    """
    Convert a flow rate value from standard unit (kg/hr) to given unit.
    
    Args:
        value (float): The flow rate value in kg/hr.
        unit (str): The target unit.
        
    Returns:
        float: The flow rate value in the target unit.
    """
    # Conversion factors from kg/hr
    conversion_factors = {
        "kg/hr": 1.0,
        "g/min": 16.67,  # 1 kg/hr = 16.67 g/min
        "g/hr": 1000.0,  # 1 kg/hr = 1000 g/hr
        "ton/day": 0.024  # 1 kg/hr = 0.024 ton/day (approximate)
    }
    
    # Perform conversion
    if unit in conversion_factors:
        return value * conversion_factors[unit]
    else:
        # Default to no conversion if unit not recognized
        return value