# Testing Python Code in Pyodide/WASM

This example demonstrates how to test your Python code to ensure it runs correctly in Pyodide (WebAssembly).

## What is Pyodide?

Pyodide is a Python distribution for the browser and Node.js using WebAssembly. It allows you to run Python code in JavaScript environments, including:
- Web browsers
- Node.js (as demonstrated here)
- Other JavaScript runtimes

## Why Test in Pyodide?

Testing your code in Pyodide ensures:
1. **WASM Compatibility**: Your code works in WebAssembly environments
2. **Browser Compatibility**: If you plan to run Python in browsers
3. **Cross-Platform**: Verify your code works in JavaScript runtimes
4. **Package Compatibility**: Ensure dependencies work in Pyodide

## Setup

The setup includes:
- **Vitest**: Modern test runner for JavaScript/TypeScript
- **Pyodide 0.22.1**: Python runtime compiled to WebAssembly
- **Configuration**: Proper setup for Node.js environment

## Running Tests

```bash
# Run all tests
pnpm test

# Run specific test file
pnpm test test.test.js

# Run tests in watch mode
pnpm test --watch
```

## How It Works

### 1. Vitest Configuration (`vitest.config.js`)

The configuration:
- Sets up Node.js environment
- Configures path resolution for Pyodide
- Handles WASM and binary file types

### 2. Test Helper (`pyodide-test-helper.js`)

Provides utilities:
- `createPyodideInstance()`: Creates a configured Pyodide instance
- `runPythonCode()`: Executes Python code
- `loadPythonFile()`: Loads Python files from disk
- `canImportModule()`: Checks if a module can be imported

### 3. Basic Tests (`test.test.js`)

Demonstrates:
- Verifying WASM execution (platform check)
- Running Python code
- Importing standard library modules
- Working with Python data structures

### 4. Advanced Tests (`test-your-code.test.js`)

Shows how to:
- Load packages (like pandas)
- Test code that uses external dependencies
- Work with Pyodide's virtual filesystem
- Test your actual Python code

## Testing Your Code

### Step 1: Load Required Packages

```javascript
beforeAll(async () => {
  pyodide = await createPyodideInstance();
  
  // Load packages your code needs
  await pyodide.loadPackage("pandas");
  // Add more packages as needed
});
```

### Step 2: Load Your Python Code

You have several options:

**Option A: Load as string**
```javascript
const code = `
# Your Python code here
def my_function():
    return "Hello from WASM!"
`;
runPythonCode(pyodide, code);
```

**Option B: Load from file**
```javascript
// Copy your Python files to Pyodide's virtual filesystem first
await loadPythonFile(pyodide, "path/to/your/code.py");
```

**Option C: Use micropip to install packages**
```javascript
await pyodide.loadPackage("micropip");
runPythonCode(pyodide, `
import micropip
await micropip.install("your-package")
`);
```

### Step 3: Verify WASM Execution

Always verify your code is running in WASM:

```javascript
it("runs in WASM", () => {
  const platform = runPythonCode(pyodide, "import sys; sys.platform");
  expect(platform).toBe("emscripten"); // This confirms WASM
});
```

## Important Notes

1. **Package Availability**: Not all Python packages work in Pyodide. Check [Pyodide packages](https://pyodide.org/en/stable/usage/packages-in-pyodide.html) for available packages.

2. **File I/O**: Pyodide uses a virtual filesystem. Files must be loaded into it before use.

3. **Performance**: WASM execution may be slower than native Python. This is normal.

4. **Memory**: Pyodide runs in a sandboxed environment with memory limits.

5. **Network**: Packages are downloaded from CDN on first use, then cached locally.

## Troubleshooting

### Module Not Found Errors

If you see module resolution errors:
- Check that `indexURL` is set correctly
- Verify the Pyodide package path is correct
- Ensure WASM files are accessible

### Package Loading Issues

If packages fail to load:
- Check if the package is available in Pyodide
- Verify package version compatibility
- Check network connectivity (first load downloads from CDN)

### Path Issues

If you see `file://` prefix errors:
- Ensure `indexURL` is set to a directory path (not a URL)
- Use absolute paths when possible
- Check Vitest configuration

## Example: Testing Your Postcodes Library

A complete example is provided in `test-qlacref-postcodes.test.js` that shows how to test the actual `qlacref_postcodes` library.

### Quick Start

The test automatically:
1. Loads required packages (pandas, rsa via micropip)
2. Copies your module directory to Pyodide's filesystem
3. Sets up the Python path for imports
4. Tests the module functionality

### Manual Setup

If you want to set up your own module:

1. **Load required packages**:
```javascript
await pyodide.loadPackage("pandas");
await pyodide.loadPackage("micropip");
await pyodide.runPythonAsync(`
import micropip
await micropip.install("rsa")
`);
```

2. **Copy your module to Pyodide**:
```javascript
import { setupQlacrefPostcodes } from "./pyodide-test-helper.js";

const modulePath = "/path/to/qlacref_postcodes";
await setupQlacrefPostcodes(pyodide, modulePath, {
  insecure: true, // Skip signature verification for testing
});
```

3. **Test functionality**:
```javascript
const result = runPythonCode(pyodide, `
from qlacref_postcodes import Postcodes
import os
os.environ['QLACREF_PC_INSECURE'] = 'True'

pc = Postcodes()
len(pc.dataframe.columns)
`);
expect(result).toBe(5);
```

### Using a Built Distribution

If you prefer to test a built distribution:

1. **Build your package**:
```bash
poetry build
# or
python -m build
```

2. **Copy the built package to Pyodide**:
```javascript
// Copy the dist/ directory or wheel file to Pyodide's filesystem
// Then install it using pip in Pyodide
await pyodide.runPythonAsync(`
import micropip
await micropip.install("/path/to/your/package.whl")
`);
```

## Resources

- [Pyodide Documentation](https://pyodide.org/)
- [Pyodide Packages](https://pyodide.org/en/stable/usage/packages-in-pyodide.html)
- [Vitest Documentation](https://vitest.dev/)

## Verification

All tests verify that code is running in WASM by checking:
```python
import sys
sys.platform == "emscripten"  # True in Pyodide/WASM
```

This ensures your tests are actually running in the WebAssembly environment, not just regular Python!

