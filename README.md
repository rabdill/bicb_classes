# BICB Course search

This isn't done yet.

1. Fetch data for a campus (and semester) based on the instructions for the Academic Support Resources [courses API](http://asr-custom.umn.edu/courses/).
1. Save the result as a JSON file.
1. Run "loader.py" with the JSON file's name as the lone parameter. (Example: `python loader.py 2018_fall.json`)
1. The output will be called "final.js" and is referenced directly by index.html. You're done.
