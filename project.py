class BSTNode:
    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.left = None
        self.right = None

class MaxHeapNode:
    def __init__(self, id, priority):
        self.id = id
        self.priority = priority

class RequestSystem:
    def __init__(self):
        self.bst_root = None
        self.heap = []

    # ---------- BST Operations ----------
    def insert_bst(self, root, id, name):
        if not root:
            return BSTNode(id, name)
        elif id < root.id:
            root.left = self.insert_bst(root.left, id, name)
        else:
            root.right = self.insert_bst(root.right, id, name)
        return root

    def search_bst(self, root, id):
        if not root:
            return None
        if id == root.id:
            return root
        elif id < root.id:
            return self.search_bst(root.left, id)
        else:
            return self.search_bst(root.right, id)

    def delete_bst(self, root, id):
        if not root:
            return None
        if id < root.id:
            root.left = self.delete_bst(root.left, id)
        elif id > root.id:
            root.right = self.delete_bst(root.right, id)
        else:
            if not root.left:
                return root.right
            elif not root.right:
                return root.left
            temp = self.get_min_value_node(root.right)
            root.id, root.name = temp.id, temp.name
            root.right = self.delete_bst(root.right, temp.id)
        return root

    def get_min_value_node(self, node):
        current = node
        while current.left:
            current = current.left
        return current

    def print_bst(self, root):
        if root:
            print(f"ID: {root.id}, Name: {root.name}")
            self.print_bst(root.left)
            self.print_bst(root.right)

    # ---------- MaxHeap Operations ----------
    def insert_heap(self, id, priority):
        self.heap.append(MaxHeapNode(id, priority))
        self.heapify_up(len(self.heap) - 1)

    def heapify_up(self, index):
        parent = (index - 1) // 2
        if index > 0 and self.heap[index].priority > self.heap[parent].priority:
            self.heap[index], self.heap[parent] = self.heap[parent], self.heap[index]
            self.heapify_up(parent)

    def heapify_down(self, index):
        largest = index
        left = 2 * index + 1
        right = 2 * index + 2

        if left < len(self.heap) and self.heap[left].priority > self.heap[largest].priority:
            largest = left
        if right < len(self.heap) and self.heap[right].priority > self.heap[largest].priority:
            largest = right

        if largest != index:
            self.heap[largest], self.heap[index] = self.heap[index], self.heap[largest]
            self.heapify_down(largest)

    def delete_max_heap(self):
        if len(self.heap) == 0:
            return None
        root = self.heap[0]
        last = self.heap.pop()
        if self.heap:
            self.heap[0] = last
            self.heapify_down(0)
        return root

    def increase_priority(self, id, new_priority):
        for i in range(len(self.heap)):
            if self.heap[i].id == id:
                self.heap[i].priority = new_priority
                self.heapify_up(i)
                return True
        return False

    def process_highest_priority_request(self):
        max_node = self.delete_max_heap()
        if max_node:
            self.bst_root = self.delete_bst(self.bst_root, max_node.id)
            print(f"Processed request ID: {max_node.id}")
        else:
            print("No request to process")

    def print_heap(self):
        for node in self.heap:
            print(f"ID: {node.id}, Priority: {node.priority}")

    # ---------- Interface Functions ----------
    def insert_request(self, id, name, priority):
        self.bst_root = self.insert_bst(self.bst_root, id, name)
        self.insert_heap(id, priority)

    def search_request(self, id):
        node = self.search_bst(self.bst_root, id)
        return node

    def delete_request(self, id):
        self.bst_root = self.delete_bst(self.bst_root, id)
        for i, node in enumerate(self.heap):
            if node.id == id:
                self.heap[i] = self.heap[-1]
                self.heap.pop()
                self.heapify_down(i)
                break

    def is_empty_bst(self):
        return self.bst_root is None

    def is_empty_heap(self):
        return len(self.heap) == 0

    def size_bst(self):
        def count(node):
            return 0 if not node else 1 + count(node.left) + count(node.right)
        return count(self.bst_root)

    def size_heap(self):
        return len(self.heap)


def main():
    system = RequestSystem()  # Create an instance of the request management system

    while True:
        print("\n========== Request Management System ==========")
        print("1. Insert a new request")
        print("2. Delete a request")
        print("3. Search for a request")
        print("4. Process the highest-priority request")
        print("5. Print BST")
        print("6. Print MaxHeap")
        print("7. Increase the priority of a request")
        print("8. Exit")
        
        choice = input("Enter your choice (1-8): ")

        if choice == "1":
            try:
                id = int(input("Enter Request ID (integer): "))
                name = input("Enter Request Name: ")
                priority = int(input("Enter Request Priority (integer): "))
                system.insert_request(id, name, priority)
                print("Request inserted successfully.")
            except ValueError:
                print("Invalid input. ID and Priority must be integers.")

        elif choice == "2":
            try:
                id = int(input("Enter ID to delete: "))
                system.delete_request(id)
                print("Request deleted successfully (if it existed).")
            except ValueError:
                print("Invalid input. ID must be an integer.")

        elif choice == "3":
            try:
                id = int(input("Enter ID to search: "))
                result = system.search_request(id)
                if result:
                    print(f"Request found - ID: {result.id}, Name: {result.name}")
                else:
                    print("Request not found.")
            except ValueError:
                print("Invalid input. ID must be an integer.")

        elif choice == "4":
            system.process_highest_priority_request()

        elif choice == "5":
            print("BST:")
            system.print_bst(system.bst_root)

        elif choice == "6":
            print("MaxHeap:")
            system.print_heap()

        elif choice == "7":
            try:
                id = int(input("Enter ID to update priority: "))
                new_priority = int(input("Enter new priority: "))
                if system.increase_priority(id, new_priority):
                    print("Priority updated successfully.")
                else:
                    print("Request ID not found in heap.")
            except ValueError:
                print("Invalid input. Both ID and priority must be integers.")

        elif choice == "8":
            print("Exiting the system. Goodbye!")
            break

        else:
            print("Invalid choice. Please select a number between 1 and 8.")

if __name__ == "__main__":
    main()
