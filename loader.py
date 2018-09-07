import json

with open("approved.json", "r") as f:
  contents = f.read()
  approved = json.loads(contents)
with open("2018_fall.json", "r") as f:
  contents = f.read()
  parsed = json.loads(contents)

final = []
for course in parsed["courses"]:
  dept = course["subject"]["subject_id"]
  num = course["catalog_number"]
  if dept in approved and num in approved[dept]:
    print("Found one! {} {}".format(dept, num))
    entry = {
      "catalog": "{} {}".format(dept, num),
      "title": course["title"],
      "semesters": course["offer_frequency"],
      "credits": course["credits_minimum"],
      "sections": []
    }
    for section in course["sections"]:
      section_entry = {
        "type": section["component"],
        "times": []
      }
      if "meeting_patterns" not in section: # no meetings this semester
        continue
      for pattern in section["meeting_patterns"]:
        if "start_time" not in pattern or pattern["start_time"] is None or pattern["start_time"] == '00:00':
          continue
        if "location" not in pattern:
          # the data is all over the place in these
          print("\n\nSomething's fishy with this one:")
          print(pattern)
        newtime = {
          "start": pattern["start_time"],
          "end": pattern["end_time"],
          "location": pattern["location"]["description"],
          "days": [d["abbreviation"] for d in pattern["days"]]
        }
        print(newtime)
        section_entry["times"].append(newtime)
      # else:
      #   continue # if it ran into a busted meeting pattern
      entry["sections"].append(section_entry)
    final.append(entry) # we're done one class
# done evaluating all classes:
with open("done.json", "w") as f:
  f.write(json.dumps(final))