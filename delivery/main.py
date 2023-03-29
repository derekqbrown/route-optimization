# Derek Brown - Student ID: 005836312
import schedule


# The main function   time-complexity = O(n^2)
class Main:
    # This function populates the data for reference
    schedule.prepare_packages()
    prompt_str = "-------------\nPerform an action from the list below then hit the Enter key:\n" \
                 "1. Type a Package ID to view package info at end of day \n" \
                 "2. Type a time to view the information for all packages at that time " \
                 "(HH:MM:SS) Times must be military time \n" \
                 "3. Type a time and id to view the package info at a given time " \
                 "(examples: \"9:00:00, 1\" or \"1, 9:00:00\" - separated by a comma) \n" \
                 "4. Type \"q\" to quit program\n-------------\n"
    print("Total distance travelled by all trucks: " + str("{:.2f}".format(schedule.total_distance)) + " miles")
    user_input = input(prompt_str)

    while user_input != "q":
        print("-------------")
        schedule.check_switch(user_input)
        user_input = input(prompt_str)
    print("-------------")
    print("Closing program")
