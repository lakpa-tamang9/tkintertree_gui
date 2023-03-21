from tkinter import *
from tkinter import filedialog
from tkinter import ttk
import json


class App:
    def __init__(self):
        root = Tk()
        root.title("Automation App")
        root.geometry("1280x960")

        # DEfine the columns in the tree
        table = ttk.Treeview(
            root, columns=("col1", "col2", "col3", "col4", "col5"), show="headings"
        )
        table.pack()

        table_info = [
            ("col1", "S.N", 2),
            ("col2", "Filename", 80),
            ("col3", "Path", 200),
            ("col4", "Time(mins)", 20),
            ("col5", "Type", 20),
        ]

        # Create table headings and columns
        for info in table_info:
            table.heading(info[0], text=info[1])
            table.column(info[0], width=info[2], anchor="center")
        table.pack(fill="both", expand=True)

        # Loading table with json data
        with open("./settings.json", "r") as f:
            settings = json.load(f)

            for i, setting in enumerate(settings):
                table.insert(
                    "",
                    "end",
                    values=(
                        i + 1,
                        setting["file_name"],
                        setting["path"],
                        setting["duration_min"],
                        setting["type"],
                    ),
                )
        # Button methods
        def add_record():
            time = []
            filepath = filedialog.askopenfilename()
            filename = filepath.split("/")[-1]
            filetype = filename.split(".")[-1]
            filename = filename.split(".")[0]

            count = get_row_count()
            if filetype == "png":
                open_popup(time)
                # print(time)
                table.insert(
                    parent="",
                    index="end",
                    values=(count + 1, filename, filepath, time[0], filetype),
                )
            else:
                # print(filepath)
                time = "N/A"
                table.insert(
                    parent="",
                    index="end",
                    values=(count + 1, filename, filepath, time[0], filetype),
                )

        def open_popup(time):
            def enter_button():
                val = entry.get().strip()
                if val.isdigit():
                    time.append(int(val))
                top.destroy()

            top = Toplevel(root)

            entry = Entry(top)
            entry.pack()
            enter_button = Button(top, text="Enter", command=enter_button)
            enter_button.pack(pady=10)
            top.geometry("600x200")
            top.title("Enter time")
            Label(
                top,
                text="Enter the time in minutes that you want to execute this file?",
                font=("Mistral 10 bold"),
            ).place(x=150, y=80)
            # wait the user to close window
            top.wait_window()

        def remove_all():
            for record in table.get_children():
                table.delete(record)

        def remove_one():
            x = table.selection()[0]
            table.delete(x)

        def get_row_count():
            return len(table.get_children())

        def save_button():
            settings = []

            for row_id in table.get_children():
                row_data = table.item(row_id)["values"]
                sn = row_data[0]
                filename = row_data[1]
                file_path = row_data[2]
                time_duration = row_data[3]
                file_type = row_data[4]

                setting = {
                    "file_name": filename,
                    "path": file_path,
                    "duration_min": time_duration,
                    "type": file_type,
                }
                settings.append(setting)

            # Write the table data to a JSON file
            with open("settings.json", "w") as json_file:
                json.dump(settings, json_file)

        def update_record():
            selected = table.focus()
            values = list(table.item(selected, "values"))
            # time_box.insert(0, values[3])
            values[3] = time_box.get()
            values = tuple(values)
            # Save new data
            table.item(
                selected,
                text="",
                values=(values[0], values[1], values[2], values[3], values[4]),
            )
            time_box.delete(0, END)
            temp_label.config(
                text=f"Time updated for {values[1]}. New time is {values[3]} minutes. "
            )

        # Add buttons
        add_record = Button(root, text="Add", command=add_record)
        add_record.pack(padx=20, side=LEFT)

        save_button = Button(root, text="Save", command=save_button)
        save_button.pack(padx=10, side=LEFT)

        # Adding new frame in the root
        add_frame = Frame(root)
        add_frame.pack(pady=20, side=LEFT)

        tm = Label(add_frame, text="Enter new time:")
        tm.grid(row=0, column=0)

        # Entry boxes
        time_box = Entry(add_frame)
        time_box.grid(row=0, column=1)

        update_button = Button(root, text="Update time", command=update_record)
        update_button.pack(padx=20, side=LEFT)

        # Remove records
        remove_one = Button(root, text="Delete", command=remove_one)
        remove_one.pack(padx=10, side=LEFT)

        remove_all = Button(root, text="Delete all", command=remove_all)
        remove_all.pack(padx=10, side=LEFT)

        # Printing new time in window
        temp_label = Label(root, text="")
        temp_label.pack(pady=20)

        root.mainloop()


if __name__ == "__main__":
    App()
