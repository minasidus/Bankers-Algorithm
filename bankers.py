from asyncio import sleep
from threading import Thread
from PyQt5.QtWidgets import (QGridLayout, QLineEdit, QComboBox,
                            QVBoxLayout, QApplication, QWidget,
                            QLabel, QPushButton, QDialog,
                            QListWidget, QScrollArea)
from PyQt5.QtCore import Qt

def banker_algorithm(num_processes, total_resources, available_resources, process_allocation, max_need, process_request, process):
    # init with zeros
    process_request=[0,0,0,0]

    needed_resources = []
    
    
    process = 0
    for i in range(num_processes):
        process_needed = []
        for j in range(len(total_resources)):
            needed = max_need[i][j] - process_allocation[i][j]
            process_needed.append(needed)
        needed_resources.append(process_needed)
    
    
    finished_processes = [False for x in range(num_processes)]

    # initialize the safe sequence list
    safe_sequence = []
    all_steps = []
    
    
    

    all_steps.append("Available resources: {}".format(available_resources) )



    if all(process_request[i] <= needed_resources[i][j] and process_request[i] <= available_resources[j] for i in range(num_processes) for j in range(len(total_resources))):
        # assume deadlock present
        deadlock_detected = True

        # update the needed_resources and available_resources lists
        for j in range(len(total_resources)):
            needed_resources[process][j] -= process_request[j]
            available_resources[j] -= process_request[j]

        for _ in range(num_processes):
            for i in range(num_processes):
                # check if the process has already finished or if its needed resources are greater than the available resources
                if not finished_processes[i] and all(needed_resources[i][j] <= available_resources[j] for j in range(len(total_resources))):
                    # process can complete
                    deadlock_detected = False

                    # add the process to the safe sequence
                    safe_sequence.append(i)

                    # update the available resources and finished_processes list
                    for j in range(len(total_resources)):
                        available_resources[j] += process_allocation[i][j]
                    finished_processes[i] = True

                all_steps.append("Safe sequence: {}".format(available_resources))
                all_steps.append("Process {} can complete".format(i))
                all_steps.append("Available resources: {}".format(available_resources))

                for k in range(num_processes):
                    print("Process {}: {}".format(k,needed_resources[k]))
                print()

            # if deadlock is detected and not all processes have finished, then it is not safe to grant any more requests
            if deadlock_detected and False in finished_processes:
                # revert the needed_resources and available_resources lists to their original values
                for j in range(len(total_resources)):
                    needed_resources[process][j] += process_request[j]
                    available_resources[j] += process_request[j]
                print("Not safe")
                return None, False, all_steps

            # if all processes have finished, then the system is in a safe state
            elif all(finished_processes):
                break

        # print the final state
        print("Final state:")
        all_steps.append("Final state:")
        print("Safe sequence: {}".format(safe_sequence))
        all_steps.append("Safe sequence: {}".format(safe_sequence))
        print("Available resources: {}".format(available_resources))
        all_steps.append("Available resources: {}".format(available_resources))
        
        all_steps.append("Finished")
        

        print("Safe sequence:")
        for i in safe_sequence:
            print("Process ", i, end=",")
        print("Done")

    else:
        print("Unsafe.")
        return None, False, all_steps

    return safe_sequence, True, all_steps

class App(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Banker\'s Algorithm')
        # self.setFixedSize(1200, 800)
    # Create labels
        self.total = QLabel('Total Resources:')
        self.available = QLabel('Available Resources:')
        self.max = QLabel('Max Need:')
        self.process_allocation = QLabel('Process Alloc:')
        self.request_resc = QLabel('Request Resources:')
        self.status_label = QLabel('Status:')

        # Create line edit widgets for input
        self.total_res_inputs = [QLineEdit() for x in range(4)]
        self.avail_res_inputs = [QLineEdit() for x in range(4)]
        self.max_need_inputs = [[QLineEdit() for x in range(4)] for y in range(3)]
        self.proc_alloc_inputs = [[QLineEdit() for x in range(4)] for y in range(3)]
        self.req_res_inputs = [QLineEdit() for x in range(4)]

        # Create dropdown list widget for selecting process
        self.process_selection = QComboBox()
        self.process_selection.clear()
        self.process_selection.addItems(['P1', 'P2', 'P3'])
      
        # Create submit button
        self.submit_button = QPushButton('Submit')
        self.submit_button.clicked.connect(self.submit_button_clicked)

        # Create grid layout
        self.grid = QGridLayout()
        self.grid.setSpacing(20)

 # Add labels and line edits to grid
        self.grid.addWidget(self.total, 0, 0)
        for i, input_widget in enumerate(self.total_res_inputs):
            self.grid.addWidget(input_widget, 0, i + 1)

        self.grid.addWidget(self.available, 1, 0)
        for i, input_widget in enumerate(self.avail_res_inputs):
            self.grid.addWidget(input_widget, 1, i + 1)

        self.grid.addWidget(self.max, 2, 0)
        for i, input_row in enumerate(self.max_need_inputs):
            for j, input_widget in enumerate(input_row):
                self.grid.addWidget(input_widget, i + 2, j + 1)

        self.grid.addWidget(self.process_allocation, 6, 0)
        for i, input_row in enumerate(self.proc_alloc_inputs):
            for j, input_widget in enumerate(input_row):
                self.grid.addWidget(input_widget, i + 6, j + 1)

        self.grid.addWidget(self.request_resc, 9, 0)
        self.grid.addWidget(self.process_selection, 10, 0)
        for i, input_widget in enumerate(self.req_res_inputs):
            input_widget.setText("0")
            self.grid.addWidget(input_widget, 10, i + 1)
            

        self.grid.addWidget(self.submit_button, 11, 4)
        self.grid.addWidget(self.status_label, 11, 0, 1, 4)

        # Set layout
        self.setLayout(self.grid)


    def get_input_data(self):
        """
        Get input data from the line edit widgets and return as lists
        """
        total_resources = [int(input_widget.text()) for input_widget in self.total_res_inputs]
        available_resources = [int(input_widget.text()) for input_widget in self.avail_res_inputs]
        max_need = [[int(input_widget.text()) for input_widget in input_row] for input_row in self.max_need_inputs]
        process_allocation = [[int(input_widget.text()) for input_widget in input_row] for input_row in self.proc_alloc_inputs]
        request_resources = [int(input_widget.text()) for input_widget in self.req_res_inputs]
        process = self.process_selection.currentText()
        return total_resources, available_resources, max_need, process_allocation, request_resources, process

    def display_steps(self, items):
        dialog = QDialog(self)
        dialog.setWindowTitle('showing steps')  
        layout = QVBoxLayout()

        # labeling
        for item in items:
            label = QLabel(item)
            layout.addWidget(label)

        dialog.setLayout(layout)

        dialog.exec_()    


    def display_list(self, items):
        # Create list of strings

        # Create new window
        new_window = QWidget()
        new_window.setWindowTitle('List Display')

        # Create label and add to layout
        label = QLabel('List of Items:', new_window)
        label.setGeometry(50, 50, 200, 30)

        # Create list widget and add items
        list_widget = QListWidget(new_window)
        list_widget.setGeometry(50, 80, 300, 200)
        for item in items:
            list_widget.addItem(item)

        # Add list widget to scroll area and set layout
        scroll_area = QScrollArea(new_window)
        scroll_area.setGeometry(50, 80, 300, 200)
        scroll_area.setWidget(list_widget)

        # Set layout and show window
        layout = QVBoxLayout(new_window)
        layout.addWidget(label)
        layout.addWidget(scroll_area)
        new_window.setLayout(layout)
        new_window.show()
        
    def submit_button_clicked(self):
        # Get input data
        total_resources, available_resources, max_need, process_allocation, request_resources, process = self.get_input_data()

        if process == "P1":
            process = 0
        elif process =="P2":
            process = 1
        elif process =="P3":
            process = 2

        
        safe_sequence, status, steps = banker_algorithm(3, total_resources, available_resources, process_allocation, max_need, request_resources, process)

        print(safe_sequence, status)
        # Display result
        if safe_sequence:
            self.status_label.setText(f'Safe sequence: {safe_sequence}\nStatus: {status}')
        else:
            self.status_label.setText(f'Status: {status}')
        self.display_steps(steps)
        # t = Thread(target=self.display_steps, args=(steps,))
        # t.start()




app = QApplication([])
window = App()
window.show()
app.exec_()