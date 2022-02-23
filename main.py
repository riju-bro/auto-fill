from tkinter import *


class Trie:
    def __init__(self):
        self.childrens = {}
        self.is_end = False

    def insert(self, key):
        p_crawl = self
        for char in key:
            if not p_crawl.childrens.get(char):
                p_crawl.childrens[char] = Trie()
            p_crawl = p_crawl.childrens[char]
        p_crawl.is_end = True

    def auto_complete(self, key, result, pCrawl, prefix="", ind=0):
        key_len = len(key)
        # Search for prefix is completed
        if ind == key_len:
            # no other string with prefix as key
            if not pCrawl.childrens:
                result.append(prefix)
                return
            self.traverse(pCrawl, prefix, result)
            return
        char = key[ind]
        # string with char lowercase
        tempPCrawl = pCrawl.childrens.get(char.upper())
        if tempPCrawl:
            self.auto_complete(key, result, tempPCrawl, prefix + char.upper(), ind+1)

        # string with char uppercase
        tempPCrawl = pCrawl.childrens.get(char.lower())
        if tempPCrawl:
            self.auto_complete(key, result, tempPCrawl, prefix + char.lower(), ind+1)

    # It is a function for traversing the Trie and printing all words.
    # we use this function as a helper of auto_complete
    def traverse(self, trie_node, string, result):
        if trie_node.is_end:
            result.append(string)
        for key in trie_node.childrens:
            # calling function recursively
            self.traverse(trie_node.childrens[key], string + key, result)


root = Tk()
root.title('Codemy.com - Auto Select/Search')
root.geometry("500x300")


# Update the listbox
def update(data):
    # Clear the listbox
    my_list.delete(0, END)

    # Add toppings to listbox
    for item in data:
        my_list.insert(END, item)


# Update entry box with listbox clicked
def fillout(e):
    # Delete whatever is in the entry box
    my_entry.delete(0, END)

    # Add clicked list item to entry box
    my_entry.insert(0, my_list.get(ANCHOR))


# Create function to check entry vs listbox
def check(e):
    # grab what was typed
    typed = my_entry.get()

    # implementing Trie to autofill
    if typed == '':
        data = toppings
    else:
        data = []
        # third arguement is pCrawl
        trie_node.auto_complete(typed, data, trie_node)

    # update our listbox with selected items
    update(data)


# Create a label
my_label = Label(root, text="Start Typing...",
                 font=("Helvetica", 14), fg="grey")

my_label.pack(pady=20)

# Create an entry box
my_entry = Entry(root, font=("Helvetica", 20))
my_entry.pack()

# Create a listbox
my_list = Listbox(root, width=50)
my_list.pack(pady=40)

# Create a list of pizza toppings
toppings = ["Pepperoni", "Peppers", "Mushrooms",
            "Cheese", "Onions", "Taco", "Broccoli", "popcorn"]

# Add items to trie
trie_node = Trie()
for item in toppings:
    trie_node.insert(item)

# Add the toppings to our list
update(toppings)

# Create a binding on the listbox onclick
my_list.bind("<<ListboxSelect>>", fillout)

# Create a binding on the entry box
my_entry.bind("<KeyRelease>", check)

root.mainloop()
