class PaginationHelper:

    # The constructor takes in an array of items and an integer indicating
    # how many items fit within a single page
    def __init__(self, collection, items_per_page):
        self.collection = collection
        self.items_per_page = items_per_page

    # returns the number of items within the entire collection
    def item_count(self):
        return len(self.collection)

    # returns the number of pages
    def page_count(self):
        return len(self.collection) // self.items_per_page + (len(self.collection) % self.items_per_page > 0)

        # returns the number of items on the given page. page_index is zero based

    # this method should return -1 for page_index values that are out of range
    def page_item_count(self, page_index):
        num_of_pages = self.page_count()
        if page_index < 0 or page_index >= num_of_pages:
            return -1
        return self.items_per_page if page_index + 1 != num_of_pages else len(self.collection) % self.items_per_page

    # determines what page an item at the given index is on. Zero based indexes.
    # this method should return -1 for item_index values that are out of range
    def page_index(self, item_index):
        return item_index // self.items_per_page if item_index > 0 and item_index <= len(self.collection) else -1
