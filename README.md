# HTO Mass Balance Calculator

A Python application for performing mass balance calculations for hydrothermal oxidation (HTO) batch reactors with multiple feed streams.

## Features

- **User-friendly GUI** for inputting feed stream data and reactor parameters
- **Multiple feed streams** with customizable components
- **Unit conversion** to handle different input units for mass flow rates
- **Visual results** including tabular data and pie charts
- **Export capability** to save results in CSV format

## Installation

### Prerequisites

- Python 3.7 or higher
- PyQt5
- NumPy
- Pandas
- Matplotlib

### Setup

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/hto-massbalance.git
   cd hto-massbalance
   ```

2. Create and activate a virtual environment (recommended):
   ```
   python -m venv .venv
   source .venv/bin/activate  # On Windows, use .venv\Scripts\activate
   ```

3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

1. Run the application:
   ```
   python main.py
   ```

2. Using the application:
   - Add feed streams and components in the "Feed Streams" tab
   - Define reactor parameters in the "Reactor Parameters" tab
   - Click "Calculate Mass Balance" to perform the calculation
   - View results in tabular format
   - Toggle the chart view to see a visual representation
   - Export results to CSV if needed

## Application Structure

- `main.py`: Main entry point for the application
- `src/`: Source code directory
  - `gui/`: GUI components
    - `app.py`: Main application window
    - `feed_stream.py`: Feed stream input components
    - `reactor.py`: Reactor parameters input components
    - `results.py`: Results display components
  - `modeling/`: Calculation logic
    - `mass_balance.py`: Mass balance calculation functions

## Building an Executable

To build a standalone executable for Windows:

```
pyinstaller --onefile --windowed main.py
```

The executable will be created in the `dist` directory.

## Future Features

- Saving and loading feed stream configurations
- Advanced reporting capabilities
- Thermodynamic calculations
- Reaction kinetics modeling
- Handle output streams and phase separations
- More advanced visualizations

## License

[MIT License](LICENSE)
````

--------