table = document.getElementById("results");
cols = ["catalog", "title", "semesters", "credits", "type", "time"];

for(var i=0, entry; entry=data[i]; i++) { // each class
  console.log(entry["catalog"])
  for(var j=0, section; section=entry["sections"][j]; j++) { // each section
    row = table.insertRow(-1);
    for(var k=0, col; col=cols[k]; k++) {
      cell = row.insertCell(k);
      if(col == "time") {
        contents = "";
        console.log(section);
        for(var m=0, time; time=section["times"][m]; m++) { // each meeting time for a section
          for(var n=0, day; day=time["days"][n]; n++) { // each day that it meets at that time
            contents += day;
            if(n < time["days"].length - 1) {
              contents += "/";
            }
          }
          contents += ": " + time["start"] + "&ndash;" + time["end"]
          if(m < section["times"].length - 1) {
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
  }
}
// {"catalog": "AGRO 5021", "title": "Plant Breeding Principles", "semesters": "Every Fall", "credits": "3", "sections": [{"type": "LEC", "times": [{"start": "10:15", "end": "11:30", "location": "Borlaug Hall 306", "days": ["t", "th"]}]}]}