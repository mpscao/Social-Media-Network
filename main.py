
from Graph import *
from typing import IO, Tuple, List
# constants that allows the user to input a number to access one part of the menu
PROGRAMMER = "Darren Cao"
MEMBER_INFO = "1"
NUM_OF_FRIENDS = "2"
LIST_OF_FRIENDS = "3"
RECOMMEND = "4"
SEARCH = "5"
ADD_FRIEND = "6"
REMOVE_FRIEND = "7"
SHOW_GRAPH = "8"
SAVE = "9"
# line that separates each time the user inputs a number
LINE = "\n*-*_*-*_*-*_*-*_*-*_*-*_*-*_*-*_*-*_*-*_*-*_*-*_*-*_*-*_*-*\n"


class Member:
    # method to instantiate id, name, email and country of member in network
    def __init__(self, member_id: int,
                 first_name: str,
                 last_name: str,
                 email: str,
                 country: str):
        # instantiates the id of the member
        self.member_id = member_id
        # instantiates the first name of the member
        self.first_name = first_name
        # instantiates the last name of the member
        self.last_name = last_name
        # instantiates the email of the member
        self.email = email
        # instantiates the country of the member
        self.country = country
        # instantiates a list of the id's of all friends of member
        self.friends_id_list = []
    # method to add friend to a member
    def add_friend(self, friend_id) -> None:
        # use the append function to add a new friend for the member
        self.friends_id_list.append(friend_id)
    # method to remove friend from a member
    def remove_friend(self, friend_id) -> None:
        # use the remove function to add a new friend for the member
        self.friends_id_list.remove(friend_id)
    # method to show list of id's of all friends of member
    def friend_list(self) -> List[int]:
        # return a list of the id's of all friends of member
        return self.friends_id_list
    # method to give the number of friends a user has
    def number_of_friends(self) -> int:
        # the length of the list gives the number of friends of the person since each id in list is a friend
        return len(self.friends_id_list)
    # method that will print the attributes of a member of the network
    def __str__(self) -> str:
        # string that will give name, email, country, and number of friends of a member in network
        message = self.first_name + " " + self.last_name + "\n" + self.email + "\n" + "From " + self.country + "\n" \
                  + "Has " + str(self.number_of_friends()) + " friends"
        return message

    # method that will print the first and last name of member
    def display_name(self) -> str:
        return self.first_name + " " + self.last_name

def open_file(file_type: str) -> IO:
    
    file_name = input("Enter the " + file_type + " filename:\n")
    # TODO To save time, comment out the above line and uncomment the following section
    # if file_type == "profile":
    #   file_name = "profile_10.csv"
    #else:
    #  file_name = "connection_10.txt"
    # file is not changeable
    file_pointer = None
    while file_pointer is None:
        try:
            # try to open and read file now that have access to file pointer loaded in program
            file_pointer = open(file_name, "r")
        except IOError:
            # except if the file can't be opened, let user know if the file name is invalid
            print(f"An error occurred while opening the file {file_name}.\n"
                  f"Make sure the file path and name are correct \nand that "
                  f"the file exist and is readable.")
            # ask them to input file name that is a string again
            file_name = input("Enter the " + file_type + " filename:\n")

    return file_pointer


def create_network(fp: IO) -> List[List[int]]:
    # the number in first line gives number of members of network
    size = int(fp.readline())
    # list of network of members
    network = []

    for i in range(size):
        # create empty lists according to number of members
        network.append([])
    # read the lines that have member and its friend
    line = fp.readline()
    # while there are lines and there are at least 3 lines which is necessary to create a network
    while line is not None and len(line) >= 3:
        # separate each number in line by space while removing unnecessary whitespaces
        split_line = line.strip().split(" ")
        # make the first number starting from the 2nd line the first member
        member_id1 = int(split_line[0])
        # make the second number starting from the 2nd line the second member
        member_id2 = int(split_line[1])
        if member_id2 not in network[member_id1]:
            # if the 2nd member has not already been placed as a friend of the first member, do so
            network[member_id1].append(member_id2)
        if member_id1 not in network[member_id2]:
            # do the same by placing the 1st member in the inner list of the 2nd member since friends are always mutual
            network[member_id2].append(member_id1)
        # order the network of the first member from lowest to highest id
        network[member_id1].sort()
        # order the network of the second member from lowest to highest id
        network[member_id2].sort()
        # continue reading each line into list
        line = fp.readline()
    # return the full network of friends
    return network


def num_in_common_between_lists(list1: List, list2: List) -> int:
    # set the degree of common friends initially to 0
    degree = 0
    for i in range(len(list1)):
        if list1[i] in list2:
            # add a degree of common friends if any of the friends of the first member is also a friend of the 2nd member
            # (in both lissts)
            degree += 1

    return degree


def init_matrix(size: int) -> List[List[int]]:
    # create empty matrix
    matrix = []
    for row in range(size):
        # add the number of rows to the matrix according to number of members
        matrix.append([])
        for column in range(size):
            # in each row, add a column of 0's according to number of members
            matrix[row].append(0)

    return matrix


def calc_similarity_scores(profile_list: List[Member]) -> List[List[int]]:
    # create a similarity matrix that is of the size network
    matrix = init_matrix(len(profile_list))

    for i in range(len(profile_list)):
        for j in range(i, len(profile_list)):
            # call the function to find the number of friends in common between users
            degree = num_in_common_between_lists(profile_list[i].friends_id_list,
                                                 profile_list[j].friends_id_list)
            matrix[i][j] = degree # assign degree of similarity to matrix for first user
            matrix[j][i] = degree # do the same for the 2nd user because friendships are mutual

    return matrix


def recommend(member_id: int, friend_list: List[int], similarity_list: List[int]) -> int:
    # make similarity amount a very small number so it gets taken by the first friend of member
    max_similarity_val = -1
    # make similarity position an id that does not already exist
    max_similarity_pos = -1

    for i in range(len(similarity_list)):
        # check if the friend is not a friend already and is not the user itself
        if i not in friend_list and i != member_id:
            # if the member has more friends in common than the previous member with most friends in common
            if max_similarity_val < similarity_list[i]:
                # make that friend's id the new recommended friend
                max_similarity_pos = i
                # make that number of friends in common the new highest number of friends in common
                max_similarity_val = similarity_list[i]

    return max_similarity_pos


def create_members_list(profile_fp: IO) -> List[Member]:
    # make an empty list of the profiles
    profiles = []
    # skip first line since first line is header
    profile_fp.readline()
    # reads the lines that actually contain data
    line = profile_fp.readline()
    # separating each element of each line by comma
    profile_list = line.split(',')
    # while there are lines and each line has the 5 attributes
    while line is not None and len(profile_list) == 5:
        # get rid of extra unnecessary spaces to extract just the member id
        member_id = profile_list[0].strip()
        # get rid of extra unnecessary spaces to extract just the member's first name
        first_name = profile_list[1].strip()
        # get rid of extra unnecessary spaces to extract just the member's last name
        last_name = profile_list[2].strip()
        # get rid of extra unnecessary spaces to extract just the member's email
        email = profile_list[3].strip()
        # get rid of extra unnecessary spaces to extract just the country member is from
        country = profile_list[4].strip()
        # add all of that information to the list of profiles
        profiles.append(Member(member_id, first_name, last_name, email, country))
        # Continue reading the next lines
        line = profile_fp.readline()
        # Continue separating according to comma for each line
        profile_list = line.split(',')

    return profiles


def display_menu():
    print("\nPlease select one of the following options.\n")
    # prints out the menu of options the user can choose from according to number
    print(MEMBER_INFO + ". Show a member's information \n" +
          NUM_OF_FRIENDS + ". Show a member's number of friends\n" +
          LIST_OF_FRIENDS + ". Show a member's list of friends\n" +
          RECOMMEND + ". Recommend a friend for a member\n" + SEARCH +
          ". Search members by country\n" + ADD_FRIEND + ". Add friend\n" + REMOVE_FRIEND
          + ". Remove friend\n" + SHOW_GRAPH + ". Show graph\n" + SAVE + ". Save changes\n")
    # receive which item from menu user wants to do or explore
    return input("Press any other key to exit.\n")


def receive_verify_member_id(size: int):
    # make the user id initially an invalid one
    valid = False
    while not valid:
        # ask the user for the id he or she wishes to access
        member_id = input(f"Please enter a member id between 0 and {size}:\n")
        if not member_id.isdigit():
            # if the id is not a number, let the user know
            print("This is not a valid entry.")

        elif not 0 <= int(member_id) < size:
            # if the id is not in the range of number of the network, let the user now
            print("This member id does not exist.")
        else:
            # else the conditions are satisfied, allow the user to use that id
            valid = True
    # return id as integer
    return int(member_id)


def add_friend(profile_list: List[Member],
               similarity_matrix: List[List[int]]) -> None:
    # get the number of members in network
    size = len(profile_list)
    print("For the first friend: ")
    # verify the first id the user entered is a valid id
    member1 = receive_verify_member_id(size)
    print("For the second friend: ")
    # verify the second id the user entered is a valid id
    member2 = receive_verify_member_id(size)
    if member1 == member2:
        # ask the user for a different id if the two ids are the same
        print("You need to enter two different ids. Please try again.")
    elif member1 in profile_list[member2].friends_id_list:
        # ask the user to enter new id(s) if the two members entered were already friends
        print("These two members are already friends. Please try again.")
    else:
        # otherwise add the 2nd member to the friend's list of the 1st member
        profile_list[member1].add_friend(member2)
        # do the same for the 2nd member since friendships are always mutual
        profile_list[member2].add_friend(member1)

        for i in range(size):
            # if the first member's new friend is a common friend between the first member and other members
            if member2 in profile_list[i].friends_id_list:
                # increase number of common friends between those two members for first member matrix
                similarity_matrix[member1][i] += 1
                # other than the first member him or herslf,
                if member1 != i:
                    #increase number of common friends for matrix of other members since they too will have one more
                    # friend in common
                    similarity_matrix[i][member1] += 1
            # repeat the same for the friend of first member(second member) since friendships are mutual
            if member1 in profile_list[i].friends_id_list:
                similarity_matrix[member2][i] += 1
                if member2 != i:
                    similarity_matrix[i][member2] += 1
        print("The connection is added. Please check the graph.")


def remove_friend(profile_list: List[Member],
                  similarity_matrix: List[List[int]]) -> None:
    # get the number of members in network
    size = len(profile_list)
    print("For the first friend: ")
    # verify the first id the user entered is a valid id
    member1 = receive_verify_member_id(size)
    # ask the user to choose an id from the list of friends of first member
    print(f"For the second friend, select from following list: {profile_list[member1].friends_id_list}")
    # verify the second id the user entered is a valid id
    member2 = receive_verify_member_id(size)
    if member1 == member2:
        # ask the user for a different id if the two ids are the same
        print("You need to enter two different ids. Please try again.")
    elif member1 not in profile_list[member2].friends_id_list:
        # ask the user for a different id if the 2nd member id is not already a friend of the first member
        print("These two members are not friends. Please try again.")
    else:
        # otherwise add the 2nd member to the friend's list of the 1st member
        profile_list[member1].remove_friend(member2)
        # do the same for the 2nd member since friendships are always mutual
        profile_list[member2].remove_friend(member1)
        for i in range(size):
            # if the first member's new friend was a common friend between the first member and other members
            if member2 in profile_list[i].friends_id_list:
                # decrease number of common friends between those two members for first member matrix
                similarity_matrix[member1][i] -= 1
                # other than the first member him or herslf,
                if member1 != i:
                    # decrease number of common friends for matrix of other members since they too will have one less
                    # friend in common
                    similarity_matrix[i][member1] -= 1
            # repeat the same for the friend of first member(second member) since lost friendships are mutual
            if member1 in profile_list[i].friends_id_list:
                similarity_matrix[member2][i] -= 1
                if member2 != i:
                    similarity_matrix[i][member2] -= 1
        # first member needs to remove one mutual friend from the similarity matrix with him or herself as well
        similarity_matrix[member1][member1] -= 1
        # same needs to be done for 2nd member since friendships are mutual
        similarity_matrix[member2][member2] -= 1

        print("The connection is removed. Please check the graph.")
# This function asks for a country name and list all members from that country.
def search(profile_list: List[Member]) -> None:
    # ask user for country
    location = input("Please enter a country name: ")
    # check if any member is from that country by making the checker false initially
    exist = False

    for i in range(len(profile_list)):
        # if the country the user entered is one of the countries a member of the network is from(ignoring case-sensite)
        if profile_list[i].country.casefold() == location.casefold():
            # if any member is from that country, make it true
            exist = True
            # print that member's name
            print(profile_list[i].display_name())
    if exist == False:
        #if no member is found from the country entered, let the user know
        print("No member comes from the country you entered. Please check for typos and try again.")



def add_friends_to_profiles(profile_list: List[Member],
                            network: List[List[int]]) -> None:
    for i in range(len(profile_list)):
        # add friends from the network list to the friends id list from the profile for consistency
        profile_list[i].friends_id_list = network[i]


def select_action(profile_list: List[Member],
                  network: List[List[int]],
                  similarity_matrix: List[List[int]]) -> str:
    response = display_menu()
    # print the constant LINE to create space between new selections from menu
    print(LINE)
    # get the number of members in network
    size = len(profile_list)

    if response in [MEMBER_INFO, NUM_OF_FRIENDS, LIST_OF_FRIENDS, RECOMMEND]:
        # if the selection requires the user to input a member id, verify if the id exists
        member_id = receive_verify_member_id(size)

    if response == MEMBER_INFO:
        # if the user wants to know member information, print the 5 attributes of the member
        print(profile_list[member_id])
    elif response == NUM_OF_FRIENDS:
        # if the user wants to know number of friends, use Member's number of friends function to get number of friends
        print(f"{profile_list[member_id].first_name} has {profile_list[member_id].number_of_friends()} Friends.")
    elif response == LIST_OF_FRIENDS:
        # make friend_list the list of friends of a user by calling friend_list from class Member
        friend_list = profile_list[member_id].friend_list()
        for i in range(len(friend_list)):
           # for each friend in the friends list, print the id and the name corresponding to that id from profile_list
           print(str(friend_list[i]) + " " + profile_list[friend_list[i]].display_name())
    elif response == RECOMMEND:
        # for more space, made rec_id the id of the friend that would be recommended to a member
        rec_id = recommend(member_id, profile_list[member_id].friend_list(), similarity_matrix[member_id])
        # print the message using f-string that gives both the recommended friend's name and id.
        print(f"The suggested friend for {profile_list[member_id].display_name()} is {profile_list[rec_id].display_name()} "
              f"with id {rec_id}.")
    elif response == SEARCH:
        # call the search function to search members from a country
        search(profile_list)
    elif response == ADD_FRIEND:
        # call the add friend function for a member to add a friend
        add_friend(profile_list, similarity_matrix)
    elif response == REMOVE_FRIEND:
        # call the remove friend function for a member to remove a friend
        remove_friend(profile_list, similarity_matrix)
    elif response == SHOW_GRAPH:
        # create an empty list
        tooltip_list = []
        for profile in profile_list:
            # add the profiles to the empty list
            tooltip_list.append(profile)
        # create a graph that has attributes of class Graph with a size of the number of members
        # and has the list of profiles and network list
        graph = Graph(PROGRAMMER,
                      [*range(len(profile_list))],
                      tooltip_list, network)
        # draw the graph of network of members by calling the graph function from class Graph
        graph.draw_graph()
        print("Graph is ready. Please check your browser.")
    elif response == SAVE:
        # call the save_changes function if the user wants to save a file
        save_changes(profile_list)
    else:
        # if any other character is entered, exit the program
        return "Exit"
    # print the constant LINE to create space between new selections from menu
    print(LINE)
    # continue the program
    return "Continue"


def save_changes(profile_list: List[Member]) -> None:
    # ask for the new file name that will be saved
    file_save = input("Please enter the filename:")
    # handler to open the output file and to write it
    output_save = open(file_save, "w")
    # the first line will be the number of members
    first_line = str(len(profile_list))
    # create an empty list current that will contain the network of friends
    current = []
    for member in profile_list:
        # for each friend in the list of friend id's of each member
        for friend in member.friends_id_list:
            # to avoid repeating friend combinations
            if int(member.member_id) < friend:
                # each line starting from the 2nd line being added to the output
                current.append(str(member.member_id) + " " + str(friend) + "\n")
    # add all of the combination of friends to the first line, which is the number of members
    first_line += "\n" + "".join(current)
    # write the new output file
    output_save.write(first_line)
    # close the file
    output_save.close
    print("All changes are saved in " + file_save)



def initialization() -> Tuple[List[Member], List[List[int]], List[List[int]]]:
    # open the profile file
    profile_fp = open_file("profile")
    # return the file pointer to create function create_members_list
    profile_list = create_members_list(profile_fp)
    # open the connection file
    connection_fp = open_file("connection")
    # return a file pointer to create a network of who are the friends
    network = create_network(connection_fp)
    # use the add friends to profile function to add friends from network to profile for consistency
    add_friends_to_profiles(profile_list, network)
    # create similarity matrix that is n by n with n being the number of member in network
    similarity_matrix = calc_similarity_scores(profile_list)
    # close profile file
    profile_fp.close()
    # close connection file
    connection_fp.close()

    return profile_list, network, similarity_matrix

def main():
    print("Welcome to the network program.")
    print("We need two data files.")
    # initialize/create the profile list, network and similarity matrix
    profile_list, network, similarity_matrix = initialization()
    # make the action continue unless the user asks to exit
    action = "Continue"
    while action != "Exit":
        # ask the user for inputs to the menu as long as the user does not wish to exit
        action = select_action(profile_list, network, similarity_matrix)

    input("Thanks for using this program.")


if __name__ == "__main__":
    main()
