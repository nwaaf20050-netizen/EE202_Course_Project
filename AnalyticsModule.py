import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

# Ensure you import your RegistrationSystem class
from RegistrationSystemClass import RegistrationSystem 

class AnalyticsModule:
    """
    Handles data aggregation, calculation of metrics (like fill rates), 
    and generation of graphical charts for the Admin Dashboard.
    """
    def __init__(self, registration_system: RegistrationSystem):
        self.system = registration_system

    def calculate_fill_rate_chart(self):
        """
        Calculates the Course Fill Rate (enrollment vs. capacity) for all courses 
        and returns the chart as a PyQt-compatible FigureCanvas object.
        
        This object can be directly added to a QWidget layout.
        """
        # 1. Fetch data from the Registration System
        data = self.system.get_course_enrollment_data()

        if not data:
            # Return None if no data is available to avoid errors
            return None

        course_codes = []
        fill_rates = []
        
        # 2. Process data: Calculate the fill rate metric
        for code, capacity, enrollment in data:
            # Calculate Fill Rate: (Current Enrollment / Max Capacity) * 100
            # Handle division by zero case
            fill_rate = (enrollment / capacity) * 100 if capacity > 0 else 0
            course_codes.append(code)
            fill_rates.append(fill_rate)

        # 3. Visualization: Generate the Matplotlib Figure and Canvas
        
        # Create a new Figure object
        fig = Figure(figsize=(8, 5))
        # Add a subplot to the figure (1 row, 1 column, 1st plot)
        ax = fig.add_subplot(111)
        
        # Plot the bar chart
        ax.bar(course_codes, fill_rates, color='teal')
        
        # Set chart labels and title
        ax.set_xlabel('Course Code')
        ax.set_ylabel('Fill Rate (%)')
        ax.set_title('Course Enrollment Fill Rate Analysis')
        ax.set_ylim(0, 100) # Fill rate is always between 0 and 100%
        ax.grid(axis='y', linestyle='--')
        
        # Return the FigureCanvas object for PyQt integration
        return FigureCanvas(fig)