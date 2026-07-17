from openpyxl import Workbook, workbook
import scraper

wb = Workbook()

sheet = wb.active

#titles
sheet["A1"] = "Uni Name"
sheet["B1"] = "Rank"
sheet["C1"] = "Course"
sheet["D1"] = "Requirement"

def write_row():
    pass


wb.save(filename="uni thing.xlsx")