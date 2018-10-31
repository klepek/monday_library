Monday.com (formerly DaPulse) library

Api is described here: https://developers.monday.com

Api key can be obtained based on instructions there.

I have created this in order to process data from Redmine (where my developers track their stuff) and Monday/DaPulse (where management/customer manages their wishes)

This is not 1:1 implementation of Monday API (quite general), it is more client focused (as you do not want to iterate over columns, boards and look for correct board_id and column_id and follow with update to it, you want to update column for that pulse)

Typical usage:

```python
from monday_library import Monday as M
api_key = "...."
Monday = M(api_key)
pulse = Monday.GetPulse(123)
try:
	Monday.SetColumnValue(pulse,"something",1)
except ColumnNotFound:
	print("scary, missing column")
```

For more information of available Methods, see source-code (sorry, later will be replaced with documentation)

Do not forget to check for exception(s):

AccessErrorException - Your api key or your rights are not good enough  
NotImplemented - Method not implemented yet (contributions will help)  
ColumnNotFound - Column for given pulse not found  
PulseNotFound - Pulse not found  

Status:
- [X] Get Pulse  
- [ ] WIP: Get Pulse columns  
- [ ] WIP: Update column for given pulse  
- [ ] Write documentation
- [ ] Write tests
