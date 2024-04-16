import tkinter as tk
from tkinter import ttk
import requests
from datetime import datetime

class CurrencyConverter:
    def __init__(self, root):
        self.root = root
        self.root.title("Currency Converter")
        self.root.geometry("600x500")  # Adjust the width and height as needed

        self.amount_var = tk.DoubleVar()
        self.from_currency_var = tk.StringVar()
        self.to_currency_var = tk.StringVar()
        self.last_updated_var = tk.StringVar()

        header_font = ('Times New Roman', 20, 'bold')
        label_font = ('Times New Roman', 12)
        entry_font = ('Times New Roman', 12)
        button_font = ('Times New Roman', 12, 'bold')

        # Header
        header_label = tk.Label(root, text="Currency Converter", font=header_font, bg='#4CAF50', fg='white')
        header_label.grid(row=0, column=0, columnspan=2, pady=(50, 20), sticky='n', ipadx=20)

        # Entry for entering the amount
        amount_label = tk.Label(root, text="Amount:", font=label_font)
        amount_label.grid(row=1, column=0, pady=5, sticky='e')

        self.amount_entry = tk.Entry(root, textvariable=self.amount_var, font=entry_font, width=15, bd=3, relief=tk.SOLID, highlightthickness=0, bg='#F5F5F5')
        self.amount_entry.grid(row=1, column=1, pady=5, sticky='w')

        # Dropdown for selecting the 'from' currency
        from_currency_label = tk.Label(root, text="From Currency:", font=label_font)
        from_currency_label.grid(row=2, column=0, pady=5, sticky='e')

        self.from_currency_combobox = ttk.Combobox(root, textvariable=self.from_currency_var, font=entry_font, width=15, state="readonly", background='#F5F5F5')
        self.from_currency_combobox['values'] = ('ALL', 'AFN', 'ARS', 'AWG', 'AUD', 'AZN', 'BSD', 'BBD', 'BYN', 'BZD', 'BMD', 'BOB', 'BAM', 'BWP', 'BGN', 'BND', 'KHR', 'CAD', 'KYD', 'CLP', 'CNY', 'COP', 'CRC', 'HRK', 'CUP', 'CZK', 'DKK', 'DOP', 'XCD', 'EGP', 'SVC', 'EUR', 'FKP', 'FJD', 'GHS', 'GIP', 'GTQ', 'GGP', 'GYD', 'HNL', 'HKD', 'HUF', 'ISK', 'INR')
        self.from_currency_combobox.grid(row=2, column=1, pady=5, sticky='w')

        # Dropdown for selecting the 'to' currency
        to_currency_label = tk.Label(root, text="To Currency:", font=label_font)
        to_currency_label.grid(row=3, column=0, pady=5, sticky='e')

        self.to_currency_combobox = ttk.Combobox(root, textvariable=self.to_currency_var, font=entry_font, width=15, state="readonly", background='#F5F5F5')
        self.to_currency_combobox['values'] = ('ALL', 'AFN', 'ARS', 'AWG', 'AUD', 'AZN', 'BSD', 'BBD', 'BYN', 'BZD', 'BMD', 'BOB', 'BAM', 'BWP', 'BGN', 'BND', 'KHR', 'CAD', 'KYD', 'CLP', 'CNY', 'COP', 'CRC', 'HRK', 'CUP', 'CZK', 'DKK', 'DOP', 'XCD', 'EGP', 'SVC', 'EUR', 'FKP', 'FJD', 'GHS', 'GIP', 'GTQ', 'GGP', 'GYD', 'HNL', 'HKD', 'HUF', 'ISK', 'INR')
        self.to_currency_combobox.grid(row=3, column=1, pady=5, sticky='w')

        # Button to perform the conversion
        convert_button = tk.Button(root, text="Convert", command=self.convert_currency, font=button_font, bg='#3498db', fg='white', padx=10, pady=15, bd=0, highlightthickness=0, cursor='hand2')
        convert_button.grid(row=4, column=0, pady=20, padx=(10, 5), sticky='e')

        # Clear button
        clear_button = tk.Button(root, text="Clear", command=self.clear_fields, font=button_font, bg='#e74c3c', fg='white', padx=10, pady=15, bd=0, highlightthickness=0, cursor='hand2')
        clear_button.grid(row=4, column=1, pady=20, padx=(5, 10), sticky='w')

        # Label for displaying results
        self.result_label = tk.Label(root, text="", fg='#4CAF50', font=label_font)
        self.result_label.grid(row=5, column=0, columnspan=2, pady=20, sticky='n')

        # Label for displaying last update time
        last_updated_label = tk.Label(root, textvariable=self.last_updated_var, font=label_font, fg='gray')
        last_updated_label.grid(row=6, column=0, columnspan=2, pady=10)

        # Configure row and column to center components
        root.columnconfigure(0, weight=1)
        root.columnconfigure(1, weight=1)
        root.rowconfigure(0, weight=1)
        root.rowconfigure(1, weight=1)
        root.rowconfigure(2, weight=1)
        root.rowconfigure(3, weight=1)
        root.rowconfigure(4, weight=1)
        root.rowconfigure(5, weight=1)
        root.rowconfigure(6, weight=1)

    def convert_currency(self):
        amount = self.amount_var.get()
        from_currency = self.from_currency_var.get()
        to_currency = self.to_currency_var.get()

        if amount and from_currency and to_currency:
            try:
                # Make a request to the ExchangeRate-API
                api_url = f'https://api.exchangerate-api.com/v4/latest/{from_currency}'
                response = requests.get(api_url)
                data = response.json()

                # Check if the API request was successful
                if response.status_code == 200 and 'rates' in data:
                    # Get the exchange rate
                    exchange_rate = data['rates'].get(to_currency)

                    if exchange_rate is not None:
                        # Calculate the converted amount
                        converted_amount = amount * exchange_rate

                        # Display the result
                        result_str = f"{amount} {from_currency} is equal to {converted_amount:.2f} {to_currency}"
                        self.result_label.config(text=result_str)

                        # Display last update time
                        timestamp = data.get('time_last_updated_utc', '')
                        if timestamp:
                            try:
                                timestamp = int(timestamp)
                                last_updated_time = datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S UTC')
                                self.last_updated_var.set(f"Last Updated: {last_updated_time}")
                            except ValueError:
                                self.last_updated_var.set("Last Updated: Unknown")
                        else:
                            self.last_updated_var.set("Last Updated: Unknown")
                    else:
                        error_msg = f"Error: {to_currency} not found in the rates data."
                        self.result_label.config(text=error_msg, fg='red')
                        self.last_updated_var.set("")
                else:
                    error_msg = f"Error: Unable to fetch data from the API. Status code: {response.status_code}"
                    self.result_label.config(text=error_msg, fg='red')
                    self.last_updated_var.set("")

            except Exception as e:
                error_msg = f"Error: {e}"
                self.result_label.config(text=error_msg, fg='red')
                self.last_updated_var.set("")
        else:
            error_msg = "Error: Please enter amount, from currency, and to currency."
            self.result_label.config(text=error_msg, fg='red')
            self.last_updated_var.set("")

    def clear_fields(self):
        self.amount_var.set("")
        self.from_currency_var.set("")
        self.to_currency_var.set("")
        self.result_label.config(text="")
        self.last_updated_var.set("")

if __name__ == "__main__":
    root = tk.Tk()
    converter = CurrencyConverter(root)
    root.mainloop()