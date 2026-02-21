# =============================
# PRIORITY SETTINGS
# =============================

priority_map = {
    "Emergency": 1,
    "VIP": 2,
    "Senior": 3,
    "Normal": 4
}

# =============================
# GLOBAL VARIABLES
# =============================

token_counter = 0
queue_list = []
completed_list = []


# =============================
# ADD TO QUEUE
# =============================

def add_to_queue(name, priority):
    global token_counter, queue_list

    token_counter += 1

    priority_value = priority_map.get(priority, 4)

    queue_list.append({
        "Token": token_counter,
        "Name": name,
        "Priority": priority,
        "PriorityValue": priority_value
    })

    queue_list.sort(key=lambda x: x["PriorityValue"])

    return token_counter


# =============================
# GET QUEUE
# =============================

def get_queue():
    return queue_list


# =============================
# GET COMPLETED LIST
# =============================

def get_completed():
    return completed_list


# =============================
# CALL NEXT PERSON
# =============================

def call_next():
    global queue_list, completed_list

    if queue_list:
        person = queue_list.pop(0)
        completed_list.append(person)
        return person
    return None


# =============================
# RESET QUEUE
# =============================

def reset_queue():
    global queue_list, token_counter
    queue_list.clear()
    token_counter = 0


# =============================
# CALCULATE WAIT TIME
# =============================

def calculate_wait_time(token, avg_service_time=3):
    for index, person in enumerate(queue_list):
        if person["Token"] == token:
            position = index + 1
            wait_time = position * avg_service_time
            return position, wait_time

    return None, None