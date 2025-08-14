import setuptools
from distutils.core import setup

setup(
    name="expense-tracker",
    version="1.0.0",
    description="CLI Expense tracker",
    author="Jakub Stankiewicz",
    author_email="jakubstankiewicz024@gmail.com",
    packages=["expense_tracker"],
    entry_points={
        "console_scripts":["expensetracker=expense_tracker.entry:cli_entry_point"]
    },
    install_requires=[
        'argparse',
        ]
)