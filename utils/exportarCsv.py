import csv

class ExportarCsv:
    def __init__(self, listaCsv, fileName):
        self.listaCsv = listaCsv
        self.fileName = fileName

    def criarCsv(self):
        with open(f'{self.fileName}.csv', 'w', encoding='utf8', newline='') as output_file:
            campos = self.listaCsv[0].keys()
            escritor = csv.DictWriter(output_file, campos)

            escritor.writeheader()
            escritor.writerows(self.listaCsv)