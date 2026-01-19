# Contributing to Abiqua Archive Tools

We welcome contributions that improve the accuracy and institutional reliability of our capture protocols.

### Standards for PRs
1. **Dimensional Accuracy:** Any changes to geometry must maintain 1:1 scale fidelity.
2. **Matplotlib Best Practices:** Use `Patches` (Wedge/Circle) over raw coordinate plotting to ensure clean vector exports.
3. **No Bloat:** Keep dependencies limited to standard scientific libraries (numpy/matplotlib).

### Scientific Focus
We are specifically looking for help with:
- Improved bit-pattern logic for higher-order coded targets.
- SVG path optimization for laser cutters and CNC machines.