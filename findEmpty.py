import json
from xlrd import open_workbook

def percentString(part, total):
    return str(round(100*float(part)/float(total),2)) + '%'

def main():
    with open('infoboxes.json', 'rb') as fp:
        infoboxAttributes = json.load(fp)
        emptyAttributes = {}
        
        wb = open_workbook('infoboxes.xlsx')
        sheet = wb.sheet_by_index(0)

        totalPages = 0
        totalMissedPages = 0
        totalMissedTemplates = 0
        mostMissedTemplate = 3596 # start with template with one page
        
        for row in range(2, sheet.nrows):        
            cell = str(sheet.cell(row,0).value)
            numberOfPages = sheet.cell(row,1).value # how many pages
            totalPages += numberOfPages
            infobox = 'Template:Infobox ' + cell.replace('-', ' ')
            print 'Checking ' + str(row) + ' of ' + str(sheet.nrows) + " : " + infobox
            if infoboxAttributes[infobox] == {}:
                emptyAttributes[infobox] = numberOfPages
                totalMissedPages += numberOfPages
                totalMissedTemplates += 1
                if numberOfPages > sheet.cell(mostMissedTemplate,1).value:
                    mostMissedTemplate = row

        print 'Done. Writing to disk...'
        with open('emptyAttributes.json', 'wb') as fp:
            json.dump(emptyAttributes, fp)

        print
        print 'DONE. Statistics:'
        print 'Total number of missed infobox templates: ' + str(totalMissedTemplates) + ' out of ' + str(sheet.nrows - 2) + ' total, or ' + percentString(totalMissedTemplates, sheet.nrows - 2)
        print 'This misses ' + str(int(totalMissedPages)) + ' Wikipedia pages out of ' + str(int(totalPages)) + ' total, or ' + percentString(totalMissedPages, totalPages)
        print 'Missed template with most pages: ' + '[Template:Infobox ' + str(sheet.cell(mostMissedTemplate,0).value).replace('-', ' ') + '] with ' + str(int(sheet.cell(mostMissedTemplate,1).value)) + ' pages'

main()
