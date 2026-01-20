# Abiqua Archive - Tooling Roadmap

## Phase 1: Geometry & Scale (Completed)
- [x] Transition from Polygon to Wedge geometry for sub-pixel accuracy.
- [x] Implement 1:1 scale verification (20mm reference).
- [x] SVG and PDF export support.

## Phase 2: User Interface & Automation (Completed)
- [x] **CLI Interface:** Move configuration (Dot radius, Bit count) to command-line arguments.
- [x] **Code Quality Improvements:** Add execution guard, refactor duplicate code, extract magic numbers.
- [x] **Validation:** Add input validation and overlap detection.
- [ ] **Spiral Generator:** Automatically generate the 12.6" circular disc layout as a single printable PDF.
- [ ] **Radial Centering:** Add center-dowel alignment marks to the generated disc.

## Phase 3: Testing & Quality Assurance (Next)
- [ ] **Unit Test Suite:** Add comprehensive tests for geometric calculations, validation, and rendering.
- [ ] **Integration Tests:** Verify PDF/SVG output correctness.
- [ ] **CI/CD:** Automated testing pipeline.

## Phase 4: Forensic Integration (V3.0)
- [ ] **Metrology Logging:** Generate a CSV log alongside the PDF for manual caliper entry.
- [ ] **Blockchain "Anchor" Prep:** Automated SHA-256 hashing of generated target sets.
- [ ] **Custom Code Logic:** Implement rotationally invariant bit patterns for 12-bit and 14-bit targets.
