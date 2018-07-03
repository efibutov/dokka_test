From inside the package directory do following steps:

0. Assuming you have a virtenv inside the current (package's) dir, activate the virtenv:
    source virtenv/bin/activate
    Now you're running local virtenv's interpreter rather than 'global system's' one
1. Install the requirements using:
    pip install -r requirements.txt
2. Run the webserver using
    python app.py
3. Open additional shell and test the API using curl:
    curl -i -F data=@./data.csv localhost:5000/get_addresses
    (./data.csv is a test data file inside the dir)
    If you see an output similar to this:

    {"points": [{"name": "A", "address": "Kyiv, 01001, Ukraine"}, {"name": "D", "address": "Kyiv, 01001, Ukraine"}, {"name": "B", "address": "Kyiv, 01030, Ukraine"}, {"name": "C", "address": "Danyla Halytskoho vulytsia, 46/1, Sumy, Ukraine"}], "links": [{"distance": 614.4096018960828, "name": "AC"}, {"distance": 3.395493274661279, "name": "AB"}, {"distance": 0.0, "name": "AD"}, {"distance": 6533.723229415757, "name": "CB"}, {"distance": 6555.121165896085, "name": "CD"}, {"distance": 3.5820387258441886, "name": "BD"}]}%

    then everything's OK
3a. Optionally: open a browser on http://localhost:5000/get_addresses and upload the provided data.csv
    (If using Chrome it is recommended to install any JSON plugin for nice output)
