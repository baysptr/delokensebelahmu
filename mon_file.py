import time
import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class Watcher:
    DIRECTORY_TO_WATCH = "/home/private/Documents/mas_bagus/test"

    def __init__(self):
        self.observer = Observer()

    def run(self):
        event_handler = Handler()
        self.observer.schedule(event_handler, self.DIRECTORY_TO_WATCH, recursive=True)
        self.observer.start()
        try:
            while True:
                time.sleep(5)
        except:
            self.observer.stop()
            print("Error")

        self.observer.join()

class Pecah:
    def linear_search(item, my_list):
        found = False
        position = 0
        while position < len(my_list) and not found:
            if my_list[position] == item:
                found = True
            position = position + 1
        return found


class Handler(FileSystemEventHandler):

    @staticmethod
    def on_any_event(event):
        if event.is_directory:
            return None

        elif event.event_type == 'created':
            # Take any action here when a file is first created.
            currentDT = datetime.datetime.now()
            out_text = event.src_path
            itemfound = Pecah.linear_search('swp', out_text.split('.'))
            if itemfound:
                print("...")
            else:
                print("Created: {}".format(out_text))
                print("Time: {}-{}-{} {}:{}:{}".format(currentDT.day, currentDT.month, currentDT.year, currentDT.hour, currentDT.minute, currentDT.second))
            #print("Created: {}".format(event.src_path))

        elif event.event_type == 'modified':
            # Taken any action here when a file is modified.
            currentDT = datetime.datetime.now()
            out_text = event.src_path
            itemfound = Pecah.linear_search('swp', out_text.split('.'))
            if itemfound:
                print("...")
            else:
                print("Modified: {}".format(out_text))
                print("Time: {}-{}-{} {}:{}:{}".format(currentDT.day, currentDT.month, currentDT.year, currentDT.hour, currentDT.minute, currentDT.second))
            #print("Modified: {}".format(event.src_path))
            #print("Time: {}-{}-{} {}:{}:{}".format(currentDT.day, currentDT.month, currentDT.year, currentDT.hour, currentDT.minute, currentDT.second))
        elif event.event_type == 'deleted':
            # Taken any action here when a file is modified.
            currentDT = datetime.datetime.now()
            out_text = event.src_path
            itemfound = Pecah.linear_search('swp', out_text.split('.'))
            if itemfound:
                print("...")
            else:
                print("Deleted: {}".format(out_text))
                print("Time: {}-{}-{} {}:{}:{}".format(currentDT.day, currentDT.month, currentDT.year, currentDT.hour, currentDT.minute, currentDT.second))    


if __name__ == '__main__':
    w = Watcher()
    w.run()
