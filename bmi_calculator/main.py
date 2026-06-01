"""Entry point for the BMI Calculator app."""
from bmi_calculator.gui.app import BMIApp


def main():
    app = BMIApp()
    app.mainloop()


if __name__ == "__main__":
    main()
