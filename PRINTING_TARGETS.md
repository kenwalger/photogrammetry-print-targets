# Photogrammetric Target Printing Guidance
## Inkjet vs Laser, Tolerances, and Sanity Checks

### Purpose
This document describes acceptable printing methods and verification procedures
for photogrammetric coded targets used in dimensional capture workflows.

The goal is **repeatability and verification**, not absolute perfection.

---

## Printer Technology Comparison

### Inkjet Printers
**Pros**
- Widely available
- High contrast
- Excellent circular centroid detection
- Works well on matte photo or presentation paper

**Cons**
- Ink spread (dot gain)
- Paper expansion during drying
- Slight dimensional variability

**Expected Tolerance**
- ±0.2–0.3 mm on a 6 mm feature

**Recommendation**
Inkjet printing is fully acceptable for photogrammetry when used with a physical
scale reference or calibration feature.

---

### Laser Printers
**Pros**
- Sharper edges
- Lower dot gain
- Better dimensional repeatability

**Cons**
- Some toners introduce edge halos
- Glossy fusing can affect reflectivity
- Not always available

**Expected Tolerance**
- ±0.1–0.15 mm on a 6 mm feature

**Recommendation**
Laser printing is preferred when available, but not required.

---

## Calibration Feature (Required Verification)

Each printed sheet includes a **20.00 mm center-to-center calibration reference**.

### Verification Procedure
1. Print at **100% / Actual Size**
2. Disable:
   - Fit-to-page
   - Borderless expansion
   - Automatic scaling
3. Allow ink to dry for at least 10 minutes
4. Measure center-to-center distance with calipers
5. Record observed distance

### Acceptance Criteria
- Inkjet: 19.7–20.3 mm
- Laser: 19.85–20.15 mm

Observed deviation does **not** invalidate targets.
It documents printer behavior.

---

## Photogrammetry Sanity Check

Photogrammetry software:
- Detects **centroids**, not edges
- Uses **relative geometry**
- Is insensitive to small dot diameter variation

Therefore:
- A 5.8 mm dot behaves the same as a 6.2 mm dot
- Calibration references and scale bars define absolute size

This workflow meets professional documentation standards when paired with:
- Physical scale references
- Consistent printing procedures
- Logged verification results

---

## Summary

✔ Inkjet printing is acceptable  
✔ Laser printing is preferred when available  
✔ Calibration references provide traceability  
✔ Verification is more important than correction  

This approach prioritizes repeatability, transparency, and institutional trust.
