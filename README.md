Monday.com (formerly DaPulse) library

Api is described here: https://developers.monday.com

Api key can be obtained based on instructions there.

I have created this in order to process data from Redmine (where my developers track their stuff) and Monday/DaPulse (where management/customer manages their wishes)

This is not 1:1 implementation of Monday API (they have it universal), this is more client focused (as you do not want to iterate over columns, boards and look for correct board_id and column_id and follow with update to it, you want to update column for that pulse)

Typical usage:

```python
from monday_library import Monday as M
api_key = "...."
dapulse = M(api_key)
pulse = dapulse.GetPulse(123)
try:
	dapulse.PutColumnValue(pulse,"something",1)
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
- [X] Get Pulse columns  
- [X] Update column for given pulse  
- [ ] Make better library  
- [ ] Write documentation
- [ ] Write tests  
