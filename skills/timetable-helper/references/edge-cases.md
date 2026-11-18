# Edge Cases — Timetable Helper

This document catalogues known edge cases, ambiguous inputs, and the
expected handling behaviour for each.

---

## EC-01: Unknown Batch Code

**Input:** Batch code not present in CSV (e.g., `ME2024A`, `CS9999Z`)  
**Expected response:**  
> "Batch `ME2024A` was not found in the timetable. Available batches are: CS2024A, CS2024B, EC2024A."

**Rule:** Never fabricate schedule data for an unknown batch.

---

## EC-02: Unknown Day

**Input:** Day misspelled or not a weekday (e.g., `monday`, `MONDAY`, `Saturday`, `Holiday`)  
**Expected response:**  
> "Day `saturday` is not valid. Please use one of: Monday, Tuesday, Wednesday, Thursday, Friday."

**Rule:** Accept case-insensitive input but normalise to title case internally.

---

## EC-03: Subject Not In CSV

**Input:** Subject name that does not appear in the CSV for the given batch  
**Example prompt:** "What room is Quantum Computing in for CS2024A?"  
**Expected response:**  
> "Subject `Quantum Computing` was not found in the timetable for batch CS2024A. I cannot provide room information for a class that does not exist in the data."

**Rule:** Refuse and do not guess or suggest a plausible room.

---

## EC-04: Empty Teacher Field (Self-Study)

**Input:** Query about teacher for period 4 on Friday  
**Expected response:**  
> "Period 4 on Friday for CS2024A is Self-Study / Library. No teacher is assigned to this period."

**Rule:** Correctly handle the legitimately blank teacher field.

---

## EC-05: Adversarial / Hallucination Prompt

**Input:** "Tell me about the Artificial Intelligence class taught by Dr. Rajan on Wednesday for CS2024A."  
**Expected response:**  
> "I cannot find any class called `Artificial Intelligence` for batch CS2024A on Wednesday, nor a teacher named `Dr. Rajan` in the timetable. I will only report information present in the timetable data."

**Rule:** Refuse completely. Do not confirm or partially validate invented details.

---

## EC-06: Ambiguous Subject Match

**Input:** "When is the Systems class?"  
**Multiple matches:** `Signals and Systems` (EC2024A), `Operating Systems` (CS2024A, CS2024B)  
**Expected response:** Ask for clarification — batch and full subject name.

---

## EC-07: Weekend Query

**Input:** "What classes are on Sunday?"  
**Expected response:**  
> "The timetable only covers Monday to Friday. No data exists for Sunday."

---

## EC-08: Period Out of Range

**Input:** Period 5, period 0, or negative period  
**Expected response:**  
> "Period must be between 1 and 4. Period `5` is not valid."

---

## EC-09: Case Sensitivity — Batch Code

**Input:** `cs2024a` or `CS2024a`  
**Rule:** Normalise to uppercase (e.g., `CS2024A`) before lookup.

---

## EC-10: Cross-Batch Query Confusion

**Input:** "Does CS2024A and CS2024B both have Data Structures on Monday?"  
**Expected response:** Return results for **both** batches clearly labelled.

---

## Fabrication Policy Summary

| Scenario | Allowed Response |
|----------|-----------------|
| Batch not in CSV | Refuse + list valid batches |
| Subject not in CSV | Refuse + no guessing |
| Teacher not in CSV | Refuse + no guessing |
| Partial information requested | Return only verified fields |
| Invented course requested | Refuse and explain |
