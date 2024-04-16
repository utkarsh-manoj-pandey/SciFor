import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from ttkthemes import ThemedStyle

class Patient:
    def __init__(self, patient_id, patient_name, disease, doctor_incharge):
        self.id = patient_id
        self.name = patient_name
        self.disease = disease
        self.doctor = doctor_incharge

class RainbowHospital:
    def __init__(self):
        self.patients = []

    def admit_patient(self, patient):
        self.patients.append(patient)
        messagebox.showinfo("Success", "Patient admitted successfully.")

    def get_patient(self, key, value):
        found_patients = []
        for patient in self.patients:
            if getattr(patient, key, None) == value:
                found_patients.append(patient)
        return found_patients

    def show_all_patients(self):
        return self.patients

    def discharge_patient(self, key, value):
        patients_to_remove = self.get_patient(key, value)
        if not patients_to_remove:
            messagebox.showinfo("Not Found", "Patient not found.")
        else:
            for patient in patients_to_remove:
                self.patients.remove(patient)
            messagebox.showinfo("Success", "Patient discharged successfully.")

class HospitalGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("THE RAINBOW HOSPITAL")

        style = ThemedStyle(self.root)
        style.set_theme("clam")  # Choose a theme from available themes

        self.hospital = RainbowHospital()

        header_font = ("Helvetica", 22, "bold")
        button_font = ("Helvetica", 12, "bold")

        self.label = ttk.Label(root, text="Welcome to The Rainbow Hospital", font=header_font)
        self.label.pack(pady=20)

        style.configure("TButton", font=button_font)

        self.button_admit = ttk.Button(root, text="Admit Patient", command=self.admit_patient, style="TButton")
        self.button_admit.pack(pady=10, padx=20, ipadx=10, ipady=5)

        self.button_get = ttk.Button(root, text="Get Patient Details", command=self.get_patient, style="TButton")
        self.button_get.pack(pady=5, padx=20, ipadx=10, ipady=5)

        self.button_show = ttk.Button(root, text="Show All Patients", command=self.show_all_patients, style="TButton")
        self.button_show.pack(pady=5, padx=20, ipadx=10, ipady=5)

        self.button_discharge = ttk.Button(root, text="Discharge Patient", command=self.discharge_patient,
                                           style="TButton")
        self.button_discharge.pack(pady=5, padx=20, ipadx=10, ipady=5)

        self.button_exit = ttk.Button(root, text="Exit", command=root.destroy, style="TButton")
        self.button_exit.pack(pady=5, padx=20, ipadx=10, ipady=5)

    def admit_patient(self):
        patient_id = self.get_input("Enter patient ID:")
        patient_name = self.get_input("Enter patient name:")
        disease = self.get_input("Enter patient's disease:")
        doctor_incharge = self.get_input("Enter doctor in charge:")
        new_patient = Patient(patient_id, patient_name, disease, doctor_incharge)
        self.hospital.admit_patient(new_patient)

    def get_patient(self):
        search_key = self.get_input("Enter search key (Id/Name/Disease/Doctor):").lower()
        search_value = self.get_input(f"Enter {search_key}:")
        found_patients = self.hospital.get_patient(search_key, search_value)
        if found_patients:
            patient_details = ""
            for patient in found_patients:
                patient_details += f"ID: {patient.id}, Name: {patient.name}, Disease: {patient.disease}, Doctor: {patient.doctor}\n"
            messagebox.showinfo("Patient Details", patient_details)
        else:
            messagebox.showinfo("Not Found", "Patient not found.")

    def show_all_patients(self):
        patients = self.hospital.show_all_patients()
        if patients:
            patient_details = ""
            for patient in patients:
                patient_details += f"ID: {patient.id}, Name: {patient.name}, Disease: {patient.disease}, Doctor: {patient.doctor}\n"
            messagebox.showinfo("All Patients", patient_details)
        else:
            messagebox.showinfo("No Patients", "No patients in the hospital.")

    def discharge_patient(self):
        discharge_key = self.get_input("Enter discharge key (Id/Name/Disease/Doctor):").lower()
        discharge_value = self.get_input(f"Enter {discharge_key}:")
        self.hospital.discharge_patient(discharge_key, discharge_value)

    def get_input(self, prompt):
        return simpledialog.askstring("Input", prompt)

# Main program
if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("400x550")
    root.resizable(True, True)  # Allow window resizing

    gui = HospitalGUI(root)

    root.mainloop()