### Question E1

### 

### **Question E1 — Circuit Breaker Fail-Fast**

#### Scenario

Service A calls Service B.
Service B starts failing intermittently.

#### Task

Write Python code that:

* Calls Service B
* Uses a **Circuit Breaker**
* Opens the circuit after **3 failures**
* When OPEN, **does NOT call Service B**
* Returns a fallback response immediately

#### Constraints

* No retries
* No bulkhead yet
* Log CB state transitions

#### Expected behavior

* First 3 failures → Service B is called
* After CB opens → Service B is **never called**
* Logs clearly show **FAIL-FAST**

#### What interviewer checks

* Do you understand **fail-fast**
* Do you understand CB state transitions
* Do you mistakenly still call downstream when OPEN

❌ Common mistake:

> Logging fallback but still calling Service B

---
