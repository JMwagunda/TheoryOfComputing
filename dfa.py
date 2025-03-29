class VendingMachineSimulation:
    def __init__(self):
        # Initialize the machine with 0 money
        self.current_amount = 0
        self.drink_price = 50
        self.valid_denominations = [10, 20, 40, 50, 100, 200, 500, 1000]
        self.transaction_history = []
        self.drinks_dispensed = 0
        self.current_state = "q0"
    
    def insert_money(self, denomination):
        """Insert money into the vending machine."""
        if denomination not in self.valid_denominations:
            return f"Error: {denomination} is not a valid denomination."
        
        self.current_amount += denomination
        self.current_state = f"q{self.current_amount}"
        
        # Add to transaction history
        self.transaction_history.append(f"Inserted {denomination} KShs")
        
        return f"Inserted {denomination} KShs. Current amount: {self.current_amount} KShs"
    
    def dispense_drink(self):
        """Attempt to dispense a drink if enough money is inserted."""
        if self.current_amount < self.drink_price:
            return f"Insufficient funds. Please insert at least {self.drink_price - self.current_amount} more KShs"
        
        # Dispense drink and calculate change
        self.drinks_dispensed += 1
        change = self.current_amount - self.drink_price
        old_state = self.current_state
        
        # Update state
        self.current_amount = change
        self.current_state = f"q{self.current_amount}"
        
        # Add to transaction history
        if change > 0:
            self.transaction_history.append(f"Drink dispensed. Change: {change} KShs")
            return f"Drink dispensed! Your change is {change} KShs. New state: {self.current_state}"
        else:
            self.transaction_history.append("Drink dispensed. No change.")
            return "Drink dispensed! No change. New state: q0"
    
    def cancel_transaction(self):
        """Cancel the current transaction and return all inserted money."""
        if self.current_amount == 0:
            return "No money to return."
        
        refund = self.current_amount
        old_state = self.current_state
        
        # Update state
        self.current_amount = 0
        self.current_state = "q0"
        
        # Add to transaction history
        self.transaction_history.append(f"Transaction cancelled. Refunded {refund} KShs")
        
        return f"Transaction cancelled. {refund} KShs returned. New state: q0"
    
    def display_state(self):
        """Show the current state of the machine."""
        return f"Current State: {self.current_state}\nAmount: {self.current_amount} KShs"
    
    def display_history(self):
        """Show transaction history."""
        if not self.transaction_history:
            return "No transactions yet."
        
        history = "\n".join(f"{i+1}. {t}" for i, t in enumerate(self.transaction_history[-5:]))
        return f"Recent Transactions:\n{history}"
    
    def simulate_transition(self, input_value=None):
        """Show what happens when a specific input is given."""
        if input_value is None:
            return "Please specify an input (coin/note denomination or 'dispense')"
        
        old_state = self.current_state
        result = ""
        
        if input_value == "dispense":
            result = self.dispense_drink()
        elif input_value == "cancel":
            result = self.cancel_transaction()
        else:
            try:
                amount = int(input_value)
                if amount in self.valid_denominations:
                    result = self.insert_money(amount)
                else:
                    return f"Invalid denomination: {amount}"
            except ValueError:
                return f"Invalid input: {input_value}"
        
        transition = f"Transition: {old_state} --({input_value})--> {self.current_state}"
        return f"{result}\n{transition}"
    
    def draw_simple_diagram(self):
        """Draw a simple ASCII representation of the finite automaton."""
        diagram = [
            "Simplified State Diagram:",
            "                  10              10              10",
            "  q0 ------> q10 ------> q20 ------> q30 ... and so on",
            "   |           |           |",
            "   |           |           |",
            "  50|          |60         |70",
            "   |           |           |",
            "   v           v           v",
            "  q50 <------ q60 <------ q70 ... and so on",
            "   |     disp   ^     disp  ^     disp",
            "   |            |           |",
            "   |            |           |",
            "disp|           |50         |50",
            "   |            |           |",
            "   v            |           |",
            "  q0 ---------> q50 -------> q100 ... and so on",
            "                50          50",
            "",
            f"Current state: {self.current_state}",
            f"Can dispense drink: {'Yes' if self.current_amount >= self.drink_price else 'No'}"
        ]
        return '\n'.join(diagram)

def run_simulation():
    """Run an interactive text-based simulation of the vending machine."""
    vm = VendingMachineSimulation()
    
    print("=== JKUAT Soft Drink Vending Machine Simulation ===")
    print("All drinks cost 50 KShs")
    print("Valid denominations: 10, 20, 40, 50, 100, 200, 500, 1000 KShs")
    print("\nCommands:")
    print("- insert X: Insert X KShs (e.g., 'insert 50')")
    print("- dispense: Attempt to dispense a drink")
    print("- cancel: Cancel transaction and get refund")
    print("- state: Display current state")
    print("- history: Show transaction history")
    print("- diagram: Show simple state diagram")
    print("- exit: End simulation")
    print("===========================================\n")
    
    while True:
        command = input("\nEnter command > ").strip().lower()
        
        if command == "exit":
            print("Thank you for using the JKUAT Vending Machine Simulation!")
            break
            
        elif command.startswith("insert "):
            try:
                amount = int(command.split()[1])
                print(vm.insert_money(amount))
                print(vm.display_state())
            except (ValueError, IndexError):
                print("Invalid command. Usage: insert <amount>")
                
        elif command == "dispense":
            print(vm.dispense_drink())
            print(vm.display_state())
            
        elif command == "cancel":
            print(vm.cancel_transaction())
            print(vm.display_state())
            
        elif command == "state":
            print(vm.display_state())
            
        elif command == "history":
            print(vm.display_history())
            
        elif command == "diagram":
            print(vm.draw_simple_diagram())
            
        else:
            print("Unknown command. Valid commands: insert <amount>, dispense, cancel, state, history, diagram, exit")

if __name__ == "__main__":
    run_simulation()