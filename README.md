# Form-X
 A String Formatting and Structure Tool


# Form-X - String Formatting and Data Structure Tool

- **`main.py`** - Main application file (GUI)
- **`example.py`** - Sample data file containing example strings for testing
- **`requirements.txt`** - Project dependencies (uses Python standard library only)
- **`README.md`** - documentation

**Smart Input Analysis**
- **Analyze String**: Intelligent character analysis with visual status indicator
- **Status Indicator**: Red/Green dot showing analysis status (🔴 not analyzed → 🟢 ready to format)
- **Problematic Character Detection**: Warns about characters that might interfere with formatting

**Input Management**
- **Load Example**: Automatically load sample data from `example.py`
- **Clear Controls**: Separate buttons for clearing input and output areas

**Output Format Selection** *(Mutually Exclusive Radio Selection)*
- **None**: Raw output based on separator choice only
- **Python List**: Creates `['item1', 'item2', 'item3']`
- **Python Dictionary**: Creates `{'key': 'value'}` pairs with advanced key options
- **Python Tuple**: Creates `('item1', 'item2', 'item3')`

**Advanced Dictionary Options** *(Dynamically Enabled)*
*Only available when Dictionary format is selected - all options greyed out otherwise*

- **None**: Simple item count output
- **Index Keys**: Numeric indices `{'0': 'item1', '1': 'item2'}`
- **Auto-generated**: Descriptive keys `{'item_1': 'value1', 'item_2': 'value2'}`
- **First Word as Key**: `{'Hello': 'World'}`
- **User-defined Prefix**: Custom prefix with auto-numbering `{'myPrefix_1': 'value1'}`
  - *Prefix field only enabled when User-defined is selected*

- **Item Counter**: Accurate count of content words (excluding operators/brackets)
- **Copy to Clipboard**: Smart copying (excludes item count from copied text)
- **Clear Output**: Dedicated output clearing functionality
- **Error Handling**: Comprehensive error messages and user guidance
---

## 🖥️ **How to Run:**

```powershell
# Navigate to project directory
Set-Location "c:\Users\..."

# Run the application
python main.py


## 📋 **Usage Workflow:**

### **Recommended Workflow:**
1.- Input Data**: Enter your raw string or click "Load Example"
2.- Analyze**: Click "Analyze String" (status indicator turns green)
3.- Configure Options**: 
   - Select separator type (Auto-detect recommended)
   - Choose output format (List, Dictionary, Tuple, or None)
   - Configure dictionary options (if Dictionary selected)
4.- Format**: Click "Format String" to generate output
5.- Copy**: Use "Copy to Clipboard" if needed

Author: "Steelie44" 2025
