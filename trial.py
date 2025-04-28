import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import time
import random

class VendingMachineGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("JKUAT Soft Drink Vending Machine")
        self.root.geometry("1000x700")
        self.root.configure(bg="#f0f0f0")
        
        # Initialize the vending machine logic
        self.current_amount = 0
        self.drink_price = 50
        self.valid_denominations = [10, 20, 40, 50, 100, 200, 500, 1000]
        self.transaction_history = []
        self.drinks_dispensed = 0
        self.current_state = "q0"
        
        # Initialize stock
        self.drink_types = ["Coca Cola", "Sprite", "Fanta", "Pepsi", "Mountain Dew", "7Up"]
        self.drink_colors = ["#e51c23", "#4caf50", "#ff9800", "#2196f3", "#8bc34a", "#00bcd4"]
        self.stock = {drink: 5 for drink in self.drink_types}  # 5 of each drink
        self.selected_drinks = []
        
        # For animation
        self.animation_in_progress = False
        self.sound_enabled = True
        
        # Admin password
        self.admin_password = "admin123"
        
        # Create the main frames
        self.create_frames()
        
        # Create the UI components
        self.create_header()
        self.create_state_display()
        self.create_coin_buttons()
        self.create_drink_selection()
        self.create_action_buttons()
        self.create_transaction_history()
        self.create_diagram_view()
        
        # Initial state visualization
        self.update_state_display()
        self.update_diagram()
    
    def create_frames(self):
        # Main container
        self.main_container = tk.Frame(self.root, bg="#f0f0f0")
        self.main_container.pack(fill=tk.BOTH, expand=True)
        
        # Top frame for header
        self.top_frame = tk.Frame(self.main_container, bg="#f0f0f0", height=80)
        self.top_frame.pack(fill=tk.X)
        
        # Bottom container for content
        self.bottom_container = tk.Frame(self.main_container, bg="#f0f0f0")
        self.bottom_container.pack(fill=tk.BOTH, expand=True)
        
        # Left frame for controls
        self.left_frame = tk.Frame(self.bottom_container, bg="#f0f0f0", width=400)
        self.left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Middle frame for drink display
        self.middle_frame = tk.Frame(self.bottom_container, bg="#e8e8e8", width=300)
        self.middle_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Right frame for state diagram
        self.right_frame = tk.Frame(self.bottom_container, bg="#e0e0e0", width=300)
        self.right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    def create_header(self):
        header_frame = tk.Frame(self.top_frame, bg="#4CAF50", height=80)
        header_frame.pack(fill=tk.X)
        
        title = tk.Label(header_frame, text="JKUAT Soft Drink Vending Machine", 
                         font=("Arial", 18, "bold"), bg="#4CAF50", fg="white")
        title.pack(pady=8)
        
        subtitle = tk.Label(header_frame, text="All drinks cost 50 KShs", 
                            font=("Arial", 12), bg="#4CAF50", fg="white")
        subtitle.pack()
        
        # Admin button (small and discreet)
        self.admin_button = tk.Button(header_frame, text="Admin", 
                                     command=self.admin_login,
                                     bg="#4CAF50", fg="white", bd=0)
        self.admin_button.place(relx=0.95, rely=0.5, anchor=tk.E)
    
    def create_state_display(self):
        state_frame = tk.Frame(self.left_frame, bg="#ffffff", bd=2, relief=tk.GROOVE)
        state_frame.pack(fill=tk.X, pady=10, padx=20)
        
        # Current state display
        self.state_label = tk.Label(state_frame, text="Current State: Idle", 
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
        
        # Selected drinks display
        self.selection_label = tk.Label(state_frame, text="Selected: None", 
                                    font=("Arial", 12), bg="#ffffff")
        self.selection_label.pack(pady=5)
    
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
    
    def create_drink_selection(self):
        # Create a frame for the drinks display
        drink_frame = tk.LabelFrame(self.middle_frame, text="Available Drinks", 
                                   font=("Arial", 12), bg="#e8e8e8")
        drink_frame.pack(fill=tk.BOTH, expand=True, pady=10, padx=10)
        
        # Container for drink display
        self.drink_container = tk.Frame(drink_frame, bg="#ffffff")
        self.drink_container.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Create the drinks display
        self.drink_buttons = {}
        self.stock_labels = {}
        
        for i, drink in enumerate(self.drink_types):
            row = i // 2
            col = i % 2
            
            # Create a frame for each drink
            drink_item_frame = tk.Frame(self.drink_container, bg="#ffffff", 
                                      highlightbackground="#ddd", highlightthickness=1)
            drink_item_frame.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
            
            # Add weight to rows and columns
            self.drink_container.grid_rowconfigure(row, weight=1)
            self.drink_container.grid_columnconfigure(col, weight=1)
            
            # Drink can visual
            can_canvas = tk.Canvas(drink_item_frame, width=80, height=120, 
                                  bg="#ffffff", bd=0, highlightthickness=0)
            can_canvas.pack(pady=5)
            
            # Draw the drink can
            self.draw_drink_can(can_canvas, self.drink_colors[i], drink)
            
            # Drink name
            drink_name = tk.Label(drink_item_frame, text=drink, 
                                font=("Arial", 10, "bold"), bg="#ffffff")
            drink_name.pack()
            
            # Stock label
            stock_label = tk.Label(drink_item_frame, text=f"Stock: {self.stock[drink]}", 
                                  font=("Arial", 9), bg="#ffffff")
            stock_label.pack()
            
            # In the create_drink_selection method, modify the select_button creation:
            select_button = tk.Button(drink_item_frame, text="SELECT DRINK", 
                         command=lambda d=drink: self.select_drink(d),
                         width=12, height=2, bg="#4CAF50", fg="white",
                         font=("Arial", 10, "bold"))  # Make text bold and larger
            select_button.pack(pady=10)  # Increase padding
            
            # Store references
            self.drink_buttons[drink] = select_button
            self.stock_labels[drink] = stock_label
        
        # Dispensing area
        dispense_frame = tk.LabelFrame(self.middle_frame, text="Dispensing Area", 
                                     font=("Arial", 12), bg="#e8e8e8")
        dispense_frame.pack(fill=tk.X, pady=10, padx=10)
        
        # Create a canvas for dispensing animation
        self.dispense_canvas = tk.Canvas(dispense_frame, width=280, height=100, 
                                       bg="#d0d0d0", bd=2, relief=tk.SUNKEN)
        self.dispense_canvas.pack(padx=5, pady=5)
        
        # Draw the dispensing tray
        self.dispense_canvas.create_rectangle(20, 70, 260, 90, fill="#a0a0a0", outline="#808080")
        self.dispense_canvas.create_text(140, 50, text="No drinks dispensed yet", tags=("dispense_text"))
    
    def draw_drink_can(self, canvas, color, name):
        # Draw a can shape
        canvas.create_oval(20, 10, 60, 30, fill=color, outline="")
        canvas.create_rectangle(20, 20, 60, 100, fill=color, outline="")
        canvas.create_oval(20, 90, 60, 110, fill=color, outline="")
        
        # Add some details
        canvas.create_rectangle(22, 30, 58, 60, fill="white", outline="")
        canvas.create_text(40, 45, text=name.split()[0], font=("Arial", 7, "bold"))
        
        # Add shine effect
        canvas.create_oval(45, 15, 55, 25, fill="white", outline="")
    
    def create_action_buttons(self):
        action_frame = tk.Frame(self.left_frame, bg="#f0f0f0")
        action_frame.pack(fill=tk.X, pady=10, padx=20)
        
        # Dispense button
        self.dispense_button = tk.Button(action_frame, text="Dispense Selected Drinks", 
                                        command=self.dispense_drinks,
                                        width=18, height=2, bg="#a0a0a0", fg="white",
                                        state=tk.DISABLED)  # Initially disabled
        self.dispense_button.pack(side=tk.LEFT, padx=5)
        
        # Cancel button
        self.cancel_button = tk.Button(action_frame, text="Cancel & Refund", 
                                      command=self.cancel_transaction,
                                      width=15, height=2, bg="#f44336", fg="white")
        self.cancel_button.pack(side=tk.LEFT, padx=5)
        
        # Toggle sound button
        self.sound_button = tk.Button(action_frame, text="🔊 Sound On", 
                                     command=self.toggle_sound,
                                     width=10, height=1, bg="#e0e0e0")
        self.sound_button.pack(side=tk.RIGHT, padx=5, pady=5)
    
    def create_transaction_history(self):
        history_frame = tk.LabelFrame(self.left_frame, text="Transaction History", 
                                     font=("Arial", 12), bg="#f0f0f0")
        history_frame.pack(fill=tk.BOTH, expand=True, pady=10, padx=20)
        
        # Create a scrollable text widget for history
        scrollbar = tk.Scrollbar(history_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.history_text = tk.Text(history_frame, height=6, width=40, 
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
        # Update state
        old_state = self.current_state
        self.current_amount += denomination
        
        if self.current_state == "q0":
            self.current_state = "Waiting for Payment"
        
        # Update UI
        self.update_state_display()
        self.update_diagram()
        self.add_history(f"Inserted {denomination} KShs")
        
        # Play coin sound
        if self.sound_enabled:
            self.play_sound("coin")
        
        # Flash the status
        self.status_label.config(text=f"Inserted {denomination} KShs", fg="#008000")
        self.root.after(1500, lambda: self.status_label.config(text="Ready"))
        
        # Enable buttons based on available amount
        self.update_drink_buttons()
        self.update_dispense_button()
    
    def select_drink(self, drink):
        # Check if drink is in stock
        if self.stock[drink] <= 0:
            messagebox.showinfo("Out of Stock", f"Sorry, {drink} is out of stock!")
            return
        
        # Check if user has enough money
        if self.current_amount < self.drink_price:
            needed = self.drink_price - self.current_amount
            messagebox.showinfo("Insufficient Funds", f"Please insert {needed} more KShs")
            return
        
        # Add drink to selection
        self.selected_drinks.append(drink)
        
        # Update display
        self.update_selection_display()
        self.status_label.config(text=f"Selected {drink}", fg="#008000")
        
        # Play selection sound
        if self.sound_enabled:
            self.play_sound("select")
        
        # Update dispense button
        self.update_dispense_button()
    
    def update_selection_display(self):
        if not self.selected_drinks:
            self.selection_label.config(text="Selected: None")
        else:
            # Count occurrences of each drink
            drink_counts = {}
            for drink in self.selected_drinks:
                if drink in drink_counts:
                    drink_counts[drink] += 1
                else:
                    drink_counts[drink] = 1
            
            # Create display text
            selection_text = "Selected: " + ", ".join(f"{count}x {drink}" for drink, count in drink_counts.items())
            self.selection_label.config(text=selection_text)
    
    def dispense_drinks(self):
        if not self.selected_drinks:
            messagebox.showinfo("No Selection", "Please select a drink first!")
            return
        
        # Calculate total cost
        total_cost = len(self.selected_drinks) * self.drink_price
        
        # Check if user has enough money
        if self.current_amount < total_cost:
            needed = total_cost - self.current_amount
            messagebox.showinfo("Insufficient Funds", f"Please insert {needed} more KShs")
            return
        
        # Update state
        old_state = self.current_state
        self.current_state = "Processing Purchase"
        self.update_state_display()
        self.update_diagram()
        
        # Start dispensing process
        self.animate_dispensing()
    
    def animate_dispensing(self):
        if self.animation_in_progress:
            return
        
        self.animation_in_progress = True
        self.current_state = "Dispensing Drink(s)"
        self.update_state_display()
        
        # Clear previous dispense text
        self.dispense_canvas.delete("dispense_text")
        self.dispense_canvas.create_text(140, 30, text="Dispensing...", tags=("dispense_text"), font=("Arial", 10, "bold"))
        
        # Calculate cost and change
        total_cost = len(self.selected_drinks) * self.drink_price
        change = self.current_amount - total_cost
        
        # Process each selected drink
        self.process_next_drink(0, change)
    
    def process_next_drink(self, index, change):
        if index >= len(self.selected_drinks):
            # All drinks dispensed
            self.finish_dispensing(change)
            return
        
        drink = self.selected_drinks[index]
        
        # Update stock
        self.stock[drink] -= 1
        self.stock_labels[drink].config(text=f"Stock: {self.stock[drink]}")
        
        # Update buttons if stock depleted
        if self.stock[drink] <= 0:
            self.drink_buttons[drink].config(state=tk.DISABLED, bg="#a0a0a0")
        
        # Animate can dropping
        self.animate_can_drop(drink, index, change)
    
    def animate_can_drop(self, drink, index, change):
        # Get color for this drink
        color = self.drink_colors[self.drink_types.index(drink)]
        
        # Create can at top
        can_id = self.dispense_canvas.create_oval(120, 10, 160, 30, fill=color, outline="")
        rect_id = self.dispense_canvas.create_rectangle(120, 20, 160, 40, fill=color, outline="")
        bottom_id = self.dispense_canvas.create_oval(120, 30, 160, 50, fill=color, outline="")
        
        # Play dispensing sound
        if self.sound_enabled:
            self.play_sound("dispense")
        
        # Animate dropping
        self.animate_drop(can_id, rect_id, bottom_id, 0, drink, index, change)
    
    def animate_drop(self, can_id, rect_id, bottom_id, step, drink, index, change):
        if step < 6:  # Number of animation steps
            # Move can down
            self.dispense_canvas.move(can_id, 0, 10)
            self.dispense_canvas.move(rect_id, 0, 10)
            self.dispense_canvas.move(bottom_id, 0, 10)
            
            # Schedule next frame
            self.root.after(100, lambda: self.animate_drop(
                can_id, rect_id, bottom_id, step + 1, drink, index, change))
        else:
            # Animation complete for this can
            # Process next drink after a delay
            self.root.after(500, lambda: self.process_next_drink(index + 1, change))
    
    def finish_dispensing(self, change):
        # Update state and UI
        self.drinks_dispensed += len(self.selected_drinks)
        
        # Calculate cost
        total_cost = len(self.selected_drinks) * self.drink_price
        
        # Update amount and state
        self.current_amount = change
        self.current_state = "Idle" if change == 0 else "Waiting for Payment"
        
        # Update display
        self.dispense_canvas.delete("dispense_text")
        self.dispense_canvas.create_text(140, 30, 
                                       text=f"{len(self.selected_drinks)} drink(s) dispensed!",
                                       tags=("dispense_text"), font=("Arial", 10))
        
        if change > 0:
            self.dispense_canvas.create_text(140, 50, 
                                          text=f"Change: {change} KShs",
                                          tags=("dispense_text"), font=("Arial", 10))
        
        # Play change sound if needed
        if change > 0 and self.sound_enabled:
            self.play_sound("change")
        
        # Log transaction
        dispensed_summary = ", ".join(sorted(self.selected_drinks))
        self.add_history(f"Dispensed: {dispensed_summary}. Total: {total_cost} KShs.")
        if change > 0:
            self.add_history(f"Change returned: {change} KShs")
        
        # Clear selection
        dispensed_drinks = self.selected_drinks.copy()
        self.selected_drinks = []
        self.update_selection_display()
        
        # Show message box
        message = f"Thank you for your purchase!\n\nDrinks dispensed: {len(dispensed_drinks)}\n"
        if change > 0:
            message += f"Change: {change} KShs"
        messagebox.showinfo("Purchase Complete", message)
        
        # Update state display and diagram
        self.update_state_display()
        self.update_diagram()
        
        # Reset status
        self.status_label.config(text="Ready", fg="#008000")
        self.animation_in_progress = False
        
        # Check if any drinks are out of stock
        self.check_stock_status()
    
    def check_stock_status(self):
        out_of_stock = [drink for drink, count in self.stock.items() if count <= 0]
        
        if len(out_of_stock) == len(self.drink_types):
            # All drinks out of stock
            self.current_state = "Out of Stock"
            self.status_label.config(text="ALL DRINKS OUT OF STOCK", fg="#ff0000")
            messagebox.showwarning("Out of Stock", "All drinks are out of stock!")
            self.update_state_display()
            self.update_diagram()
    
    def cancel_transaction(self):
        if self.animation_in_progress:
            return
        
        if self.current_amount == 0 and not self.selected_drinks:
            self.status_label.config(text="No money to return", fg="#ff0000")
            return
        
        # Get refund amount
        refund = self.current_amount
        old_state = self.current_state
        
        # Update state
        self.current_amount = 0
        self.current_state = "Idle"
        
        # Clear selection
        self.selected_drinks = []
        self.update_selection_display()
        
        # Update UI
        self.status_label.config(text=f"Returned {refund} KShs", fg="#ff0000")
        self.add_history(f"Transaction cancelled. Refunded {refund} KShs")
        
        # Play refund sound
        if self.sound_enabled and refund > 0:
            self.play_sound("refund")
        
        # Show message
        if refund > 0:
            messagebox.showinfo("Transaction Cancelled", f"Refunded {refund} KShs")
        
        # Update display and diagram
        self.update_state_display()
        self.update_diagram()
        
        # Reset status
        self.root.after(1500, lambda: self.status_label.config(text="Ready", fg="#008000"))
    
    def update_state_display(self):
        # Update labels
        self.state_label.config(text=f"Current State: {self.current_state}")
        self.amount_label.config(text=f"Amount: {self.current_amount} KShs")
        
        # Update button states
        self.update_drink_buttons()
        self.update_dispense_button()
    
    def update_drink_buttons(self):
        for drink in self.drink_types:
            # Enable/disable based on stock and funds
            if self.stock[drink] <= 0:
                self.drink_buttons[drink].config(state=tk.DISABLED, bg="#a0a0a0")
            elif self.current_amount >= self.drink_price:
                self.drink_buttons[drink].config(state=tk.NORMAL, bg="#4CAF50")
            else:
                self.drink_buttons[drink].config(state=tk.DISABLED, bg="#a0a0a0")
    
    def update_dispense_button(self):
        # Enable dispense button if selected drinks and enough money
        if self.selected_drinks and self.current_amount >= len(self.selected_drinks) * self.drink_price:
            self.dispense_button.config(state=tk.NORMAL, bg="#4CAF50")
        elif self.current_amount >= self.drink_price:
            # Enable dispense button if we have enough money for at least one drink
            # This allows direct dispensing when money is inserted
            self.dispense_button.config(state=tk.NORMAL, bg="#4CAF50")
        else:
            self.dispense_button.config(state=tk.DISABLED, bg="#a0a0a0")
    
    def update_diagram(self):
        # Clear canvas
        self.canvas.delete("all")
        
        # Define states to show
        states = ["Idle", "Waiting for Payment", "Processing Purchase", 
                 "Dispensing Drink(s)", "Out of Stock"]
        
        # Define state positions
        positions = {
            "Idle": (150, 100),
            "Waiting for Payment": (150, 200),
            "Processing Purchase": (300, 200),
            "Dispensing Drink(s)": (300, 100),
            "Out of Stock": (225, 300)
        }
        
        # Draw states
        radius = 40
        for state in states:
            x, y = positions[state]
            
            # Highlight current state
            fill_color = "#ffcc00" if state == self.current_state else "white"
            outline_color = "red" if state == self.current_state else "black"
            outline_width = 3 if state == self.current_state else 1
            
            self.canvas.create_oval(x-radius, y-radius, x+radius, y+radius, 
                                   fill=fill_color, outline=outline_color, width=outline_width)
            
            # Wrap text if needed
            if len(state) > 10:
                lines = state.split()
                if len(lines) == 1:
                    # Split long word
                    mid = len(state) // 2
                    self.canvas.create_text(x, y-10, text=state[:mid])
                    self.canvas.create_text(x, y+10, text=state[mid:])
                else:
                    # Use existing space
                    self.canvas.create_text(x, y-10, text=lines[0])
                    self.canvas.create_text(x, y+10, text=" ".join(lines[1:]))
            else:
                self.canvas.create_text(x, y, text=state)
        
        # Draw transitions
        self.draw_transition("Idle", "Waiting for Payment", "Insert Money", positions)
        self.draw_transition("Waiting for Payment", "Processing Purchase", "Select & Dispense", positions)
        self.draw_transition("Processing Purchase", "Dispensing Drink(s)", "Confirm Purchase", positions)
        self.draw_transition("Dispensing Drink(s)", "Idle", "Complete (No Change)", positions)
        self.draw_transition("Dispensing Drink(s)", "Waiting for Payment", "Complete (With Change)", positions)
        self.draw_transition("Waiting for Payment", "Idle", "Cancel", positions)
        self.draw_transition("Waiting for Payment", "Out of Stock", "All Drinks Sold", positions)
        self.draw_transition("Out of Stock", "Idle", "Refill", positions)
    
    def draw_transition(self, from_state, to_state, label, positions):
        x1, y1 = positions[from_state]
        x2, y2 = positions[to_state]
        
        # Calculate control points for curved lines
        if from_state == "Dispensing Drink(s)" and to_state == "Waiting for Payment":
            # Make a curved line
            cx = (x1 + x2) / 2 + 80
            cy = (y1 + y2) / 2
            
            # Draw a curved line
            self.canvas.create_line(x1+40, y1, cx, cy, x2+40, y2, 
                                   smooth=True, arrow=tk.LAST, width=1.5)
            
            # Position label
            self.canvas.create_text(cx+20, cy-10, text=label, anchor=tk.W)
        elif from_state == "Idle" and to_state == "Waiting for Payment":
            # Vertical line
            self.canvas.create_line(x1, y1+40, x2, y2-40, arrow=tk.LAST, width=1.5)
            self.canvas.create_text((x1+x2)/2 + 40, (y1+y2)/2, text=label, anchor=tk.W)
        elif from_state == "Waiting for Payment" and to_state == "Idle":
            # Return line
            self.canvas.create_line(x1-30, y1-30, x2-30, y2+30, arrow=tk.LAST, width=1.5)
            self.canvas.create_text((x1+x2)/2 - 60, (y1+y2)/2, text=label, anchor=tk.E)
        else:
            # Draw a direct line
            self.canvas.create_line(x1+40*((x2-x1)/((x2-x1)**2+(y2-y1)**2)**0.5), 
                                  y1+40*((y2-y1)/((x2-x1)**2+(y2-y1)**2)**0.5),
                                  x2-40*((x2-x1)/((x2-x1)**2+(y2-y1)**2)**0.5), 
                                  y2-40*((y2-y1)/((x2-x1)**2+(y2-y1)**2)**0.5),
                                  arrow=tk.LAST, width=1.5)
            
            # Position label
            mid_x = (x1 + x2) / 2
            mid_y = (y1 + y2) / 2
            offset = 15  # Offset to avoid overlapping with the line
            self.canvas.create_text(mid_x, mid_y - offset, text=label)
    
    def add_history(self, message):
        timestamp = time.strftime("%H:%M:%S")
        entry = f"[{timestamp}] {message}\n"
        
        # Enable text widget for editing
        self.history_text.config(state=tk.NORMAL)
        
        # Insert at the beginning
        # Enable text widget for editing
        self.history_text.config(state=tk.NORMAL)
        
        # Insert at the beginning
        self.history_text.insert("1.0", entry)
        
        # Disable text widget again
        self.history_text.config(state=tk.DISABLED)
    
    def play_sound(self, sound_type):
        """Simulate playing a sound effect"""
        # In a real implementation, you would use a sound library like pygame.mixer
        # For this simulation, we'll just print what sound would be played
        sound_names = {
            "coin": "Clink!",
            "select": "Click!",
            "dispense": "Thunk!",
            "change": "Jingle!",
            "refund": "Ching!",
            "error": "Buzz!"
        }
        
        print(f"Playing sound: {sound_names.get(sound_type, 'Beep!')}")
        # In real app: pygame.mixer.Sound(f"sounds/{sound_type}.wav").play()
    
    def toggle_sound(self):
        """Toggle sound effects on/off"""
        self.sound_enabled = not self.sound_enabled
        if self.sound_enabled:
            self.sound_button.config(text="🔊 Sound On")
        else:
            self.sound_button.config(text="🔇 Sound Off")
    
    def admin_login(self):
        """Prompt for admin password"""
        password = simpledialog.askstring("Admin Login", 
                                         "Enter admin password:", 
                                         show='*')
        if password == self.admin_password:
            self.open_admin_panel()
        else:
            messagebox.showerror("Access Denied", "Incorrect password")
    
    def open_admin_panel(self):
        """Open the admin control panel"""
        admin_window = tk.Toplevel(self.root)
        admin_window.title("Admin Control Panel")
        admin_window.geometry("500x400")
        admin_window.configure(bg="#f0f0f0")
        
        # Add header
        header = tk.Label(admin_window, text="Vending Machine Admin Panel", 
                         font=("Arial", 16, "bold"), bg="#4CAF50", fg="white",
                         pady=10)
        header.pack(fill=tk.X)
        
        # Add tabs
        tab_control = ttk.Notebook(admin_window)
        
        # Stock management tab
        stock_tab = tk.Frame(tab_control, bg="#f0f0f0")
        tab_control.add(stock_tab, text="Stock Management")
        
        # Create stock controls
        stock_frame = tk.Frame(stock_tab, bg="#f0f0f0")
        stock_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Create a grid of stock controls
        stock_controls = {}
        row = 0
        for drink in self.drink_types:
            # Drink name
            tk.Label(stock_frame, text=drink, font=("Arial", 12), bg="#f0f0f0").grid(
                row=row, column=0, sticky=tk.W, pady=5)
            
            # Current stock
            tk.Label(stock_frame, text="Current Stock:", bg="#f0f0f0").grid(
                row=row, column=1, padx=10)
            
            stock_var = tk.StringVar(value=str(self.stock[drink]))
            stock_entry = tk.Entry(stock_frame, textvariable=stock_var, width=5)
            stock_entry.grid(row=row, column=2)
            
            # Buttons to adjust stock
            tk.Button(stock_frame, text="+", width=3,
                     command=lambda d=drink, s=stock_var: self.adjust_stock(d, s, 1)).grid(
                row=row, column=3, padx=2)
            
            tk.Button(stock_frame, text="-", width=3,
                     command=lambda d=drink, s=stock_var: self.adjust_stock(d, s, -1)).grid(
                row=row, column=4, padx=2)
            
            # Store reference
            stock_controls[drink] = stock_var
            row += 1
        
        # Add refill all button
        tk.Button(stock_frame, text="Refill All to Maximum (5)",
                 command=lambda: self.refill_all_stock(stock_controls),
                 bg="#4CAF50", fg="white", pady=5).grid(
            row=row, column=0, columnspan=5, sticky=tk.EW, pady=10)
        
        # Sales report tab
        sales_tab = tk.Frame(tab_control, bg="#f0f0f0")
        tab_control.add(sales_tab, text="Sales Report")
        
        # Create simple sales report
        report_frame = tk.Frame(sales_tab, bg="#f0f0f0")
        report_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Add sales statistics
        tk.Label(report_frame, text="Sales Statistics", 
                font=("Arial", 14, "bold"), bg="#f0f0f0").pack(anchor=tk.W)
        
        tk.Label(report_frame, text=f"Total Drinks Dispensed: {self.drinks_dispensed}", 
                font=("Arial", 12), bg="#f0f0f0", pady=5).pack(anchor=tk.W)
        
        tk.Label(report_frame, text=f"Total Revenue: {self.drinks_dispensed * self.drink_price} KShs", 
                font=("Arial", 12), bg="#f0f0f0", pady=5).pack(anchor=tk.W)
        
        # Transaction log
        tk.Label(report_frame, text="Transaction Log", 
                font=("Arial", 14, "bold"), bg="#f0f0f0", pady=10).pack(anchor=tk.W)
        
        log_frame = tk.Frame(report_frame, bg="white", bd=1, relief=tk.SUNKEN)
        log_frame.pack(fill=tk.BOTH, expand=True)
        
        scrollbar = tk.Scrollbar(log_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        log_text = tk.Text(log_frame, height=10, yscrollcommand=scrollbar.set)
        log_text.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=log_text.yview)
        
        # Copy transaction history
        log_text.insert(tk.END, self.history_text.get("1.0", tk.END))
        log_text.config(state=tk.DISABLED)
        
        # Maintenance tab
        maint_tab = tk.Frame(tab_control, bg="#f0f0f0")
        tab_control.add(maint_tab, text="Maintenance")
        
        # Create maintenance controls
        maint_frame = tk.Frame(maint_tab, bg="#f0f0f0")
        maint_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        tk.Label(maint_frame, text="Maintenance Controls", 
                font=("Arial", 14, "bold"), bg="#f0f0f0").pack(anchor=tk.W, pady=10)
        
        # Reset counter button
        tk.Button(maint_frame, text="Reset Transaction Counter",
                 command=self.reset_transaction_counter,
                 bg="#e0e0e0", pady=5).pack(anchor=tk.W, pady=5, fill=tk.X)
        
        # Clear history button
        tk.Button(maint_frame, text="Clear Transaction History",
                 command=self.clear_transaction_history,
                 bg="#e0e0e0", pady=5).pack(anchor=tk.W, pady=5, fill=tk.X)
        
        # Change password button
        tk.Button(maint_frame, text="Change Admin Password",
                 command=lambda: self.change_admin_password(admin_window),
                 bg="#e0e0e0", pady=5).pack(anchor=tk.W, pady=5, fill=tk.X)
        
        # Show tabs
        tab_control.pack(expand=1, fill=tk.BOTH)
        
        # Close button
        tk.Button(admin_window, text="Close Admin Panel",
                 command=admin_window.destroy,
                 bg="#f44336", fg="white", pady=8).pack(pady=10)
    
    def adjust_stock(self, drink, stock_var, amount):
        """Adjust stock level of a drink"""
        current = int(stock_var.get())
        new_value = max(0, min(current + amount, 10))  # Limit between 0 and 10
        
        # Update stock variable
        stock_var.set(str(new_value))
        
        # Update actual stock
        self.stock[drink] = new_value
        
        # Update stock display
        self.stock_labels[drink].config(text=f"Stock: {new_value}")
        
        # Update button states
        self.update_drink_buttons()
        
        # Check if we're no longer out of stock
        if self.current_state == "Out of Stock" and any(count > 0 for count in self.stock.values()):
            self.current_state = "Idle"
            self.status_label.config(text="Ready", fg="#008000")
            self.update_state_display()
            self.update_diagram()
    
    def refill_all_stock(self, stock_controls):
        """Refill all drinks to maximum stock level"""
        for drink, stock_var in stock_controls.items():
            # Set to maximum (5)
            stock_var.set("5")
            self.stock[drink] = 5
            
            # Update stock display
            self.stock_labels[drink].config(text="Stock: 5")
        
        # Log the refill
        self.add_history("Admin: Refilled all drinks to maximum stock")
        
        # Update button states
        self.update_drink_buttons()
        
        # If we were out of stock, update state
        if self.current_state == "Out of Stock":
            self.current_state = "Idle"
            self.status_label.config(text="Ready", fg="#008000")
            self.update_state_display()
            self.update_diagram()
    
    def reset_transaction_counter(self):
        """Reset the transaction counter"""
        self.drinks_dispensed = 0
        messagebox.showinfo("Counter Reset", "Transaction counter has been reset to zero.")
    
    def clear_transaction_history(self):
        """Clear the transaction history"""
        # Clear text widget
        self.history_text.config(state=tk.NORMAL)
        self.history_text.delete("1.0", tk.END)
        self.history_text.config(state=tk.DISABLED)
        
        # Clear history list
        self.transaction_history = []
        
        messagebox.showinfo("History Cleared", "Transaction history has been cleared.")
    
    def change_admin_password(self, parent_window):
        """Change the admin password"""
        # Ask for current password
        current_pwd = simpledialog.askstring("Password Change", 
                                           "Enter current password:", 
                                           parent=parent_window,
                                           show='*')
        
        if current_pwd != self.admin_password:
            messagebox.showerror("Error", "Incorrect current password")
            return
        
        # Ask for new password
        new_pwd = simpledialog.askstring("Password Change", 
                                       "Enter new password:", 
                                       parent=parent_window,
                                       show='*')
        
        if not new_pwd:
            return
        
        # Confirm new password
        confirm_pwd = simpledialog.askstring("Password Change", 
                                           "Confirm new password:", 
                                           parent=parent_window,
                                           show='*')
        
        if new_pwd != confirm_pwd:
            messagebox.showerror("Error", "Passwords do not match")
            return
        
        # Set new password
        self.admin_password = new_pwd
        messagebox.showinfo("Success", "Admin password has been changed successfully")


def main():
    root = tk.Tk()
    app = VendingMachineGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()