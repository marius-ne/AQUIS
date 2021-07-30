# STA's PocketQube
### Python repository

Development repository for our PocketQube-project.

## How to use

Put contents of lib-folder into lib-folder of E:\CIRCUITPYTHON drive on your board. 
Put code.py into root folder.

## Architecture

```mermaid

flowchart TD


style Node1 fill:#ede26b,stroke-width:2px,stroke:#000000

subgraph "Modules and sensors"
  
  Node20[LTC2934] --> Node1{OBC}
  Node100[IMU2968] --> Node1
  Node40[DRF1268T] --> Node1
  style Node20 fill:#bbf
  style Node100 fill:#bbf
  style Node40 fill:#bbf

end
```
```mermaid
graph LR
    C{Main Loop} --> G
    subgraph State Machine
    G{{Read sensors}} -->|Look at thresholds| I{{Choose next state}}
    end



    I -->|Transmitting| K{{Transmit data}}
    subgraph Communications
    K --> M((Idle))
    M -->|Signal received| N{{Execute commands}}
    end
    M -->|Timeout| L
    N --> L
    I -->|Not transmitting| L[Next loop]


    style G fill:#a2e0cd,stroke-width:2px,stroke:#000000
    style I fill:#a2e0cd,stroke-width:2px,stroke:#000000
    style C fill:#ede26b,stroke-width:2px,stroke:#000000
    style L fill:#ede26b,stroke-width:2px,stroke:#000000
    style K fill:#bbf,stroke-width:2px,stroke:#000000
    style N fill:#bbf,stroke-width:2px,stroke:#000000
    style M stroke-width:2px,stroke:#000000
    
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

> Testing of libraries for external modules
