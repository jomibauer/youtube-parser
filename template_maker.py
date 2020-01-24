def template_maker():
    import openpyxl
    from openpyxl.styles import Font

    bold_font = Font(bold = True)

    wb = openpyxl.Workbook()

    sheet = wb.active

    sheet['A1'] = 'Channel name'
    sheet['B1'] = 'Subs'
    sheet['C1'] = 'Total channel views'
    sheet['D1'] = 'Avg views per video'
    sheet['E1'] = 'Avg uploads per month'
    
    sheet.column_dimensions['A'].width = 14.4
    sheet.column_dimensions['C'].width = 19
    sheet.column_dimensions['D'].width = 19
    sheet.column_dimensions['E'].width = 22

    for cell in sheet['1:1']:
        cell.font = bold_font
        
    wb.save('template.xlsx')