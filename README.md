# The Fucking Comment Nuke
A simple multi‑language comment remover.

---

## 🚀 Overview
**The Comment Nuke** is a Python script designed to recursively remove comments from source files in multiple programming languages. It supports both **single-file** and **full-directory** processing, making it easy to clean up large codebases fast.

---

## 🧠 Supported Languages
The tool can remove comments from:

- **Java**
- **C++**
- **C#**
- **Python**
- **JavaScript**
- **Assembly**
- **All supported languages at once** (multi‑mode)

Each language has its own tailored comment‑removal function for maximum accuracy.

---

## 🛠️ Usage

### **Basic Syntax**
```bash
python easyfuckingpeasy.py /path/to/project [language] [mode]
```

---

## ⚙️ Arguments

| Argument | Description |
|---------|-------------|
| **/path/to/project** | Path to a directory or file (depending on mode). |
| **language** | Language to clean. Defaults to `java`. Options: `java`, `cpp`, `cs`, `python`, `javascript`, `assembly`, `all`. |
| **mode** | `dir` (default) for directories, or `file` for single-file mode. |

---

## 📌 Examples

### **Clean all Java files in a directory**
```bash
python easyfuckingpeasy.py ./src java
```

### **Clean a single Python file**
```bash
python easyfuckingpeasy.py script.py python file
```

### **Clean ALL supported file types recursively**
```bash
python easyfuckingpeasy.py ./project all
```

---

## ⚠️ Notes
- In `all` mode, the comment remover is chosen automatically based on file extension.  
- `file` mode is **not allowed** when using `all`.  
- The script modifies files **in place** — version control is strongly recommended.

---

Happy fucking. 🔥