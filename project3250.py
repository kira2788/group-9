import pandas as pd
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk
import os
from datetime import datetime


class CPU_Scheduler:
    def __init__(self, tasks):
        # Initialize the scheduler with a list of tasks
        self.tasks = tasks

    def FCFS(self):
        # First-Come, First-Served (FCFS) scheduling algorithm
        tasks = sorted(self.tasks, key=lambda x: x['arrival_time'])
        schedule = []
        current_time = 0
        for task in tasks:
            current_time += task['burst_time']
            schedule.append({'task': task['name'], 'time': current_time})
        return schedule

    def SJF(self):
        # Shortest Job First (SJF) scheduling algorithm
        tasks = sorted(self.tasks, key=lambda x: x['burst_time'])
        schedule = []
        current_time = 0
        for task in tasks:
            current_time += task['burst_time']
            schedule.append({'task': task['name'], 'time': current_time})
        return schedule

    def Priority(self):
        # Priority scheduling algorithm
        tasks = sorted(self.tasks, key=lambda x: (x['arrival_time'] != 0, -x['priority'], x['arrival_time']))
        schedule = []
        current_time = 0
        for task in tasks:
            current_time += task['burst_time']
            schedule.append({'task': task['name'], 'time': current_time})
        return schedule

    def Round_Robin(self, quantum):
        # Round Robin scheduling algorithm with a given quantum time slice
        if quantum <= 0:
            raise ValueError("Quantum must be greater than 0")
        schedule = []
        tasks = [{'name': task['name'], 'burst_time': task['burst_time']} for task in self.tasks]
        time = 0
        while tasks:
            for task in tasks[:]:
                if task['burst_time'] <= quantum:
                    time += task['burst_time']
                    schedule.append({'task': task['name'], 'time': time})
                    tasks.remove(task)
                else:
                    time += quantum
                    task['burst_time'] -= quantum
        return schedule


def visualize_schedule(schedule, algorithm):
    # 检查 schedule 内容
    print("Schedule:", schedule)

    tasks = [entry['task'] for entry in schedule if 'task' in entry]
    times = [entry['time'] for entry in schedule if 'time' in entry]

    plt.figure(figsize=(10, 6))
    plt.bar(tasks, times, color='skyblue')
    plt.title(f'Scheduling Results - {algorithm}')
    plt.xlabel('Tasks')
    plt.ylabel('Completion Time')
    plt.show()


def calculate_schedule():
    # Calculate the schedule based on user input
    selected_algorithm = algorithm_var.get()
    quantum = quantum_entry.get()
    output_text.delete('1.0', tk.END)
    output_text.insert(tk.END, f"Selected Algorithm: {selected_algorithm}\n")

    if selected_algorithm == "Round Robin":
        if not quantum.isdigit() or int(quantum) <= 0:
            output_text.insert(tk.END, "Error: Please enter a valid positive quantum!\n")
            return
        quantum = int(quantum)
        try:
            result = scheduler.Round_Robin(quantum)
        except ValueError as e:
            output_text.insert(tk.END, f"Error: {e}\n")
            return
    elif selected_algorithm in ["FCFS", "SJF", "Priority"]:
        try:
            result = getattr(scheduler, selected_algorithm)()
        except Exception as e:
            output_text.insert(tk.END, f"Error: {e}\n")
            return
    else:
        output_text.insert(tk.END, "Error: Unknown algorithm!\n")
        return

    if result:
        output_text.insert(tk.END, "Schedule Result:\n")
        for item in result:
            output_text.insert(tk.END, f"{item}\n")

        # Visualize the results with a bar plot
        visualize_schedule(result, selected_algorithm)

        # Save results to a file with a timestamp to avoid overwriting
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        filename = f"schedule_result_{timestamp}.txt"
        with open(filename, "w") as file:
            file.write(f"Selected Algorithm: {selected_algorithm}\n")
            file.write("Schedule Result:\n")
            for item in result:
                file.write(f"{item}\n")
        output_text.insert(tk.END, f"Results have been saved to {filename}\n")
    else:
        output_text.insert(tk.END, "No tasks to schedule.\n")


def input_tasks():
    # Function to input tasks from the user
    task_data = task_entry.get("1.0", tk.END).strip().split('\n')
    print("Received task data:", task_data)
    tasks = []
    for task in task_data:
        task_info = task.split(',')
        if len(task_info) != 4:
            output_text.insert(tk.END, "Error: Invalid task format.\n")
            return
        try:
            name, arrival_time, burst_time, priority = task_info
            tasks.append({
                'name': name.strip(),
                'arrival_time': int(arrival_time.strip()),
                'burst_time': int(burst_time.strip()),
                'priority': int(priority.strip())
            })
        except ValueError:
            output_text.insert(tk.END, "Error: Invalid task data type.\n")
            return
    global scheduler
    scheduler = CPU_Scheduler(tasks)
    output_text.insert(tk.END, "Tasks added successfully.\n")


# Create the main window
root = tk.Tk()
root.title("CPU Scheduling Simulator")

# User input for tasks
tk.Label(root, text="Enter tasks (name, arrival_time, burst_time, priority):").grid(row=0, column=0, padx=10, pady=10)
task_entry = tk.Text(root, height=5, width=50)
task_entry.grid(row=1, column=0, columnspan=2, padx=10, pady=10)
input_button = tk.Button(root, text="Input Tasks", command=input_tasks).grid(row=2, column=0, columnspan=2, pady=10)

# Algorithm selection
algorithm_var = tk.StringVar(value="FCFS")
tk.Label(root, text="Select Algorithm:").grid(row=3, column=0, padx=10, pady=10)
algorithm_menu = ttk.Combobox(root, textvariable=algorithm_var, values=["FCFS", "SJF", "Priority", "Round Robin"])
algorithm_menu.grid(row=3, column=1, padx=10, pady=10)

# Quantum input for Round Robin
tk.Label(root, text="Quantum (for Round Robin):").grid(row=4, column=0, padx=10, pady=10)
quantum_entry = tk.Entry(root)
quantum_entry.grid(row=4, column=1, padx=10, pady=10)

# Calculate schedule button
calculate_button = tk.Button(root, text="Calculate", command=calculate_schedule).grid(row=5, column=0, columnspan=2,
                                                                                      pady=10)

# Output text area
output_text = tk.Text(root, height=10, width=50)
output_text.grid(row=6, column=0, columnspan=2, padx=10, pady=10)

# Start the GUI event loop
root.mainloop()
