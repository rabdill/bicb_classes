import json
import sys

# (based on data from http://asr-custom.umn.edu/courses/ )
# example: https://courses.umn.edu/campuses/umntc/terms/1193/courses.json
# term numbers: https://classroom.umn.edu/scheduling/classes/session-dates

def load_all_course_info(filename):
  with open("approved.json", "r") as f:
    contents = f.read()
    approved = json.loads(contents)
  with open(filename, "r") as f:
    contents = f.read()
    parsed = json.loads(contents)
  return approved, parsed

def pull_meeting_times(meetings, location):
  results = []
  for pattern in meetings:
    # the data is all over the place in these
    if "start_time" not in pattern or pattern["start_time"] is None:# or pattern["start_time"] == '00:00':
      print("Bad start time; assuming whole class entry is incorrect.")
      pattern["start_time"] = ""
      pattern["end_time"] = ""
      # return None
    answer = {
      "start": pattern["start_time"],
      "end": pattern["end_time"],
      "days": [d["abbreviation"] for d in pattern["days"]],
      "location": location
    }
    if "location" in pattern and "description" in pattern["location"]:
      answer["location"] = pattern["location"]["description"]
    results.append(answer)
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
  if "sections" not in course or len(course["sections"]) == 0:
    print("  **WARN**: Didn't find any sections")
    return entry
  for section in course["sections"]:
    if "meeting_patterns" not in section: # no meetings this semester
      return None
    times = pull_meeting_times(section["meeting_patterns"], section["location"])
    if times is None:
      print("  WARN: Didn't find any times for this section")
    else:
      entry["sections"].append({
        "type": section["component"],
        "times": times
      })
  return entry

if __name__ == "__main__":
  if len(sys.argv) < 2:
    print("Source data filename required.")
    exit(1)
  approved, all_courses = load_all_course_info(sys.argv[1])

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
