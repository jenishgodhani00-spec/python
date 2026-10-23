# Technical Specification and Compliance Documentation for the Python Transaction-Processing and Auditing System (PTPAS)

---

## 1. Architectural Summary

The **Python Transaction-Processing and Auditing System (PTPAS)** is a minimalist, enterprise-ready monetary ledger and compliance engine built entirely using **Python 3.x**. The system operates under a strict zero-dependency constraint, utilizing only the native `random` and `datetime` packages from the standard library. 

PTPAS serves as a reference implementation for critical software engineering principles, low-level binary data stream management, manual lexical analysis, deterministic state machines, lexical closures, and object-oriented runtime polymorphism.

---

## 2. Core Architecture and Class Hierarchies

### 2.1 Workflow Diagram

```
+=============================================================================+
|                      PTPAS SYSTEM RUNTIME FLOW                              |
+=============================================================================+
|                                                                             |
|  [USER CLIENT / CONSOLE]                                                    |
|         │                                                                   |
|         ▼                                                                   |
|  +───────────────────────────────────────────────────────────────────────+  |
|  | SUBSYSTEM 1: CORE STATE LOGIC                                         |  |
|  | - Double-layered while-loop polling loop                              |  |
|  | - Mathematical compounding & levy engine via elementary operators     |  |
|  | - Early-termination guard via short-circuit evaluations               |  |
|  +──────────────────────────────────┬────────────────────────────────────+  |
|                                     │                                       |
|                                     ▼                                       |
|  +───────────────────────────────────────────────────────────────────────+  |
|  | SUBSYSTEM 2: STREAM PARSING & LEXICAL CLOSURES                        |  |
|  | - Manual Lexer using cursor indices and boolean boundary flags        |  |
|  |   (Zero str.split or str.replace usage; isolates literal quotes)      |  |
|  | - Lexical Audit Boundary containing nonlocal accumulators             |  |
|  | - Positional verification via scoped lambdas with default variables   |  |
|  +──────────────────────────────────┬────────────────────────────────────+  |
|                                     │                                       |
|                                     ▼                                       |
|  +───────────────────────────────────────────────────────────────────────+  |
|  | SUBSYSTEM 3: IN-PLACE QUEUE OPTIMIZATION                              |  |
|  | - Single-expression dictionary comprehension mapping catalog targets  |  |
|  | - High-performance queue scrubbing modifying the identical list ID    |  |
|  |   * Re-evaluating tuples to lists                                     |  |
|  |   * Eliminating even records via set differences                      |  |
|  |   * Reverse ordering arrays                                           |  |
|  |   * Primitive tracking via immediate index elimination                |  |
|  +──────────────────────────────────┬────────────────────────────────────+  |
|                                     │                                       |
|         ┌───────────────────────────┴───────────────────────────┐           |
|         ▼                                                       ▼           |
|  +─────────────────────────────────────+ +───────────────────────────────+  |
|  | SUBSYSTEM 4: PERSISTENT STORAGE     | | SUBSYSTEM 5: POLYMORPHIC OBJECTS|  |
|  | - Random-access in-place updates    | | - Encapsulated Ledger Abstract  |  |
|  |   using seek/tell commands          | |   Base Class (__balance hidden) |  |
|  | - Bidirectional sliding window shifts | | - ThriftAccount (Floor limits)  |  |
|  | - Target file resizing via truncate() | | - TransactionAccount (Overdraft) |  |
|  | - Individual record isolation hooks  | | - DeferredAccount (Extra levies)  |  |
|  |   * Valid -> master_log.txt         | | - Multi-account unified batch   |  |
|  |   * Faulty -> parsing_errors.log    | |   settlements without built-in  |  |
|  |   * Final block metric summaries    | |   min/max/sum calls             |  |
|  +─────────────────────────────────────+ +───────────────────────────────+  |
|                                                                             |
+=============================================================================+
```

### 2.2 Class Inheritance Model

```
                       +──────────────────────────+
                       |      Exception           |
                       +────────────┬─────────────+
                                    │
                                    ▼
                       +──────────────────────────+
                       |     PTPASRuntimeFault     |
                       +────────────┬─────────────+
                                    │
        ┌───────────────────────────┼───────────────────────────┐
        ▼                           ▼                           ▼
+───────────────────────+ +───────────────────+ +────────────────────────────+
| MalformedRecordFault  | | BoundaryViolation   | | DeficientCapitalViolation  |
+───────────────────────+ +───────────────────+ +────────────────────────────+


                       +─────────────────────────────────────────+
                       |             LedgerAccount               |
                       +─────────────────────────────────────────+
                       | + aggregate_account_count: int          |
                       | # _account_identifier: str              |
                       | - __balance: float                      |
                       +─────────────────────────────────────────+
                       | + __init__(account_id, initial_balance) |
                       | + get_account_identifier() -> str       |
                       | + read_balance() -> float               |
                       | + write_balance(new_balance: float)     |
                       | + apply_settlement(amount) [Abstract]   |
                       +────────────────────┬────────────────────+
                                            │
        ┌───────────────────────────────────┼───────────────────────────────────┐
        │                                   │                                   │
        ▼                                   ▼                                   ▼
+───────────────────────────+ +───────────────────────────+ +───────────────────────────+
|       ThriftAccount       | |    TransactionAccount     | |      DeferredAccount      |
+───────────────────────────+ +───────────────────────────+ +───────────────────────────+
| + MINIMUM_FLOOR = 1000.0  | | - __credit_ceiling: float | | + SURCHARGE_PERCENT = 0.02|
+───────────────────────────+ +───────────────────────────+ +───────────────────────────+
| + __init__(id, bal)       | | + __init__(id, bal, ceil) | | + __init__(id, limit)     |
|   calls super().__init__()| |   calls super().__init__()| |   calls super().__init__()|
| + apply_settlement(amt)   | | + read_credit_ceiling()   | | + apply_settlement(amt)   |
|   Blocks if balance falls | | + write_credit_ceiling()  | |   Applies flat surcharge, |
|   below floor limits      | | + apply_settlement(amt)   | |   reduces allocation space|
+───────────────────────────+ +───────────────────────────+ +───────────────────────────+
```

---

## 3. Runtime Scope and Variable Isolation Matrix

The table below breaks down variable constraints, variable lookup rules, and memory lifecycle mechanics used within the ecosystem.

| Target Variable | Declared Scope | Scope Management Logic | Runtime Visibility | Details and Purpose |
| :--- | :--- | :--- | :--- | :--- |
| `LedgerAccount.aggregate_account_count` | Class Block | Class-level modification via explicitly bound names | Accessible via Class or Instance references | Tallies the global number of accounts generated during the process lifecycle; tracking occurs inside the parent constructor. |
| `LedgerAccount._account_identifier` | Instance Block | Single underscore protection notation | Children classes and related package methods | Maintains standard identification attributes; read-only access provided by a dedicated method. |
| `LedgerAccount.__balance` | Instance Block | Double underscore name mangling rules (`_LedgerAccount__balance`) | Internal class routines only | Protects asset balances from external interference. Direct modification causes an `AttributeError`. |
| `TransactionAccount.__credit_ceiling` | Instance Block | Double underscore name mangling rules | Subclass internal methods only | Imposes constraints on maximum permitted negative asset positions; accessed via getters/setters. |
| `processed_record_tally` | Parent Context (`build_audit_boundary`) | Controlled through `nonlocal processed_record_tally` | Nested inner procedure (`evaluate_row`) | Tracks row iterations across asynchronous calls without utilizing global data sets. |
| `compliant_record_tally` | Parent Context (`build_audit_boundary`) | Controlled through `nonlocal compliant_record_tally` | Nested inner procedure (`evaluate_row`) | Maintains a dynamic tally of items matching or exceeding parameters; isolated to the individual execution instance. |
| `k` (Index Reference) | Loop Scope (`generate_index_filters`) | Functional default binding properties (`k=k`) | Anonymous function runtime environment | Fixes the current loop counter index to prevent the late-binding behaviors common in nested scopes. |
| `system_running` | Function Scope (`launch_terminal_loop`) | Top-level execution control parameter | Outer sequence logic | Dictates the overall lifespan of the interface execution loop. |
| `session_active` | Function Scope (`launch_terminal_loop`) | Second-tier execution control parameter | Inner sequence logic | Controls individual command scopes, trapping minor unexpected input exceptions to maintain stability. |
| `data_list` | Parameter Scope (`sanitize_transaction_pipeline`) | Direct object structural updates | Shares original object space via `id()` | Alters the incoming array arguments directly in the host application's memory pool to optimize performance. |
| `total_processed` | Function Scope (`parse_and_verify_ledger_file`) | Standard integer summation increments | Internal scope and trailing `finally` tracking | Tracks clean row items manually without using the native `sum()` function. |
| `total_rejected` | Function Scope (`parse_and_verify_ledger_file`) | Standard integer summation increments | Internal scope and trailing `finally` tracking | Track corrupted row data metrics manually across input pipelines. |

---

## 4. System Specification Matrix and Compliance Mapping

This registry correlates every functional requirement (FR) and non-functional requirement (NFR) to its matching design footprint.

| ID | Operational Area | Specific Criteria Description | Execution Strategy Summary |
| :--- | :--- | :--- | :--- |
| **FR-1.1** | Engine Interface | Dual-nested `while` loop interface layout; isolates faults; only shuts down via explicit close calls. | Handled via nested control states inside the interactive terminal routines. |
| **FR-1.2** | Interest Calculator | Multi-period interest compounding logic built solely using basic mathematical operators. | Executed inside raw math loops; relies purely on basic operators without external modules. |
| **FR-1.3** | Safety Guard | Monitoring loop that aborts processing via short-circuit logical chains when thresholds are breached. | Evaluated immediately within row iterations to block downstream side effects. |
| **FR-2.1** | Document Lexer | Token isolation mechanism based on explicit indices and boundary tracking without using `str.split`. | Built using a stateful character scan matrix that parses tokens individually. |
| **FR-2.2** | String Boundaries | Content inside quotes keeps structural delimiters intact; handles escaped quotes inside strings. | Tracked using lookahead checks inside the character scanning routine. |
| **FR-2.3** | Fragment Processing | Properly processes adjacent separators and trailing data rows without skipping records. | Handled by adding empty data fields during character state switches. |
| **FR-2.4** | Closure Mechanics | Generates functions that track metrics across decoupled scopes via `nonlocal` keywords. | Handled by capturing tracking counters within separate execution scopes. |
| **FR-2.5** | Lambda Optimization | Array filters generated via iteration steps using default assignment logic to isolate indices. | Managed using default index bindings to keep scope variables distinct. |
| **FR-3.1** | Catalog Management | Generates inverted records via a single dictionary comprehension structure. | Organized into structural lookup tables through compressed nested definitions. |
| **FR-3.2** | Array Sanitation | Sanitizes diverse data objects while preserving the original memory footprint. | Checked by verifying memory allocation patterns before and after manipulation routines. |
| **FR-3.3** | Variant Cleansing | Transforms nested values into standard structures and removes specific IDs via set transformations. | Applied through explicit item type conversions and set operations. |
| **FR-3.4** | Element Sorting | Sorts embedded datasets and removes redundant records without allocating new collections. | Managed via index manipulation and deletion operations on the array. |
| **FR-4.1** | Error Hierarchy | Object tree built from a common root error class to manage distinct runtime errors. | Extends the base Exception structure with specific subclasses. |
| **FR-4.2** | Database Updates | Performs data modifications in `r+` mode using file seek operations and sizing adjustments. | Regulated via bidirectional byte shifting operations to manage file space changes. |
| **FR-4.3** | Data Validation | Identifies invalid rows based on incorrect layouts, bad types, or unrecognized attributes. | Handled by checking parameters explicitly before committing entries to disk. |
| **FR-4.4** | Logging Subsystem | Wraps database logic in try-except-else-finally blocks; logs items to specific files; writes run summaries. | Handled using standard exception routing to log errors and compile execution statistics. |
| **FR-5.1** | Object Properties | Controls variables using name mangling, inheritance strategies, and instance tracking trackers. | Implemented via internal class properties and tracking attributes. |
| **FR-5.2** | Account Types | Implements distinct logic for varied accounts while routing initializations through parent objects. | Managed by implementing custom verification rules across subclasses. |
| **FR-5.3** | Batch Operations | Processes multi-type sets inside independent error containers without using `sum` or `min`. | Evaluated using manual tracking variables inside collection loops. |
| **NFR-1** | Core Architecture | Runs on pure Python 3.x using only basic standard library tools. | Enforced by restricting imports to the core `random` and `datetime` packages. |
| **NFR-2** | String Control | Zero instances of built-in string separation methods in raw data parsing modules. | Enforced by relying strictly on custom index tracking routines. |
| **NFR-3** | Aggregation Logic | Zero usage of standard math minimization, maximization, or summation utilities. | Handled by computing aggregation metrics via manual loop processes. |
| **NFR-4** | File Security | Validates that resources are released correctly via standard allocation blocks. | Enforced by using context managers for file system read and write operations. |
| **NFR-5** | Project Layout | Code structures are separated into explicit operational areas backed by descriptive reference blocks. | Maintained by dividing modules cleanly and using standard inline documentation. |

---

## 5. Technical Implementation Details

### 5.1 In-Place Byte Alignment Routines

The data access engine writes record revisions into `ledger_store.db` without loading the full file structure into memory or using heavy rewrite operations. 

When a dataset variation occurs at an established location \(O\):
1. **Size Deviation Analysis**:
   \[\Delta = \text{Length}(R_{\text{revised}}) - \text{Length}(R_{\text{historical}})\]
2. **Symmetric Adjustments (\(\Delta = 0\))**:
   The execution pointer targets location \(O\) directly and overwrites the existing segment. Surrounding text blocks remain untouched.
3. **Contraction Operations (\(\Delta < 0\))**:
   - The updated line segment is committed directly at position \(O\).
   - The downstream bytes starting from \(O + \text{Length}(R_{\text{historical}})\) are shifted toward the front of the file by \(\vert{}\Delta\vert{}\) bytes using 64-byte processing windows.
   - Because the target write position trails the current read window, downstream data remains protected during operations.
   - The engine calls `f.truncate(new_end_of_file)` to release unused trailing space on disk.
4. **Expansion Operations (\(\Delta > 0\))**:
   - The remaining file content is shifted toward the back of the file by \(\Delta\) bytes. This shift begins at the end of the file and moves backward toward the \(O + \text{Length}(R_{\text{historical}})\) boundary in 64-byte blocks.
   - This backward migration path prevents data overwrites during expansion phases.
   - The updated line segment is written into the newly allocated space at position \(O\).
   - Surrounding data lines remain structurally identical throughout the operation.

### 5.2 Deterministic Parsing Logic

The text analysis tool evaluates unformatted logs using an index-driven state model:
- **States**: `OUTSIDE_STRING`, `INSIDE_STRING`.
- **State Transition Rules**:
  - `OUTSIDE_STRING` + `quote_char` \(\rightarrow\) Change state to `INSIDE_STRING`.
  - `OUTSIDE_STRING` + `delimiter` \(\rightarrow\) Export the current string buffer and clear internal states.
  - `INSIDE_STRING` + `quote_char`:
    - When lookahead confirms `line[i+1] == quote_char` \(\rightarrow\) Append one literal quote character and advance the cursor index by two positions to process the escaped sequence (`""`).
    - Otherwise \(\rightarrow\) Revert state to `OUTSIDE_STRING`.
  - Delimiters found while inside the `INSIDE_STRING` state are treated as literal text data and added directly to the active collection buffer.
  - Line termination fragments are stripped using manual slice indexing rather than relying on automatic cleanup methods.

### 5.3 Array Element Deduplication

The system deduplicates primitive types within the `sanitize_transaction_pipeline` method without generating separate temporary tracker lists or dictionary indexes:
- An outer tracking index `i` steps forward from \(0\) through the length of the list.
- For each item at index `i`, an inner index `j` checks previously validated items from position \(0\) up to \(i-1\).
- Strict value and type checks (`type(prev) is type(curr) and prev == curr`) prevent matching different data types that share equivalent values (such as `1` and `True`).
- If the inner loop identifies a duplicate item, the system drops the element using a `del` operation. The outer index `i` stays in place to evaluate the next incoming data record shifted into that position.

---

## 6. Operation and Verification Instructions

### 6.1 Executing the Automated Tests

To launch the built-in validation script across all functional areas, run:

```bash
python main.py
```

During initialization, the application verifies the following operations:
1. **Module 1**: Validates compounding calculations and safety checks without external library support.
2. **Module 2**: Parses complex logs containing nested escape characters, validates scope boundaries, and runs index filtering logic.
3. **Module 3**: Generates single-expression lookup maps and executes in-place array cleanup tracking.
4. **Module 4**: Modifies file sizes dynamically in `r+` mode, handles unexpected records, and saves processing histories.
5. **Module 5**: Enforces encapsulation through variable name mangling and runs batch operations across diverse account classes.

### 6.2 Service Terminal Interface

When the automated diagnostic suite finishes its pass, the interactive terminal interface starts automatically. The console supports the following commands:
- `help`: Opens the system operations menu.
- `list`: Displays all accounts currently held in memory.
- `create <id> <type> <balance>`: Adds a new account instance (`THRIFT`, `TRANSACTION`, or `DEFERRED`).
- `deposit <id> <amount>`: Credits funds to an active account.
- `withdraw <id> <amount>`: Debits funds from an active account.
- `interest <principal> <rate> <periods>`: Simulates multi-period compound interest returns.
- `guard`: Exercises early-termination short-circuit rules.
- `update <id> <type> <balance>`: Modifies saved file records using random-access methods.
- `audit`: Evaluates the account file registry and exports the results to system logs.
- `settle <amount>`: Runs polymorphic batch updates across all loaded account instances.
- `exit`: Shuts down the terminal framework safely.
