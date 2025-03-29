import tkinter as tk
from tkinter import ttk, messagebox
import time

class VendingMachineGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("JKUAT Soft Drink Vending Machine")
        self.root.geometry("800x600")
        self.root.configure(bg="#f0f0f0")
        
        # Initialize the vending machine logic
        self.current_amount = 0
        self.drink_price = 50
        self.valid_denominations = [10, 20, 40, 50, 100, 200, 500, 1000]
        self.transaction_history = []
        self.drinks_dispensed = 0
        self.current_state = "q0"
        
        # Create the main frames
        self.create_frames()
        
        # Create the UI components
        self.create_header()
        self.create_state_display()
        self.create_coin_buttons()
        self.create_action_buttons()
        self.create_transaction_history()
        self.create_diagram_view()
        
        # Initial state visualization
        self.update_state_display()
        self.update_diagram()
    
    def create_frames(self):
        # Left frame for controls
        self.left_frame = tk.Frame(self.root, bg="#f0f0f0", width=400)
        self.left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Right frame for state diagram
        self.right_frame = tk.Frame(self.root, bg="#e0e0e0", width=400)
        self.right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    def create_header(self):
        header_frame = tk.Frame(self.left_frame, bg="#f0f0f0")
        header_frame.pack(fill=tk.X, pady=10)
        
        title = tk.Label(header_frame, text="JKUAT Soft Drink Vending Machine", 
                         font=("Arial", 16, "bold"), bg="#f0f0f0")
        title.pack()
        
        subtitle = tk.Label(header_frame, text="All drinks cost 50 KShs", 
                            font=("Arial", 12), bg="#f0f0f0")
        subtitle.pack()
    
    def create_state_display(self):
        state_frame = tk.Frame(self.left_frame, bg="#ffffff", bd=2, relief=tk.GROOVE)
        state_frame.pack(fill=tk.X, pady=10, padx=20)
        
        # Current state display
        self.state_label = tk.Label(state_frame, text="Current State: q0", 
                                   font=("Arial", 12, "bold"), bg="#ffffff")
        self.state_label.pack(pady=5)
        
        # Current amount display
        self.amount_label = tk.Label(state_frame, text="Amount: 0 KShs", 
                                    font=("Arial", 12), bg="#ffffff")
        self.amount_label.pack(pady=5)
        
        # Status display
        self.status_label = tk.Label(state_frame, text="Ready", 
                                    font=("Arial", 12), bg="#ffffff", fg="#008000")
        self.status_label.pack(pady=5)
    
    def create_coin_buttons(self):
        coin_frame = tk.LabelFrame(self.left_frame, text="Insert Money", 
                                  font=("Arial", 12), bg="#f0f0f0")
        coin_frame.pack(fill=tk.X, pady=10, padx=20)
        
        # Create buttons for each denomination
        for i, denom in enumerate(self.valid_denominations):
            row = i // 4
            col = i % 4
            
            button = tk.Button(coin_frame, text=f"{denom} KShs", 
                              command=lambda d=denom: self.insert_money(d),
                              width=10, height=2, bg="#e0e0e0")
            button.grid(row=row, column=col, padx=5, pady=5)
    
    def create_action_buttons(self):
        action_frame = tk.Frame(self.left_frame, bg="#f0f0f0")
        action_frame.pack(fill=tk.X, pady=10, padx=20)
        
        # Dispense button
        self.dispense_button = tk.Button(action_frame, text="Dispense Drink", 
                                        command=self.dispense_drink,
                                        width=15, height=2, bg="#4CAF50", fg="white")
        self.dispense_button.pack(side=tk.LEFT, padx=10)
        
        # Cancel button
        self.cancel_button = tk.Button(action_frame, text="Cancel", 
                                      command=self.cancel_transaction,
                                      width=15, height=2, bg="#f44336", fg="white")
        self.cancel_button.pack(side=tk.LEFT, padx=10)
    
    def create_transaction_history(self):
        history_frame = tk.LabelFrame(self.left_frame, text="Transaction History", 
                                     font=("Arial", 12), bg="#f0f0f0")
        history_frame.pack(fill=tk.BOTH, expand=True, pady=10, padx=20)
        
        # Create a scrollable text widget for history
        scrollbar = tk.Scrollbar(history_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.history_text = tk.Text(history_frame, height=10, width=40, 
                                   yscrollcommand=scrollbar.set)
        self.history_text.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.history_text.yview)
        
        # Make the text widget read-only
        self.history_text.config(state=tk.DISABLED)
    
    def create_diagram_view(self):
        diagram_frame = tk.LabelFrame(self.right_frame, text="State Diagram", 
                                     font=("Arial", 12), bg="#e0e0e0")
        diagram_frame.pack(fill=tk.BOTH, expand=True, pady=10, padx=10)
        
        # Create a canvas for the state diagram
        self.canvas = tk.Canvas(diagram_frame, bg="white")
        self.canvas.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
    
    def insert_money(self, denomination):
        self.current_amount += denomination
        self.current_state = f"q{self.current_amount}"
        
        # Update UI
        self.update_state_display()
        self.update_diagram()
        self.add_history(f"Inserted {denomination} KShs")
        
        # Flash the status
        self.status_label.config(text=f"Inserted {denomination} KShs", fg="#008000")
        self.root.after(1500, lambda: self.status_label.config(text="Ready"))
    
    def dispense_drink(self):
        if self.current_amount < self.drink_price:
            needed = self.drink_price - self.current_amount
            self.status_label.config(text=f"Need {needed} more KShs", fg="#ff0000")
            messagebox.showinfo("Insufficient Funds", f"Please insert {needed} more KShs")
            return
        
        # Dispense drink and calculate change
        self.drinks_dispensed += 1
        change = self.current_amount - self.drink_price
        old_state = self.current_state
        
        # Update state
        self.current_amount = change
        self.current_state = f"q{self.current_amount}"
        
        # Update UI with animation
        self.status_label.config(text="Dispensing drink...", fg="#008000")
        self.root.update()
        time.sleep(1)  # Simulate dispensing time
        
        # Show change message
        if change > 0:
            self.status_label.config(text=f"Drink dispensed! Change: {change} KShs")
            self.add_history(f"Drink dispensed. Change: {change} KShs")
            messagebox.showinfo("Drink Dispensed", f"Enjoy your drink!\nChange: {change} KShs")
        else:
            self.status_label.config(text="Drink dispensed! No change.")
            self.add_history("Drink dispensed. No change.")
            messagebox.showinfo("Drink Dispensed", "Enjoy your drink!")
        
        # Refresh to initial state
        self.current_amount = 0
        self.current_state = "q0"
        
        # Update the state display and diagram
        self.update_state_display()
        self.update_diagram()
        
        # Reset status
        self.status_label.config(text="Ready", fg="#008000")
    
    def cancel_transaction(self):
        if self.current_amount == 0:
            self.status_label.config(text="No money to return", fg="#ff0000")
            return
        
        refund = self.current_amount
        old_state = self.current_state
        
        # Update state
        self.current_amount = 0
        self.current_state = "q0"
        
        # Update UI
        self.status_label.config(text=f"Returned {refund} KShs", fg="#ff0000")
        self.add_history(f"Transaction cancelled. Refunded {refund} KShs")
        messagebox.showinfo("Transaction Cancelled", f"Refunded {refund} KShs")
        
        # Refresh to initial state
        self.current_amount = 0
        self.current_state = "q0"
        
        # Update display and diagram
        self.update_state_display()
        self.update_diagram()
        
        # Reset status
        self.status_label.config(text="Ready", fg="#008000")
    
    def update_state_display(self):
        self.state_label.config(text=f"Current State: {self.current_state}")
        self.amount_label.config(text=f"Amount: {self.current_amount} KShs")
        
        # Update dispense button state
        if self.current_amount >= self.drink_price:
            self.dispense_button.config(state=tk.NORMAL, bg="#4CAF50")
        else:
            self.dispense_button.config(state=tk.NORMAL, bg="#A0A0A0")
    
    def update_diagram(self, highlight_transition=False, from_state=None):
        # Clear canvas
        self.canvas.delete("all")
        
        # Define states to show (simplified for visualization)
        visible_states = ["q0", "q10", "q20", "q30", "q40", "q50", "q100"]
        
        # Add the current state if not in visible_states
        if self.current_state not in visible_states and self.current_state != "q0":
            visible_states.append(self.current_state)
        
        # Define state positions
        state_positions = {
            "q0": (100, 100),
            "q10": (200, 50),
            "q20": (300, 50),
            "q30": (400, 50),
            "q40": (500, 50),
            "q50": (200, 150),
            "q100": (300, 150)
        }
        
        # Add position for current state if not defined
        if self.current_state not in state_positions:
            state_positions[self.current_state] = (400, 150)
        
        # Draw states
        radius = 30
        for state in visible_states:
            x, y = state_positions[state]
            
            # Highlight current state
            fill_color = "#ffcc00" if state == self.current_state else "white"
            outline_color = "red" if state == self.current_state else "black"
            outline_width = 3 if state == self.current_state else 1
            
            self.canvas.create_oval(x-radius, y-radius, x+radius, y+radius, 
                                   fill=fill_color, outline=outline_color, width=outline_width)
            self.canvas.create_text(x, y, text=state)
        
        # Draw some transitions
        self.draw_transition("q0", "q10", "10", state_positions)
        self.draw_transition("q0", "q20", "20", state_positions)
        self.draw_transition("q0", "q50", "50", state_positions)
        self.draw_transition("q10", "q20", "10", state_positions)
        self.draw_transition("q20", "q30", "10", state_positions)
        self.draw_transition("q30", "q40", "10", state_positions)
        self.draw_transition("q40", "q50", "10", state_positions)
        self.draw_transition("q50", "q0", "dispense", state_positions)
        self.draw_transition("q50", "q100", "50", state_positions)
        self.draw_transition("q100", "q50", "dispense", state_positions)
        
        # Highlight a specific transition if requested
        if highlight_transition and from_state in state_positions:
            # Find transition to highlight
            if from_state == "q50" and self.current_state == "q0":
                self.highlight_transition("q50", "q0", state_positions)
            elif from_state == "q100" and self.current_state == "q50":
                self.highlight_transition("q100", "q50", state_positions)
            elif from_state == "q0" and self.current_state == "q50":
                self.highlight_transition("q0", "q50", state_positions)
    
    def draw_transition(self, from_state, to_state, label, positions):
        # Check if both states are in positions
        if from_state not in positions or to_state not in positions:
            return
        
        x1, y1 = positions[from_state]
        x2, y2 = positions[to_state]
        
        # Draw the arrow
        self.canvas.create_line(x1, y1, x2, y2, arrow=tk.LAST)
        
        # Draw the label
        label_x = (x1 + x2) / 2
        label_y = (y1 + y2) / 2 - 10
        self.canvas.create_text(label_x, label_y, text=label)
    
    def highlight_transition(self, from_state, to_state, positions):
        x1, y1 = positions[from_state]
        x2, y2 = positions[to_state]
        
        # Draw a highlighted arrow
        self.canvas.create_line(x1, y1, x2, y2, arrow=tk.LAST, 
                               fill="red", width=3)
    
    def add_history(self, message):
        timestamp = time.strftime("%H:%M:%S")
        entry = f"[{timestamp}] {message}\n"
        
        # Enable text widget for editing
        self.history_text.config(state=tk.NORMAL)
        
        # Insert at the beginning
        self.history_text.insert("1.0", entry)
        
        # Disable text widget again
        self.history_text.config(state=tk.DISABLED)

def main():
    root = tk.Tk()
    app = VendingMachineGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()