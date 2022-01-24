import datetime
import sys

def handle_recursive_dict(doc):
    data = []
    post = None
    participant = None
    start_time = None
    delta_time = None
    actual_time = None
    goe_location = None
    
    if isinstance(doc, dict):
        for key, value in sorted(doc.items())[::-1]:
            if key == "participantId":
                participant = value

            elif key == "start_time":
                start_time = value

            elif key == "entries":
                for val in value:
                    delta_time, entry = next(iter(val.items()))
                    actual_time = start_time + \
                        datetime.timedelta(days=0, seconds=int(delta_time))
                    if type(entry) is list:
                        # post = ",".join(map(
                        #     str, [participant, actual_time, ",".join(str(x) for x in entry)]))
                        post = [participant, actual_time] + list(entry)
                    else:
                        post = [participant, actual_time, entry]
                    data.append(post)
            else:
                print("Invalid attribute")
                return ""
        return data    