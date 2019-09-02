import csv
from collections import defaultdict
from model import *

EVE = "Evening Only"

global booked_counter 


def setup_schedule(data):
   
    # setup stations
    nails = Schedule(name="Nails", period=2 , num_attendants=6)
    data = nails.build(data)

    massage = Schedule(name="Massage", period=3 , num_attendants=6)
    data = massage.build(data)

    strolf = Schedule(name="Strolf", period=3 , num_attendants=3)
    data = strolf.build(data)

    eyebrows = Schedule(name="Eyebrows", period=3 , num_attendants=4)
    data = eyebrows.build(data)

    hair =Schedule(name="Hair",period=2 , num_attendants=4)
    data = hair.build(data)

    makeup=Schedule(name="Makeup", period=3 , num_attendants=2)
    data = makeup.build(data)

    meditation =Schedule(name="Meditation", period=2 , num_attendants=12)
    data = meditation.build(data)

    facial =Schedule(name="Facial", period=3 , num_attendants=2)
    data   = facial.build(data)

    napping = Schedule(name="Napping", period=2, num_attendants=4)
    data = napping.build(data)
    return data
    
  
def map_appointments():
    names = defaultdict()
    names["Spa Nails- Shellac Express Manicures- 15 minutes"]="Nails"
    names["Mama Mobile Massage Sponsored by Beneplan- 10 minutes"]="Massage"
    names["Strolf Deep Stretch- 15 minutes"]="Strolf"
    names["WAXON Brow shaping Wax or Threading- 10 minutes"]="Eyebrows"
    names["VENT Braid Bar and Hot Tools Touch Ups- 15 minutes"]="Hair"
    names["Festival Face Makeup - 10 minutes"]="Makeup"
    names["HOAME Meditation Garden - 10 minutes"]="Meditation"
    names["Well.ca Mini Facial!- 10 minutes"]="Facial"
    names["Fort Botique Resting Eye Masks- 10 minutes"]="Napping"
    
    return names

def find_next_opening(time_requested):
   
    the_index = hours.index(time_requested) 
    next_index = the_index + 1
    if next_index > len(hours):
        next_index = 0

    return hours[next_index]
    
def fit_guest_into_appointment(guest, data):
    for choice in guest.choices:
        times = guest.times 
        
        times.append(find_next_opening(times[-1]))
        for timeslot in guest.times:
           
            desired_slots = data[choice][timeslot]
            #print(choice, timeslot, desired_slots)
            for spaces in desired_slots:
                
                for s in desired_slots[spaces]:
                    current_guest = desired_slots[spaces][s]
                    if current_guest.status ==0:
                        data[choice][timeslot][spaces][s] = guest
                        output = "Booked {} for {} at {}".format(guest.full_name(), choice, timeslot)
                        f= open("book.md","a+")
                        f.write(output + "\n")
                        f.close()
                        print(output)
                        
                        return data
        #where does the next piece work
        
    print("Could not book {} for {} at {}".format(guest.full_name(), guest.choices, guest.times))
    return data
               
 
def get_service_from_name(name,name_maps):
    if "EVENING" in name:
        return None
    if "choice" in name:
        return None
    if name in name_maps:
        return name_maps[name]
    else:
        return None

def main():
    data = defaultdict()  
    data = setup_schedule(data)  
    guests = []
    name_maps = map_appointments()
    import os
    try:
        os.remove("book.md")
    except:
        pass
        
    try:
        os.remove("schedule.md")
    except:
        pass

    # get guest import
    with open('data.csv', newline='\n') as csvfile:
        moms = csv.reader(csvfile, delimiter=',', quotechar='|')
        next(moms, None) 
        for row in moms:
            if row[4]!=EVE:
                choices = []
                service = get_service_from_name(row[5], name_maps)
                if service != None:
                    choices.append(service)
                
                service = get_service_from_name(row[6], name_maps)
                if service != None:
                    choices.append(service)

                service = get_service_from_name(row[7], name_maps)
                if service != None:
                    choices.append(service)
            
                times = []
                
                if row[8]!="" and "EVENING ONLY" not in row[8] and "choice" not in row[8]:
                    time1 = row[8].split("-")
                    if time1[0] =="No Preference":
                        times.append("2:00")
                    else:
                        times.append(time1[0].strip())
                if row[9]!="" and "EVENING ONLY" not in row[9]  and "choice" not in row[9]:
                    time2 = row[9].split("-")
                    if time2[0] =="No Preference":
                        times.append("2:30")
                    else:
                        times.append(time2[0].strip())
                if times == []:
                    times = ["2:30", "3:00"]


                g = Guest(first_name = row[0].strip(), 
                last_name = row[1].strip(), 
                phone = row[2].strip(), 
                email = row[3].strip(), 
                times = times,
                choices = choices,
                status=1)
                guests.append(g)
    booked_counter = 0      
    for g in guests:
        booked_counter = booked_counter  + 1
        data = fit_guest_into_appointment(g, data) 
    print("booked {} guests for appointments".format(booked_counter))
    print("=========================================")
    f= open("appointments.md","a+")
                        
                        
    for d in data:
        f.write("#  " + d + "\n")
        
        for slots in data[d]:
            f.write("##  " + slots + "\n")
            
            for opening in data[d][slots]:
                
                for attendant in data[d][slots][opening]:
                    #for guest in data[d][slots][opening][attendant]:
                    
                    g = data[d][slots][opening][attendant]
                    if g.status==1:
                        f.write("-  " + g.display() + "\n")
                       
                    
    f.close()

if __name__ == '__main__':
    main()
