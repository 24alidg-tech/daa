# doctor_scheduler_with_names.py
# --------------------------------------------
# Doctor Scheduling System (Greedy Algorithm)
# Tkinter GUI with doctor names and total times
# --------------------------------------------

import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt


# ----------------------------
# Scheduling logic (greedy LPT)
# ----------------------------
def greedy_schedule(patients, doctors_list):
    """
    patients: list of (name, time)
    doctors_list: list of doctor dicts [{'id':1,'name':'Dr A','time':0,'appointments':[]}, ...]
    """
    # Sort patients by longest consultation first
    patients_sorted = sorted(patients, key=lambda x: x[1], reverse=True)

    doctors = doctors_list[:]  # operate on a shallow copy

    for name, consult_time in patients_sorted:
        # pick doctor who will be free earliest (min time)
        doctor = min(doctors, key=lambda d: d["time"])
        start = doctor["time"]
        end = start + consult_time
        doctor["appointments"].append((name, start, end))
        doctor["time"] = end

    return doctors


# ----------------------------
# Gantt chart plotting
# ----------------------------
def plot_gantt(doctors):
    fig, ax = plt.subplots(figsize=(9, max(3, len(doctors)*0.6)))
    colors = plt.cm.get_cmap("tab20").colors

    for i, doc in enumerate(doctors):
        for j, (patient, start, end) in enumerate(doc["appointments"]):
            ax.barh(i, width=end - start, left=start, height=0.5, color=colors[j % len(colors)])
            ax.text(start + (end - start)/2, i, patient, va='center', ha='center', color='white', fontsize=8)

    ax.set_yticks(range(len(doctors)))
    ax.set_yticklabels([doc["name"] for doc in doctors])
    ax.set_xlabel("Time (minutes)")
    ax.set_title("Doctor Scheduling - Gantt Chart")
    plt.tight_layout()
    plt.show()


# ----------------------------
# Helper: parse patients text
# ----------------------------
def parse_patients(text):
    lines = text.strip().splitlines()
    patients = []
    for line in lines:
        if not line.strip():
            continue
        if "," in line:
            parts = line.split(",")
            name = parts[0].strip()
            try:
                time = int(parts[1].strip())
            except Exception:
                raise ValueError(f"Invalid time value in line: '{line}'")
            patients.append((name, time))
        else:
            raise ValueError(f"Line must be 'Name, Time' format: '{line}'")
    return patients


# ----------------------------
# Build and run GUI
# ----------------------------
def run_gui():
    root = tk.Tk()
    root.title("Doctor Scheduling System")
    root.geometry("560x620")
    root.configure(bg="#F8FAFC")

    # Header
    header = tk.Frame(root, bg="#0B5FA4", pady=12)
    header.pack(fill="x")
    tk.Label(header, text="Doctor Scheduling System", font=("Helvetica", 18, "bold"), fg="white", bg="#0B5FA4").pack()

    # Input frame
    frame = tk.Frame(root, bg="#F8FAFC", padx=12, pady=12)
    frame.pack(fill="both", expand=True)

    # Row: Number of doctors and doctor names
    top_row = tk.Frame(frame, bg="#F8FAFC")
    top_row.pack(fill="x", pady=(0,10))

    tk.Label(top_row, text="Number of Doctors:", font=("Arial", 11), bg="#F8FAFC").grid(row=0, column=0, sticky="w")
    doctor_count_entry = tk.Entry(top_row, width=6, font=("Arial", 11))
    doctor_count_entry.grid(row=0, column=1, padx=(6,20))
    doctor_count_entry.insert(0, "3")

    tk.Label(top_row, text="Doctor Names (comma separated, optional):", font=("Arial", 11), bg="#F8FAFC").grid(row=1, column=0, columnspan=2, sticky="w", pady=(8,0))
    doctor_names_entry = tk.Entry(top_row, width=50, font=("Arial", 10))
    doctor_names_entry.grid(row=2, column=0, columnspan=2, pady=(4,0))
    doctor_names_entry.insert(0, "Dr. A, Dr. B, Dr. C")  # sample default

    # Patients input
    tk.Label(frame, text="Patients (one per line: Name, Time-in-minutes):", font=("Arial", 11, "bold"), bg="#F8FAFC").pack(anchor="w", pady=(10,4))
    text_frame = tk.Frame(frame, bg="#F8FAFC")
    text_frame.pack(fill="both", expand=False)

    scrollbar = tk.Scrollbar(text_frame)
    scrollbar.pack(side="right", fill="y")

    patients_text = tk.Text(text_frame, width=60, height=14, font=("Consolas", 10))
    patients_text.pack()
    patients_text.insert(tk.END,
                         "Alice, 45\nBob, 30\nCharlie, 20\nDaisy, 50\nEve, 25\nFrank, 15\nGrace, 40")
    patients_text.config(yscrollcommand=scrollbar.set)
    scrollbar.config(command=patients_text.yview)

    # Buttons and result area
    button_frame = tk.Frame(frame, bg="#F8FAFC")
    button_frame.pack(pady=12)

    result_frame = tk.Frame(frame, bg="#F8FAFC")
    result_frame.pack(fill="x", pady=(6,0))

    totals_label = tk.Label(result_frame, text="", font=("Arial", 10), bg="#F8FAFC", justify="left")
    totals_label.pack(anchor="w")

    # Action functions
    def schedule_action():
        try:
            # parse number of doctors
            num_doctors = int(doctor_count_entry.get())
            if num_doctors <= 0:
                messagebox.showwarning("Input error", "Number of doctors must be >= 1")
                return

            # parse doctor names (optional)
            names_raw = doctor_names_entry.get().strip()
            names = []
            if names_raw:
                names = [n.strip() for n in names_raw.split(",") if n.strip()]
            # if provided names less than count, fill defaults
            while len(names) < num_doctors:
                names.append(f"Doctor {len(names)+1}")

            # build doctors list
            doctors_list = []
            for i in range(num_doctors):
                doc_name = names[i] if i < len(names) else f"Doctor {i+1}"
                doctors_list.append({"id": i+1, "name": doc_name, "time": 0, "appointments": []})

            # parse patients
            patients_input = patients_text.get("1.0", tk.END)
            patients = parse_patients(patients_input)
            if not patients:
                messagebox.showwarning("Input error", "Enter at least one patient.")
                return

            # run greedy schedule
            scheduled = greedy_schedule(patients, doctors_list)

            # update totals in GUI
            out_lines = []
            for d in scheduled:
                out_lines.append(f"{d['name']}: Total = {d['time']} min")
            totals_label.config(text="\n".join(out_lines))

            # print to console (optional)
            print("\n--- Scheduled appointments ---")
            for d in scheduled:
                print(f"{d['name']} -> {d['appointments']}   Total: {d['time']}")

            # show Gantt
            plot_gantt(scheduled)

        except ValueError as ve:
            messagebox.showerror("Parsing error", str(ve))
        except Exception as e:
            messagebox.showerror("Error", f"Something went wrong:\n{e}")

    def clear_action():
        doctor_count_entry.delete(0, tk.END)
        doctor_count_entry.insert(0, "3")
        doctor_names_entry.delete(0, tk.END)
        doctor_names_entry.insert(0, "Dr. A, Dr. B, Dr. C")
        patients_text.delete("1.0", tk.END)
        patients_text.insert(tk.END, "Alice, 45\nBob, 30\nCharlie, 20\nDaisy, 50\nEve, 25\nFrank, 15\nGrace, 40")
        totals_label.config(text="")

    # Buttons
    style = ttk.Style()
    style.configure("Accent.TButton", font=("Arial", 11, "bold"), padding=6)
    ttk.Button(button_frame, text="Schedule", style="Accent.TButton", command=schedule_action).grid(row=0, column=0, padx=8)
    ttk.Button(button_frame, text="Clear", style="Accent.TButton", command=clear_action).grid(row=0, column=1, padx=8)

    # Footer
    footer = tk.Label(root, text="Tip: enter patients as 'Name, Time' per line", bg="#F8FAFC", fg="#333", font=("Arial", 9))
    footer.pack(side="bottom", pady=8)

    root.mainloop()


# ----------------------------
# Launch
# ----------------------------
if __name__ == "__main__":
    run_gui()
