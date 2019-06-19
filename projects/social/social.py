from collections import deque
import random

def fisher_yates_shuffle(l):
    for i in range(0, len(l) - 2):
        random_index = random.randint(i, len(l) - 1)
        swap = l[random_index]
        l[random_index] = l[i]
        l[i] = swap

class User:
    def __init__(self, name):
        self.name = name

class SocialGraph:
    def __init__(self):
        self.lastID = 0
        self.users = {}
        self.friendships = {}

    def addFriendship(self, userID, friendID):
        """
        Creates a bi-directional friendship
        """
        if userID == friendID:
            print(f'WARNING: You cannot be friends with yourself {userID}')
        elif friendID in self.friendships[userID] or userID in self.friendships[friendID]:
            print("WARNING: Friendship already exists")
        else:
            self.friendships[userID].add(friendID)
            self.friendships[friendID].add(userID)

    def addUser(self, name):
        """
        Create a new user with a sequential integer ID
        """
        self.lastID += 1  # automatically increment the ID to assign the new user
        self.users[self.lastID] = User(name)
        self.friendships[self.lastID] = set()

    def populateGraph(self, num_users, avg_friendships):
        """
        Takes a number of users and an average number of friendships
        as arguments

        Creates that number of users and a randomly distributed friendships
        between those users.

        The number of users must be greater than the average number of friendships.
        """
        if num_users < avg_friendships:
            raise Exception('The number of users must be greater than the average number of friendships.')
        
        # Reset graph
        self.lastID = 0
        self.users = {}
        self.friendships = {}


        # Add users, populate combos list
        combos = [] #could this be a set? gotta find out what the shuffle function takes

        for i in range(1, num_users + 1):
            self.addUser(f'Test User {i}')
            
            for j in range(i + 1, num_users + 1):
                combos.append((i, j))

        # Shuffle combos list
        fisher_yates_shuffle(combos)
                
        # Create friendships
        total_friendships = num_users * avg_friendships
        for i in combos[:total_friendships // 2]:
            self.addFriendship(i[0], i[1])

    def getAllSocialPaths(self, userID):
        """
        Takes a user's userID as an argument

        Returns a dictionary containing every user in that user's
        extended network with the shortest friendship path between them.

        The key is the friend's ID and the value is the path.
        """
        visited = {}  # Note that this is a dictionary, not a set

        d = deque()
        d.append([userID])
        
        while d:
            path = d.popleft()
            current_friend = path[-1]

            if not current_friend in visited \
               or len(path) < len(visited[current_friend]):
                visited[current_friend] = path

                for friend in self.friendships[current_friend]:
                    path_copy = path.copy()
                    path_copy.append(friend)
                    d.append(path_copy)

        return visited


if __name__ == '__main__':
    sg = SocialGraph()
    sg.populateGraph(10, 2)
    print(sg.friendships)
    friend_count = 0
    for friend_list in sg.friendships.values():
        friend_count += len(friend_list)
    print('friend_count:', friend_count)
    connections = sg.getAllSocialPaths(1)
    print('connections \n', connections)
