from matplotlib.backends.backend_pdf import PdfPages
def export(figure):
    filename = input("what would you like to name the file?") + ".pdf"
    with PdfPages(filename) as export_pdf:
        plt = figure
        export_pdf.savefig()
