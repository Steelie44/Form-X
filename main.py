"""
Form-X - A String Formatting and Structure Tool

A comprehensive GUI application for converting raw strings into formatted 
Python data structures (lists, tuples, dictionaries) with customizable 
separator and key options.

Author: [Your Name]
Date: July 2025
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import json
import re


class ToolTip:
    """
    Creates a hover tooltip for any tkinter widget.
    
    Provides a clean, informative tooltip that appears when the user
    hovers over a widget and disappears when they move away.
    """
    
    def __init__(self, widget, text='widget info'):
        """
        Initialize the tooltip.
        
        Args:
            widget: The tkinter widget to attach the tooltip to
            text: The text to display in the tooltip
        """
        self.widget = widget
        self.text = text
        self.widget.bind("<Enter>", self.enter)
        self.widget.bind("<Leave>", self.leave)
        self.tipwindow = None

    def enter(self, event=None):
        """Handle mouse enter event."""
        self.showtip()

    def leave(self, event=None):
        """Handle mouse leave event."""
        self.hidetip()

    def showtip(self):
        """Display the tooltip."""
        if self.tipwindow or not self.text:
            return
            
        x, y, cx, cy = self.widget.bbox("insert")
        x = x + self.widget.winfo_rootx() + 25
        y = y + cy + self.widget.winfo_rooty() + 25
        
        self.tipwindow = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.wm_geometry("+%d+%d" % (x, y))
        
        label = tk.Label(tw, text=self.text, justify=tk.LEFT,
                        background="#ffffe0", relief=tk.SOLID, borderwidth=1,
                        font=("tahoma", "8", "normal"))
        label.pack(ipadx=1)

    def hidetip(self):
        """Hide the tooltip."""
        tw = self.tipwindow
        self.tipwindow = None
        if tw:
            tw.destroy()

class StringFormatterApp:
    """
    Main application class for the Form-X tool.
    
    A comprehensive GUI application that allows users to:
    - Input raw strings and analyze them for problematic characters
    - Choose separator options (auto-detect, space, comma, newline)
    - Select output formats (list, dictionary, tuple, or none)
    - Configure dictionary key types and custom prefixes
    - Export formatted results with visual status indicators
    """
    
    def __init__(self, root):
        """
        Initialize the application.
        
        Args:
            root: The main tkinter window
        """
        self.root = root
        self.root.title("Form-X - String Formatting Tool")
        self.root.geometry("1000x800")
        
        # Initialize application variables
        self._initialize_variables()
        
        # Set up event bindings for dynamic UI behavior
        self._setup_event_bindings()
        
        # Build the user interface
        self.setup_ui()
    
    def _initialize_variables(self):
        """Initialize all tkinter variables used by the application."""
        # Format type selection (mutually exclusive)
        self.format_type = tk.StringVar(value="none")
        
        # Separator and dictionary options
        self.separator_var = tk.StringVar(value="auto")
        self.dict_key_type = tk.StringVar(value="none")
    
    def _setup_event_bindings(self):
        """Set up trace bindings for dynamic UI behavior."""
        # Enable/disable dictionary options when format type changes
        self.format_type.trace('w', self.on_format_type_change)
        
        # Enable/disable prefix field when dictionary key type changes
        self.dict_key_type.trace('w', self.on_dict_key_type_change)
    def setup_ui(self):
        """
        Build the complete user interface.
        
        Creates all UI elements including input/output areas, option panels,
        buttons, and configures the layout with proper grid weights.
        """
        # Create main container
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Build UI sections in logical order
        self._create_input_section(main_frame)
        self._create_control_buttons(main_frame)
        self._create_option_panels(main_frame)
        self._create_output_section(main_frame)
        
        # Configure responsive layout
        self._configure_grid_weights(main_frame)
    
    def _create_input_section(self, parent):
        """Create the input text area and label."""
        input_label = ttk.Label(parent, text="Input Raw String:", 
                               font=("Arial", 12, "bold"))
        input_label.grid(row=0, column=0, columnspan=3, sticky=tk.W, pady=(0, 5))
        
        self.input_text = scrolledtext.ScrolledText(parent, height=8, width=80, 
                                                   wrap=tk.WORD)
        self.input_text.grid(row=1, column=0, columnspan=3, 
                           sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
    
    def _create_control_buttons(self, parent):
        """Create the control buttons (Load Example, Analyze, Clear)."""
        # Load example button
        load_example_btn = ttk.Button(parent, text="Load Example", 
                                     command=self.load_example)
        load_example_btn.grid(row=2, column=0, sticky=tk.W, pady=(0, 10))
        
        # Analyze button with status indicator
        analyze_frame = ttk.Frame(parent)
        analyze_frame.grid(row=2, column=1, pady=(0, 10))
        
        analyze_btn = ttk.Button(analyze_frame, text="Analyze String", 
                               command=self.analyze_string)
        analyze_btn.grid(row=0, column=0, padx=(0, 8))
        
        # Add comprehensive tooltip for analyze button
        ToolTip(analyze_btn, 
               "Check your input for problematic characters.\n\n"
               "Input examples:\n"
               "• Raw text: 'hello world test data'\n"
               "• Function names: 'fnc_example fnc_test'\n"
               "• Mixed content: 'item1 item2 item3'\n"
               "• CSV data: 'value1,value2,value3'\n"
               "• Line-separated: 'line1\\nline2\\nline3'")
        
        # Status indicator (red = not analyzed, green = analyzed)
        self.status_indicator = tk.Label(analyze_frame, text="●", 
                                       font=("Arial", 16), fg="red")
        self.status_indicator.grid(row=0, column=1)
        ToolTip(self.status_indicator, 
               "String Status:\n• Red: Not analyzed yet\n• Green: Analyzed and ready to format")
        
        # Clear input button
        clear_btn = ttk.Button(parent, text="Clear Input", command=self.clear_input)
        clear_btn.grid(row=2, column=2, sticky=tk.E, pady=(0, 10))
    
    def _create_option_panels(self, parent):
        """Create the three option panels (Separator, Format, Dictionary)."""
        # Separator options panel
        self._create_separator_panel(parent)
        
        # Output format panel
        self._create_format_panel(parent)
        
        # Dictionary options panel
        self._create_dictionary_panel(parent)
    
    def _create_separator_panel(self, parent):
        """Create the separator options panel."""
        separator_frame = ttk.LabelFrame(parent, text="Separator Options (Select One)", 
                                       padding="5")
        separator_frame.grid(row=3, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), 
                           pady=(0, 10), padx=(0, 5))
        
        # Auto-detect option
        auto_rb = ttk.Radiobutton(separator_frame, text="Auto-detect", 
                                variable=self.separator_var, value="auto")
        auto_rb.grid(row=0, column=0, sticky=tk.W)
        ToolTip(auto_rb, "Automatically detects the best separator \nbased on your input text.")
        
        # Space option
        space_rb = ttk.Radiobutton(separator_frame, text="Space", 
                                 variable=self.separator_var, value="space")
        space_rb.grid(row=1, column=0, sticky=tk.W)
        ToolTip(space_rb, "Splits by spaces and maintains word spacing. \nExample: 'word1 word2 word3'")
        
        # Comma option
        comma_rb = ttk.Radiobutton(separator_frame, text="Comma", 
                                 variable=self.separator_var, value="comma")
        comma_rb.grid(row=2, column=0, sticky=tk.W)
        ToolTip(comma_rb, "Splits by spaces and adds commas between words. \nExample: 'word1, word2, word3'")
        
        # Newline option
        newline_rb = ttk.Radiobutton(separator_frame, text="Newline", 
                                   variable=self.separator_var, value="newline")
        newline_rb.grid(row=3, column=0, sticky=tk.W)
        ToolTip(newline_rb, "Splits by spaces and puts each word on a new line. \nExample:\nword1\nword2\nword3")
    
    def _create_format_panel(self, parent):
        """Create the output format selection panel."""
        format_frame = ttk.LabelFrame(parent, text="Output Format (Select One)", 
                                    padding="5")
        format_frame.grid(row=3, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), 
                        pady=(0, 10), padx=(5, 5))
        
        # None option
        none_rb = ttk.Radiobutton(format_frame, text="None", 
                                variable=self.format_type, value="none")
        none_rb.grid(row=0, column=0, sticky=tk.W)
        ToolTip(none_rb, "No bracket formatting applied. \nOutput depends on separator choice:\nSpace: word1 word2\nComma: word1, word2\nNewline: word1\\nword2")
        
        # List option
        list_rb = ttk.Radiobutton(format_frame, text="List", 
                                variable=self.format_type, value="list")
        list_rb.grid(row=1, column=0, sticky=tk.W)
        ToolTip(list_rb, "Creates a Python list with square brackets []. \nExample: ['item1', 'item2', 'item3']")
        
        # Dictionary option
        dict_rb = ttk.Radiobutton(format_frame, text="Dictionary", 
                                variable=self.format_type, value="dict")
        dict_rb.grid(row=2, column=0, sticky=tk.W)
        ToolTip(dict_rb, "Creates a Python dictionary with curly braces {}. \nExample: {'0': 'item1', '1': 'item2'}")
        
        # Tuple option
        tuple_rb = ttk.Radiobutton(format_frame, text="Tuple", 
                                 variable=self.format_type, value="tuple")
        tuple_rb.grid(row=3, column=0, sticky=tk.W)
        ToolTip(tuple_rb, "Creates a Python tuple with parentheses (). \nExample: ('item1', 'item2', 'item3')")
    
    def _create_dictionary_panel(self, parent):
        """Create the dictionary options panel."""
        dict_frame = ttk.LabelFrame(parent, text="Dictionary Options", padding="5")
        dict_frame.grid(row=3, column=2, sticky=(tk.W, tk.E, tk.N, tk.S), 
                      pady=(0, 10), padx=(5, 0))
        
        # Dictionary options label
        self.dict_label = ttk.Label(dict_frame, text="Key Type:", state="disabled")
        self.dict_label.grid(row=0, column=0, sticky=tk.W, columnspan=2)
        
        # Create dictionary key type options
        self._create_dictionary_key_options(dict_frame)
        
        # Create user-defined prefix section
        self._create_user_defined_section(dict_frame)
    
    def _create_dictionary_key_options(self, parent):
        """Create the dictionary key type radio buttons."""
        # None option
        self.none_dict_rb = ttk.Radiobutton(parent, text="None", 
                                          variable=self.dict_key_type, 
                                          value="none", state="disabled")
        self.none_dict_rb.grid(row=1, column=0, sticky=tk.W)
        ToolTip(self.none_dict_rb, "No dictionary key formatting. \nOutputs just the item count when Dictionary format is selected.")
        
        # Index option
        self.index_rb = ttk.Radiobutton(parent, text="Index (0, 1, 2...)", 
                                      variable=self.dict_key_type, 
                                      value="index", state="disabled")
        self.index_rb.grid(row=2, column=0, sticky=tk.W)
        ToolTip(self.index_rb, "Uses numeric indices as keys. \nExample: {'0': 'item1', '1': 'item2'}")
        
        # Auto-generated option
        self.auto_rb = ttk.Radiobutton(parent, text="Auto-generated (item_1, item_2...)", 
                                     variable=self.dict_key_type, 
                                     value="auto", state="disabled")
        self.auto_rb.grid(row=3, column=0, sticky=tk.W)
        ToolTip(self.auto_rb, "Uses auto-generated descriptive keys. \nExample: {'item_1': 'value1', 'item_2': 'value2'}")
        
        # First word option
        self.first_word_rb = ttk.Radiobutton(parent, text="First word as key", 
                                           variable=self.dict_key_type, 
                                           value="first_word", state="disabled")
        self.first_word_rb.grid(row=4, column=0, sticky=tk.W)
        ToolTip(self.first_word_rb, "Uses the first word of each item as the key. \nExample: {'BIS_fnc': 'ObjectsMapper', 'Hello': 'World'}")
    
    def _create_user_defined_section(self, parent):
        """Create the user-defined prefix input section."""
        prefix_frame = ttk.Frame(parent)
        prefix_frame.grid(row=5, column=0, sticky=(tk.W, tk.E), pady=(10, 0))
        
        # User-defined radio button
        self.user_defined_rb = ttk.Radiobutton(prefix_frame, text="User-defined", 
                                             variable=self.dict_key_type, 
                                             value="user_defined", state="disabled")
        self.user_defined_rb.grid(row=0, column=0, sticky=tk.W)
        ToolTip(self.user_defined_rb, "Uses your custom word/prefix for keys. \nExample: {'myWord_1': 'value1', 'myWord_2': 'value2'}")
        
        # Prefix label and entry
        self.prefix_label = ttk.Label(prefix_frame, text="Prefix:", state="disabled")
        self.prefix_label.grid(row=0, column=1, sticky=tk.W, padx=(15, 5))
        
        self.user_prefix = ttk.Entry(prefix_frame, width=12, state="disabled")
        self.user_prefix.grid(row=0, column=2, sticky=tk.W)
        ToolTip(self.user_prefix, "Enter your custom prefix for dictionary keys. \nExample: 'data' will create keys like 'data_1', 'data_2', etc.")
    
    def _create_output_section(self, parent):
        """Create the output area and related buttons."""
        # Output label
        output_label = ttk.Label(parent, text="Formatted Output:", 
                               font=("Arial", 12, "bold"))
        output_label.grid(row=4, column=0, columnspan=3, sticky=tk.W, pady=(5, 3))
        
        # Format button
        process_btn = ttk.Button(parent, text="Format String", 
                               command=self.process_string, style="Accent.TButton")
        process_btn.grid(row=5, column=0, columnspan=3, pady=3)
        
        # Output text area
        self.output_text = scrolledtext.ScrolledText(parent, height=15, width=80)
        self.output_text.grid(row=6, column=0, columnspan=3, 
                            sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Output control buttons
        self._create_output_buttons(parent)
    
    def _create_output_buttons(self, parent):
        """Create the copy and clear output buttons."""
        button_frame = ttk.Frame(parent)
        button_frame.grid(row=7, column=2, sticky=tk.E, pady=10)
        
        copy_btn = ttk.Button(button_frame, text="Copy to Clipboard", 
                            command=self.copy_to_clipboard)
        copy_btn.grid(row=0, column=0, padx=(0, 5))
        
        clear_output_btn = ttk.Button(button_frame, text="Clear Output", 
                                    command=self.clear_output)
        clear_output_btn.grid(row=0, column=1)
    
    def _configure_grid_weights(self, main_frame):
        """Configure grid weights for responsive layout."""
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        
        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.columnconfigure(2, weight=1)
        main_frame.rowconfigure(1, weight=1)  # Input text area
        main_frame.rowconfigure(3, weight=0)  # Options panels row
        main_frame.rowconfigure(6, weight=1)  # Output text area
    # ==================== FILE AND INPUT OPERATIONS ====================
    
    def load_example(self):
        """Load example string from example.py file."""
        try:
            with open("example.py", "r") as file:
                content = file.read()
                # Extract the string from the file
                start = content.find('"""') + 3
                end = content.find('"""', start)
                
                if start > 2 and end > start:
                    example_string = content[start:end]
                    self.input_text.delete(1.0, tk.END)
                    self.input_text.insert(1.0, example_string)
                    # Reset status indicator when new content is loaded
                    self.status_indicator.config(fg="red")
                else:
                    messagebox.showerror("Error", "Could not find example string in example.py")
                    
        except FileNotFoundError:
            messagebox.showerror("Error", "example.py file not found in current directory")
        except Exception as e:
            messagebox.showerror("Error", f"Error loading file: {str(e)}")
    
    def clear_input(self):
        """Clear the input text area and reset status indicator."""
        self.input_text.delete(1.0, tk.END)
        self.status_indicator.config(fg="red")
    
    def clear_output(self):
        """Clear the output text area."""
        self.output_text.delete(1.0, tk.END)
    
    def copy_to_clipboard(self):
        """Copy formatted output to clipboard (excluding item count)."""
        output = self.output_text.get(1.0, tk.END).strip()
        
        if not output:
            messagebox.showwarning("Warning", "No output to copy")
            return
            
        # Remove the item count line if it exists
        lines = output.split('\n')
        if lines and lines[0].startswith("Item count:"):
            # Skip the first line (item count) and empty line
            filtered_lines = [line for line in lines[2:] if line.strip()]
            output_to_copy = '\n'.join(filtered_lines)
        else:
            output_to_copy = output
        
        self.root.clipboard_clear()
        self.root.clipboard_append(output_to_copy)
        messagebox.showinfo("Success", "Output copied to clipboard!")
    
    def analyze_string(self):
        """Analyze input string for potentially problematic characters."""
        input_string = self.input_text.get(1.0, tk.END).strip()
        
        if not input_string:
            messagebox.showwarning("Warning", "Please enter a string to analyze")
            return
        
        # Define characters that might interfere with formatting
        problematic_chars = [',', '.', '/', ';', "'", '"', '[', ']', '{', '}', '(', ')']
        found_chars = [char for char in problematic_chars if char in input_string]
        
        if found_chars:
            char_list = ', '.join([f"'{char}'" for char in found_chars])
            message = (f"Warning: Found potentially problematic characters in your input:\n"
                      f"{char_list}\n\n"
                      f"These characters might interfere with the app's functions. "
                      f"Consider removing them or using the custom separator option.")
            messagebox.showwarning("String Analysis", message)
        else:
            messagebox.showinfo("String Analysis", 
                              "No problematic characters found. Your string should work well with all formatting options!")
        
        # Change status indicator to green after analysis
        self.status_indicator.config(fg="green")
    # ==================== STRING PROCESSING UTILITIES ====================
    
    def get_separator(self, input_string=None):
        """Get the appropriate separator based on user selection."""
        sep_type = self.separator_var.get()
        
        if sep_type == "auto":
            return self.auto_detect_separator(input_string)
        elif sep_type == "space":
            return " "
        elif sep_type == "comma":
            return ","
        elif sep_type == "newline":
            return "\n"
        else:
            return " "  # Default fallback
    
    def auto_detect_separator(self, input_string):
        """Automatically detect the best separator for the input string."""
        if not input_string:
            return " "
        
        # Count different types of separators
        comma_count = input_string.count(",")
        newline_count = input_string.count("\n")
        space_count = len([word for word in input_string.split() if word.strip()]) - 1
        
        # Choose the most likely separator based on frequency
        if comma_count > 0 and comma_count >= newline_count:
            return ","
        elif newline_count > 0:
            return "\n"
        else:
            return " "  # Default to space
    
    def clean_and_split_string(self, input_string):
        """Clean input string and split it into items based on separator type."""
        # Remove /n markers and normalize whitespace
        cleaned = re.sub(r'/n', ' ', input_string)
        cleaned = re.sub(r'\s+', ' ', cleaned)
        cleaned = cleaned.strip()
        
        sep_type = self.separator_var.get()
        
        if sep_type == "auto":
            # Auto-detect separator and split normally
            separator = self.auto_detect_separator(cleaned)
            items = [item.strip() for item in cleaned.split(separator) if item.strip()]
        elif sep_type in ["space", "comma", "newline"]:
            # For all manual separator types, split by spaces to get individual words
            items = [item.strip() for item in cleaned.split() if item.strip()]
        else:
            # Default fallback
            items = [item.strip() for item in cleaned.split() if item.strip()]
        
        return items
    
    def count_actual_content(self, items):
        """Count only words, letters, and numbers in items, excluding operators."""
        content_count = 0
        
        for item in items:
            # Remove all non-alphanumeric characters and count remaining words
            clean_item = re.sub(r'[^a-zA-Z0-9\s]', '', item)
            words = [word for word in clean_item.split() if word.strip()]
            content_count += len(words)
        
        return content_count
    # ==================== FORMATTING METHODS ====================
    
    def format_items_as_string(self, items):
        """Format items as quoted strings for use in data structures."""
        return ', '.join(f'"{item}"' for item in items)
    
    def format_as_list(self, items):
        """Format items as a Python list."""
        formatted_items = self.format_items_as_string(items)
        return f"[{formatted_items}]"
    
    def format_as_tuple(self, items):
        """Format items as a Python tuple."""
        formatted_items = self.format_items_as_string(items)
        return f"({formatted_items})"
    
    def format_as_dict(self, items):
        """Format items as a dictionary based on selected key type."""
        key_type = self.dict_key_type.get()
        
        if key_type == "none":
            # No dictionary formatting, return None to use separator formatting
            return None
        elif key_type == "index":
            dict_entries = [f'"{i}": "{item}"' for i, item in enumerate(items)]
        elif key_type == "auto":
            dict_entries = [f'"item_{i+1}": "{item}"' for i, item in enumerate(items)]
        elif key_type == "user_defined":
            user_prefix = self.user_prefix.get().strip()
            if not user_prefix:
                messagebox.showwarning("Warning", 
                                     "Please enter a prefix for user-defined keys or select a different option")
                return None
            dict_entries = [f'"{user_prefix}_{i+1}": "{item}"' for i, item in enumerate(items)]
        elif key_type == "first_word":
            dict_entries = []
            for item in items:
                words = item.split()
                if words:
                    key = words[0]
                    value = " ".join(words[1:]) if len(words) > 1 else item
                    dict_entries.append(f'"{key}": "{value}"')
                else:
                    dict_entries.append(f'"{item}": "{item}"')
        else:
            return None
        
        # Format with proper curly braces
        dict_content = ', '.join(dict_entries)
        return f"{{{dict_content}}}"
    
    def format_with_separator_style(self, items, format_type):
        """Format items based on the selected separator style."""
        sep_type = self.separator_var.get()
        
        if sep_type == "comma" and format_type == "none":
            return ', '.join(items)
        elif sep_type == "newline" and format_type == "none":
            return '\n'.join(items)
        elif sep_type == "space" and format_type == "none":
            return ' '.join(items)
        else:
            # For other format types or auto-detect, return None to use standard formatting
            return None
    # ==================== MAIN PROCESSING METHOD ====================
    
    def process_string(self):
        """Main method to process input string and generate formatted output."""
        input_string = self.input_text.get(1.0, tk.END).strip()
        
        if not input_string:
            messagebox.showwarning("Warning", "Please enter a string to format")
            return
        
        format_type = self.format_type.get()
        
        try:
            # Clean and split the string
            items = self.clean_and_split_string(input_string)
            
            if not items:
                messagebox.showwarning("Warning", "No items found in the input string")
                return
            
            # Generate output with item count
            content_count = self.count_actual_content(items)
            output = f"Item count: {content_count}\n\n"
            
            # Check for special separator formatting first
            special_format = self.format_with_separator_style(items, format_type)
            
            if special_format is not None:
                output += special_format
            else:
                # Format based on selected type (standard formatting)
                if format_type == "list":
                    output += self.format_as_list(items)
                elif format_type == "dict":
                    dict_result = self.format_as_dict(items)
                    if dict_result is not None:
                        output += dict_result
                    else:
                        # Dictionary with "none" option - use separator formatting
                        separator_format = self.format_with_separator_style(items, "none")
                        if separator_format is not None:
                            output += separator_format
                elif format_type == "tuple":
                    output += self.format_as_tuple(items)
                elif format_type == "none":
                    # Just show the item count, no additional formatting
                    pass
            
            # Display the formatted output
            self.output_text.delete(1.0, tk.END)
            self.output_text.insert(1.0, output)
            
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while processing: {str(e)}")
    # ==================== EVENT HANDLERS ====================
    
    def on_format_type_change(self, *args):
        """Handle format type changes to enable/disable dictionary options."""
        is_dict_selected = self.format_type.get() == "dict"
        
        # Enable/disable all dictionary option radio buttons
        state = "normal" if is_dict_selected else "disabled"
        
        # Update all dictionary-related widgets
        self.dict_label.config(state=state)
        self.none_dict_rb.config(state=state)
        self.index_rb.config(state=state)
        self.auto_rb.config(state=state)
        self.first_word_rb.config(state=state)
        self.user_defined_rb.config(state=state)
        self.prefix_label.config(state=state)
        
        # Handle prefix entry field separately
        if is_dict_selected and self.dict_key_type.get() == "user_defined":
            self.user_prefix.config(state="normal")
        else:
            self.user_prefix.config(state="disabled")
            self.user_prefix.delete(0, tk.END)
        
        # Reset dictionary key type when dictionary is not selected
        if not is_dict_selected:
            self.dict_key_type.set("none")

    def on_dict_key_type_change(self, *args):
        """Handle dictionary key type changes to enable/disable prefix field."""
        # Only enable prefix field if dictionary format is selected AND user-defined key type is selected
        is_dict_selected = self.format_type.get() == "dict"
        is_user_defined = self.dict_key_type.get() == "user_defined"
        
        if is_dict_selected and is_user_defined:
            self.user_prefix.config(state="normal")
        else:
            self.user_prefix.config(state="disabled")
            self.user_prefix.delete(0, tk.END)

# ==================== APPLICATION ENTRY POINT ====================

def main():
    """
    Initialize and run the Form-X application.
    
    Creates the main tkinter window and starts the application event loop.
    """
    root = tk.Tk()
    app = StringFormatterApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
