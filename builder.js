function build_page() {
  refresh = document.createElement('tbody');
  refresh.setAttribute("id", "refresh")

  cols = ["catalog", "title", "semesters", "credits", "type", "time"];
  var checkboxes = document.getElementsByName('exclude_day');
  var exclude_days = [];
  for (var day of checkboxes) {
    if (day.checked) {
      exclude_days.push(day.value)
    }
  }

  for(var entry of data) { // each class
    for(var section of entry["sections"]) { // each section
      row = refresh.insertRow(-1);
      throw_out = false;
      for(var i=0, col; col=cols[i]; i++) {
        cell = row.insertCell(i);
        if(col == "time") {
          contents = "";
          for(var k=0, time; time=section["times"][k]; k++) { // each meeting time for a section
            for(var j=0, day; day=time["days"][j]; j++) { // each day that it meets at that time
              if(exclude_days.includes(day)) {
                throw_out = true;
                break;
              }
              contents += day;
              if(j < time["days"].length - 1) {
                contents += "/";
              }
            }
            contents += ": " + time["start"] + "&ndash;" + time["end"]
            if(k < section["times"].length - 1) {
              contents += " and ";
            }
          }
        } else if(col == "type") {
          contents = section["type"];
        } else {
          contents = entry[col];
        }
        cell.innerHTML = contents;
      }
      if(throw_out) {
        row = refresh.deleteRow(refresh.rows.length - 1);
      }
    }
  }
  table = document.getElementById("resultsTable");
  old = document.getElementById("results");
  table.replaceChild(refresh, document.getElementById("results"));
  refresh.setAttribute("id", "results"); // so we can find it next time
}

build_page();