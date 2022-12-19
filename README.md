# Shard-Count-Execution

- Env setup
  - sudo apt-get install python3-pip
  - pip install uiautomator
  
- Modify all paths to relative test suites location.

- Format of execute command

  ```python3  shard-count.py “test” “retry round” “serial number”```
  ```
  Ex:
  python3 shard-count.py gsi 10 9089f948 96104d9d b3410024 39e25973
  python3 shard-count.py cts 5 9089f948 b3410024
  ```
- Sample result
![image](https://user-images.githubusercontent.com/99638331/208377303-87c6289d-0b00-410c-b8f6-8f38ee3bd346.png)
