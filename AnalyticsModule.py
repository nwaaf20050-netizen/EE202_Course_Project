import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
#alshamrani
# Ensure you import your RegistrationSystem class
from RegistrationSystemClass import RegistrationSystem 


class Analytics:
    """
    Handles data aggregation, calculation of metrics (like fill rates),
    and generation of graphical charts for the Admin Dashboard.
    """
    def __init__(self, registration_system):
        self.system = registration_system

    def calculate_section_chart(self, course_code):
        data = self.system.get_course_enrollment_data()

        # Filter the selected course
        target = next((item for item in data if item[0] == course_code), None)

        if not target:
            return None

        course_code, sections_data, total_enrolled, total_capacity = target

        section_names = []
        enrolled_numbers = []

        for section, enrolled, capacity in sections_data:
            section_names.append(section)
            enrolled_numbers.append(enrolled)

        fig = Figure(figsize=(12, 6))
        ax = fig.add_subplot(111)

        bars = ax.bar(section_names, enrolled_numbers, color='skyblue')

        ax.set_xlabel('Section')
        ax.set_ylabel('Enrolled Students (out of 100)')
        
        ax.set_title(f'Section Enrollment for Course: {course_code}',pad=5)

        # Fix Y-axis scale
        ax.set_ylim(0, 100)

        # Show enrolled number on top of each bar
        for bar, num in zip(bars, enrolled_numbers):
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1,
                    f'{num}', ha='center', va='bottom', fontsize=9)

        ax.set_xticklabels(section_names, rotation=0, ha='center', fontsize=10)

        ax.grid(axis='y', linestyle='--', alpha=0.5)
        fig.tight_layout()

        return FigureCanvas(fig)
