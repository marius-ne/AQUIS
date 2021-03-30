# STA's PocketQube
### Python repository

Development repository for our PocketQube-project.

## How to use

Put contents of lib-folder into lib-folder of E:\CIRCUITPYTHON drive on your board. 
Put code.py into root folder.

## Architecture

```mermaid

flowchart LR

Node1[Define Thresholds] --> Node2[Enter initial state]
Node2 --> Node3{Main Loop}

style Node1 stroke-width:4px
style Node2 stroke-width:4px
style Node3 color:#000

Node10(States & Thresholds) -.-> Node5
Node11(External commands) -.-> Node6

style Node10 stroke-width:4px, fill:#ffd
style Node11 stroke-width:4px, fill:#ffd

Node6[Execute State functions] --> Node3
Node3 --> Node4[Read Sensors]

subgraph "State Machine"
  
  Node4 --> Node5[Decide next State] 
  style Node5 fill:#bbf
  style Node4 fill:#bbf
  style Node6 fill:#bbf
  Node5 --> Node6
  
end

```
## States

#### Idle

> Threshold to Enter

No others met.

> Functions
* Log sensors & state
* Reading all sensors

#### LowPower

> Threshold to enter

Certain voltage reached.

> Functions
* Log state
* Read only critical sensors

#### Comms

> Threshold to enter

Antenna having received signal.

> Functions
* Receive commands
* Log sensors & state
* Transmit log






## TODO

> Encoding for Comms

> Command Parsing

> ~~API for analogueIn devices~~

> ~~State Machine & Power modes~~

> Non intrusive Exception handling that ensures stable runtime

> Globally updated log to downlink, log == stdout?
