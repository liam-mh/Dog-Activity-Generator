import random
import csv

def save_to_csv(data):
    with open('output.csv', 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerows(data)

def r(min, max):
    return random.randint(min, max)   

def cal_burned(steps, weight):
    return round(((weight * steps) * 0.004), 1)

def cal_intake(weight, meals=[]):
    rer = (70 * (weight ** 0.75)) / len(meals)
    return round(rer, 1)

def add_behaviour(activity, behaviours=[], row=[]):
    for behavior_array in behaviours:
        if behavior_array[0] == activity:
            row.append(behavior_array[0])
            row.append(behavior_array[1])
            row.append(behavior_array[2])
            row.append(cal_burned(behavior_array[1], row[1])) 
            row.extend(behavior_array[4:])
            break  # Stop searching once a match is found

def create_row(input_weight, eating_time=[], walk_time=[]):
    global day  
    hours = 24
    behaviour = ['Sleeping', 'Playing', 'Normal', 'Walking', 'Eating']
    food = 4.5 * input_weight
    water = 45 * input_weight
    bark = ['None', 'Low', 'Medium', 'High']

    for hour in range(hours):

        # Randomise standard data
        rand_steps = r(50, 300)
        rand_heart_rate = r(100, 110)
        rand_temp = round(random.uniform(24.5, 27.5), 1)
        rand_breath = r(15, 20)

        row = []
        row.append('')  # Blank col for DogID
        row.append(input_weight)  # Dog weight
        row.append('')  # Blank col for date
        row.append(hour)  # Hour

        activity = behaviour[r(0, 2)]  # Roll for activity of sleep, normal, or play
        if activity != 'Normal':
            activity = behaviour[r(0, 2)]
        if activity != 'Normal':
            activity = behaviour[r(0, 2)]
        if hour >= 23 or hour <= 5:
            activity = behaviour[0]  # Sleep between 11pm - 5am
        for meal in eating_time:
            if hour == meal:
                activity = behaviour[4]  # Eat
        for walk in walk_time:
            if hour == walk:
                activity = behaviour[3]  # Walk

        food = cal_intake(input_weight, eating_time)

        arr = [
            # behaviour, steps,                     heart rate,                  calories burned, temperature,         intake cal, intake water,            breath rate,            bark
            ['Sleeping', 0,                         rand_heart_rate + r(1, 3),   0,               rand_temp,           0,          0,                       rand_breath,            bark[0]],
            ['Playing',  rand_steps + r(150, 400),  rand_heart_rate + r(10, 30), 0,               rand_temp + r(3, 5), 0,          0,                       rand_breath + r(6, 17), bark[r(1, 3)]],
            ['Normal',   rand_steps + r(50, 300),   rand_heart_rate + r(2, 7),   0,               rand_temp + r(0, 2), 0,          r(0, int(water * 0.2)),  rand_breath + r(1, 8),  bark[r(0, 1)]],
            ['Walking',  rand_steps + r(500, 3000), rand_heart_rate + r(10, 30), 0,               rand_temp + r(3, 8), 0,          0,                       rand_breath + r(6, 20), bark[r(0, 3)]],
            ['Eating',   rand_steps + r(0, 100),    rand_heart_rate + r(2, 7),   0,               rand_temp + r(0, 2), food,       r(0, int(water * 0.6)),  rand_breath + r(1, 8),  bark[0]]
        ]

        add_behaviour(activity, arr, row)

        if activity == 'Sleeping' :
            row[7] = r(1, 3)
            
        day.append(row)

def main():
    day = [] 
    create_row(8, [6, 18], [7, 19])
    save_to_csv(day)

if __name__ == '__main__':
    main()