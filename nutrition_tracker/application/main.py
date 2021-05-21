import sys
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem
from UiMainWindow import Ui_MainWindow
from nutrition_plotter import Canvas, NutritionDiary, regex_search, df, rdi_df

class MainWindow:
    def __init__(self):
        self.main_win = QMainWindow()
        self.ui = Ui_MainWindow()
        self.diary_instance = NutritionDiary()
        
        self.grams = 100
        self.sex = 'Male'
        self.weight = 70
        
        self.ui.setupUi(self.main_win)  
        self.ui.stackedWidget.setCurrentWidget(self.ui.search_pg)
        
        self.ui.back_btn.clicked.connect(self.back_btn_clicked)
        self.ui.search_btn.clicked.connect(self.search_btn_clicked)
        self.ui.diary_btn.clicked.connect(self.diary_btn_clicked)        
        self.ui.plus_btn.clicked.connect(self.add_btn_clicked)
        
        self.ui.m_btn.clicked.connect(self.m_btn_clicked)
        self.ui.f_btn.clicked.connect(self.f_btn_clicked)
        self.ui.search_field.returnPressed.connect(self.search_returned)
        
        self.ui.hide_righthand_widgets()
    
    def show(self):
        self.main_win.show()
        
    def back_btn_clicked(self):
        if self.ui.stackedWidget.currentWidget() == self.ui.table_pg:
            self.search_btn_clicked()
        elif self.ui.stackedWidget.currentWidget() == self.ui.vis_pg:
            self.show_table()
            
    def search_btn_clicked(self):
        plt.close()
        self.ui.stackedWidget.setCurrentWidget(self.ui.search_pg)
        self.ui.hide_righthand_widgets()
    
    def diary_btn_clicked(self):
        plt.close()
        self.plot_diary_chart()
        self.ui.stackedWidget.setCurrentWidget(self.ui.diary_pg)
        self.ui.hide_righthand_widgets()
    
    def add_btn_clicked(self):
        try:
            self.change_default_values()
            self.diary_instance.add_food(df, self.food_id, self.grams)
        except AttributeError:
            print('User didn\'t select a food')
        
    def m_btn_clicked(self):
        self.ui.m_btn.setStyleSheet('font: bold 12px')
        self.ui.f_btn.setStyleSheet('font: normal 12px')
        self.sex = 'Male'
    
    def f_btn_clicked(self):
        self.ui.f_btn.setStyleSheet('font: bold 12px')
        self.ui.m_btn.setStyleSheet('font: normal 12px')
        self.sex = 'Female'
        
    def search_returned(self):
        text_string = self.ui.search_field.text()
        self.create_table(text_string)
        self.show_table()
        self.ui.search_field.clear()
               
    def create_table(self, text_string):
        self.table_df = regex_search(text_string, df)
        self.ui.make_table()
        self.ui.table.setRowCount(len(self.table_df))
        self.ui.table.setRowHeight(10, 10)
        
        row = 0
        for index, df_row in self.table_df.iterrows():
            self.ui.table.setItem(row,
                                  0,
                                  QTableWidgetItem(df_row.Description))
            self.ui.table.setItem(row,
                                  1,
                                  QTableWidgetItem(
                                      str(df_row['Completeness (%)']) + '%'))
            self.ui.table.setRowHeight(row, 25)
            row += 1
        self.ui.table.selectionModel().selectionChanged.connect(self.on_selectionChanged)
    
    def show_table(self):        
        self.ui.stackedWidget.setCurrentWidget(self.ui.table_pg)
        self.ui.show_righthand_widgets()
        plt.close()
        
    def on_selectionChanged(self, selected, deselected):
        self.food_id = 0
        for x in selected.indexes():
            self.food_id = self.table_df.index[x.row()]
        self.create_vis(self.food_id, self.grams, self.sex, self.weight)
        self.ui.stackedWidget.setCurrentWidget(self.ui.vis_pg)
               
    def create_vis(self, food_id, grams, sex, weight):
        plt.close()
        self.change_default_values()
        self.ui.vis_pg.chart = Canvas(self.ui.vis_pg, df, food_id, self.grams,
                                      rdi_df, True, self.sex, self.weight)  
        self.ui.vis_pg.chart.move(0,-13)
           
    def change_default_values(self):
        try:
            if self.ui.gram_field.text() != '':
                self.grams = int(self.ui.gram_field.text())
            if self.ui.weight_field.text() != '':
                self.weight = int(self.ui.weight_field.text())
        except ValueError:
            print('User entered non-int weight or grams')
      
    def plot_diary_chart(self):
        self.ui.diary_pg.chart = Canvas(self.ui.diary_pg,
                                        self.diary_instance.diary,
                                        None, None, rdi_df, True,
                                        self.sex, self.weight)
        self.ui.diary_pg.chart.move(0,-13)
        
def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    close_app = app.exec_()
    plt.close()
    sys.exit(close_app)    
    
if __name__ == '__main__':
    main()
