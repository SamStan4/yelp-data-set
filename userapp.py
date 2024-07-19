import os
import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QAction, QTableWidget, QTableWidgetItem, QVBoxLayout
from PyQt5 import uic, QtCore
from PyQt5.QtGui import QIcon, QPixmap
from data_base_interface import execute_query
from data_base_interface import sql_clean_string

front_end_file_path = "./user_interface.ui"

if not os.path.exists(front_end_file_path):
    raise FileNotFoundError(f"ERROR {front_end_file_path} not found")

ui_main_window, qt_base_class = uic.loadUiType(front_end_file_path)

class yelp_data_interface(QMainWindow):
    def __init__(self) -> None:
        super(yelp_data_interface, self).__init__()
        self.ui = ui_main_window()
        self.ui.setupUi(self)
        self.load_state_list()
        self.ui.state_select.currentTextChanged.connect(self.state_select_action)
        self.ui.city_select.itemSelectionChanged.connect(self.city_select_action)
        self.ui.zipcode_select.itemSelectionChanged.connect(self.zipcode_select_action)
        self.ui.search_button.clicked.connect(self.search_button_action)
        self.ui.clear_button.clicked.connect(self.clear_button_action)
        self.ui.refresh_button.clicked.connect(self.refresh_button_action)

    def load_state_list(self) -> None:
        self.ui.state_select.clear()
        query_str = ("SELECT DISTINCT business.state "
                     "FROM business "
                     "ORDER BY business.state;")
        try:
            result = execute_query(query_string=query_str)
            for row in result:
                self.ui.state_select.addItem(row[0])
        except Exception as e:
            print(f"ERROR -- load state list() -- {e}")
            return
        self.ui.state_select.setCurrentIndex(-1)
        self.ui.city_select.clear()
        self.ui.zipcode_select.clear()
        self.ui.number_of_businesses.clear()
        self.ui.total_population.clear()
        self.ui.average_income.clear()
        self.ui.top_categories.clear()
        self.ui.select_category.clear()
        self.ui.businesses.clear()
        self.ui.popular_businesses.clear()
        self.ui.successful_businesses.clear()

    def state_select_action(self) -> None:
        self.ui.city_select.clear()
        self.ui.zipcode_select.clear()
        self.ui.number_of_businesses.clear()
        self.ui.total_population.clear()
        self.ui.average_income.clear()
        self.ui.top_categories.clear()
        self.ui.select_category.clear()
        current_state = sql_clean_string(str(self.ui.state_select.currentText()))
        query_str = ("SELECT DISTINCT business.city "
                     "FROM business "
                    f"WHERE business.state  = '{current_state}' "
                     "ORDER BY business.city")
        if self.ui.state_select.currentIndex() < 0:
            return
        try:
            result = execute_query(query_string=query_str)
            for row in result:
                self.ui.city_select.addItem(row[0])
        except Exception as e:
            print(f"ERROR -- state_select_action() -- {e}")
            return

    def city_select_action(self) -> None:
        self.ui.zipcode_select.clear()
        self.ui.number_of_businesses.clear()
        self.ui.total_population.clear()
        self.ui.average_income.clear()
        self.ui.top_categories.clear()
        self.ui.select_category.clear()
        try:
            city = sql_clean_string(str(self.ui.city_select.selectedItems()[0].text()))
            state = sql_clean_string(str(self.ui.state_select.currentText()))
            query_str = ("SELECT DISTINCT business.zipcode "
                         "FROM business "
                        f"WHERE business.state = '{state}' AND business.city = '{city}' "
                         "ORDER BY business.zipcode;")
            try:
                result = execute_query(query_string=query_str)
                for row in result:
                    self.ui.zipcode_select.addItem(row[0])
            except Exception as e:
                print(f"ERROR -- city_select_action() -- {e}")
        except:
            return

    def zipcode_select_action(self) -> None:
        self.ui.number_of_businesses.clear()
        self.ui.total_population.clear()
        self.ui.average_income.clear()
        self.ui.top_categories.clear()
        self.ui.select_category.clear()
        try:
            state = sql_clean_string(str(self.ui.state_select.currentText()))
            city = sql_clean_string(str(self.ui.city_select.selectedItems()[0].text()))
            zipcode = sql_clean_string(str(self.ui.zipcode_select.selectedItems()[0].text()))
            num_business_query = ("SELECT COUNT(*) "
                                  "FROM business "
                                 f"WHERE business.state = '{state}' AND business.city = '{city}' AND business.zipcode = '{zipcode}';")
            total_population_query = ("SELECT zipcodedata.population "
                                      "FROM zipcodedata "
                                     f"WHERE zipcodedata.zipcode = '{zipcode}';")
            average_income_query = ("SELECT zipcodedata.meanincome "
                                    "FROM zipcodedata "
                                   f"WHERE zipcodedata.zipcode = '{zipcode}';")
            popular_categories_query = ("SELECT COUNT(*) AS num_businesses, categories.category_name "
                                        "FROM business INNER JOIN categories ON business.business_id = categories.business_id "
                                       f"WHERE business.zipcode = '{zipcode}' "
                                        "GROUP BY categories.category_name "
                                        "ORDER BY num_businesses DESC;")
            categories_query = ("SELECT DISTINCT categories.category_name "
                                "FROM business INNER JOIN categories ON business.business_id = categories.business_id "
                               f"WHERE business.zipcode = '{zipcode}' "
                                "ORDER BY categories.category_name;")
            try:
                num_business_result = str(execute_query(query_string=num_business_query)[0][0])
                self.ui.number_of_businesses.setText(num_business_result)
            except Exception as e:
                print(f"ERROR -- zipcode_select_action() -- {e}")
            try:
                population_result = str(execute_query(query_string=total_population_query)[0][0])
                self.ui.total_population.setText(population_result)
            except Exception as e:
                print(f"ERROR -- zipcode_select_action() -- {e}")
            try:
                average_income_result = str(execute_query(query_string=average_income_query)[0][0])
                self.ui.average_income.setText(average_income_result)
            except Exception as e:
                print(f"ERROR -- zipcode_select_action() -- {e}")
            try:
                popular_categories_result = execute_query(popular_categories_query)
                style = "::section {""background-color: #f3f3f3; }"
                self.ui.top_categories.horizontalHeader().setStyleSheet(style)
                self.ui.top_categories.setColumnCount(len(popular_categories_result[0]))
                self.ui.top_categories.setRowCount(len(popular_categories_result))
                self.ui.top_categories.setHorizontalHeaderLabels(['# businesses', 'category'])
                for i in range (0, len(popular_categories_result), 1):
                    for j in range (0, len(popular_categories_result[i]), 1):
                        self.ui.top_categories.setItem(i, j, QTableWidgetItem(str(popular_categories_result[i][j])))
            except Exception as e:
                print(f"ERROR -- zipcode_select_action() -- {e}")
            try:
                categories_result = execute_query(query_string=categories_query)
                for row in categories_result:
                    self.ui.select_category.addItem(row[0])
            except Exception as e:
                print(f"ERROR -- zipcode_select_action() -- {e}")
        except:
            return
        
    def search_button_action(self) -> None:
        try:
            state = sql_clean_string(str(self.ui.state_select.currentText()))
            city = sql_clean_string(str(self.ui.city_select.selectedItems()[0].text()))
            zipcode = sql_clean_string(str(self.ui.zipcode_select.selectedItems()[0].text()))
            category = sql_clean_string(str(self.ui.select_category.selectedItems()[0].text()))
            self.ui.businesses.clear()
            query_str = ("SELECT business.name, business.address, business.city, business.stars, business.review_count, business.num_checkins "
                         "FROM business INNER JOIN categories ON business.business_id = categories.business_id "
                        f"WHERE business.state = '{state}' AND business.city = '{city}' AND business.zipcode = '{zipcode}' AND categories.category_name = '{category}' "
                         "ORDER BY business.name;")
            try:
                result = execute_query(query_string=query_str)
                style = "::section {""background-color: #f3f3f3; }"
                self.ui.businesses.horizontalHeader().setStyleSheet(style)
                self.ui.businesses.setColumnCount(len(result[0]))
                self.ui.businesses.setRowCount(len(result))
                self.ui.businesses.setHorizontalHeaderLabels(['business name', 'address', 'city', 'stars', 'review\ncount', 'number of\ncheckins'])
                self.ui.businesses.setColumnWidth(0, 201)
                self.ui.businesses.setColumnWidth(1, 215)
                self.ui.businesses.setColumnWidth(2, 100)
                self.ui.businesses.setColumnWidth(3, 50)
                self.ui.businesses.setColumnWidth(4, 50)
                self.ui.businesses.setColumnWidth(5, 75)
                for i in range (0, len(result), 1):
                    for j in range (0, len(result[i]), 1):
                        self.ui.businesses.setItem(i, j, QTableWidgetItem(str(result[i][j])))
            except Exception as e:
                print(f"ERROR -- search_button_action() -- {e}")
        except:
            return

    def clear_button_action(self) -> None:
        self.ui.businesses.clear()

    def refresh_button_action(self) -> None:
        print("refresh")

def main() -> int:
    app = QApplication(sys.argv)
    window = yelp_data_interface()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()