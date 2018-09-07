import json

def load_all_course_info(semester):
  with open("approved.json", "r") as f:
    contents = f.read()
    approved = json.loads(contents)
  with open("{}.json".format(semester), "r") as f:
    contents = f.read()
    parsed = json.loads(contents)
  return approved, parsed

def pull_meeting_times(meetings):
  results = []
  for pattern in meetings:
    # the data is all over the place in these
    if "start_time" not in pattern or pattern["start_time"] is None or pattern["start_time"] == '00:00':
      print("Bad start time; assuming whole class entry is incorrect.")
      return None
    if "location" not in pattern:
      print("\n\nSomething's fishy with this one:")
      print(pattern)
      return None
    results.append({
      "start": pattern["start_time"],
      "end": pattern["end_time"],
      "location": pattern["location"]["description"],
      "days": [d["abbreviation"] for d in pattern["days"]]
    })
  return results

def process_approved_entry(course):
  course_name = "{} {}".format(course["subject"]["subject_id"], course["catalog_number"])
  print("Found one! {}".format(course_name))
  entry = {
    "catalog": course_name,
    "title": course["title"],
    "semesters": course["offer_frequency"],
    "credits": course["credits_minimum"],
    "sections": []
  }
  for section in course["sections"]:
    if "meeting_patterns" not in section: # no meetings this semester
      return None
    times = pull_meeting_times(section["meeting_patterns"])
    if times is None:
      return None
    entry["sections"].append({
      "type": section["component"],
      "times": times
    })
  return entry

if __name__ == "__main__":
  approved, all_courses = load_all_course_info("2018_fall")

  final = []
  for course in all_courses["courses"]:
    dept = course["subject"]["subject_id"]
    num = course["catalog_number"]
    if dept in approved and num in approved[dept]:
      processed = process_approved_entry(course)
      if processed is not None:
        final.append(processed)
  # done evaluating all classes:
  with open("final.js", "w") as f:
    f.write("var data = ") # I know, I know
    f.write(json.dumps(final))
